import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit


xs = [1, 2, 4, 8, 16, 20, 24, 28, 32, 36, 40, 48, 54, 60, 64, 70, 75, 80, 90, 100, 110, 128]
ys = [0, 19748, 23578, 54780, 30432, 64857, 68514, 70124, 80470, 80457, 107563, 120779, 130448, 128089, 145780, 165784, 164668, 169318, 200184, 190317, 227642, 226988] 


LABEL_FONT_SIZE = 20


plt.plot(xs, ys, color='orangered', alpha=0.6)
b, m = polyfit(xs, ys, 1)
xs = np.asarray([np.min(xs), np.max(xs)])
plt.plot(xs, b + m * xs, '--', color='grey')
plt.grid(b=True, which='major', color='#999999', linestyle='--')
plt.ylabel('Number of states processed', fontsize=LABEL_FONT_SIZE)
plt.xlabel('Number of cores', fontsize=LABEL_FONT_SIZE)
plt.savefig('nmodels.png')
plt.show()
