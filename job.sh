#!/bin/sh -l

#PBS -l walltime=20:00:00
#PBS -l nodes=1:ppn=8
#PBS -l mem=4gb
#PBS -l file=1gb
#PBS -N bigdata
#PBS -o bigdata.out
#PBS -e bigdata.err

# Load Python and python modules
module purge
module load Spark/2.2.0-intel-2017b-Hadoop-2.6-Java-1.8.0_152-Python-3.6.3

# Move to project folder
cd $HOME/HGF

# Run
python main.py
