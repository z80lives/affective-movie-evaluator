import numpy as np
from matplotlib import pyplot as plt

ts = np.load("data/33cd9a03-acf3-4b36-8ebc-6937f066196d/output.npy")

x = ts[:,0]
y = ts[:,1]

plt.plot(x,y)
plt.show()
