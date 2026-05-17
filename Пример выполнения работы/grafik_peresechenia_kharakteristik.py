import matplotlib.pyplot as plt
import numpy as np
import math

g = [0, -0.25, -0.5, -0.75, -1.0, -1.5, -2]
h = [0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3]
for x0 in g:
    for t0 in h:
        k1 = 2*(1+x0*x0)/(1+(1+(1+x0*x0)*(1+x0*x0))*(1+(1+x0*x0)*(1+x0*x0)))
        k2 = 2*math.exp(-t0)/(2+2*math.exp(-2*t0)+math.exp(-4*t0))
        t1 = np.arange(0, 3, 0.001)
        t2 = np.arange(0, 3, 0.001)
        x1 = x0 - t1*k1
        x2 = -(t2-t0)*k2
        plt.plot(t1, x1)
        plt.plot(t2, x2)
plt.ylim(-2.5, 0)
plt.xlim(0, 3)
plt.xlabel("t")
plt.ylabel("x")
plt.show()