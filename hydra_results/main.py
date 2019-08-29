from states import *

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

import os
import ast
import re
import time
import numpy as np


n_processed_states = 0


def evaluate(n=10, m=80, n_models=10000, tau_local=6, n_cores=4):
	global n_processed_states

	spark = SparkConf().setMaster('local[%i]' % n_cores).set('spark.cores.max', n_cores).set('spark.executor.cores', n_cores)
	sc = SparkContext(conf=spark)
	print(sc.defaultParallelism)

	BATCH_INTERVAL = 0.05

	# Create streaming context, with required batch interval
	ssc = StreamingContext(sc, BATCH_INTERVAL)
	ssc.checkpoint('checkpoint')

	rddQueue = list()
	for i in range(50):
	    rddQueue.append([(None, np.random.rand(1 + n + m))])
	dstream = ssc.queueStream(rddQueue)
	
	nus = np.linspace(0.5, 1.0, n_models)
	initial_states = [create_state('mod%i' % (i + 1), n, m, nus[i]) for i in range(n_models)]

	# Evaluate inputs to lists and convert them to arrays
	array_dstream = dstream.map(lambda x: np.array(x[1]))
	#array_dstream.pprint()

	array_dstream = array_dstream.flatMap(lambda x: [('mod%i' % (i + 1), ('mod%i' % (i + 1), x)) for i in range(n_models)])
	#array_dstream.pprint()

	full_state_RDD = sc.parallelize([(u'mod%i' % (i + 1), initial_states[i]) for i in range(n_models)])


	if m <= tau_local:
	    updated_full_state_dstream = array_dstream.updateStateByKey(full_state_update, initialRDD=full_state_RDD)
	else:
	    partial_state_RDD = full_state_RDD.flatMap(lambda x: [(x[0], s) for s in split_state(x[1])])
	    updated_partial_state_dstream = array_dstream.updateStateByKey(partial_state_update, initialRDD=partial_state_RDD)
	    updated_full_state_dstream = updated_partial_state_dstream.groupByKey().map(lambda x: (x[0], combine_partial_states(x[1])))


	n_processed_states = sc.accumulator(0)
	def count(x):
		global n_processed_states
		n_processed_states += 1
		return True

	results_dstream = updated_full_state_dstream.map(count)
	results_dstream.pprint()

	ssc.start()
	time.sleep(30)
	ssc.stop(stopSparkContext=True, stopGraceFully=False)
	#results_dstream.count().pprint()
	print('Number of states processed: %i' % n_processed_states.value)
	return n_processed_states.value



alpha = [1, 2, 4, 8, 16, 20, 24, 28, 32, 36, 40, 48, 54, 60, 64, 70, 75, 80, 90, 100, 110, 128]

results = list()
for i in range(len(alpha)):
	results.append(evaluate(n_cores=alpha[i]))
	print(results)


print('Finished')
