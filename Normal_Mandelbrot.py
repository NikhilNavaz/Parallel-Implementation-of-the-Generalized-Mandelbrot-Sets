# Normal Code
import numpy as np
import matplotlib.pyplot as plt
import time


def mandelbrot(c,n):
    z = 0
    for i in range(n):
        z = z**2 + c
        if abs(z) > 2:
            return i
    return n
x = range(1,21,1)
for a in x:
    start = time.time()
    x = np.linspace(-2, 1, 100*a)
    y = np.linspace(-1.5, 1.5, 100*a)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    x = range(0, a*100, 1)
    M = [[mandelbrot(Z[int(i),int(j)],100) for i in x] for j in x]
    stop = time.time()
    print('Time taken for a=', a, ' : ',stop - start,' seconds')
    #Plot the mandelbrot set
    # plt.imshow(M, cmap='hot')
    # plt.axis('off')