# Numpy Code
import numpy as np
import matplotlib.pyplot as plt
import timeit
start1 = timeit.default_timer()

def mandelbrot(c,n):
    z = 0
    n3 = np.empty_like(c)
    n4 = np.empty_like(c, dtype=np.float)
    for i in range(n):
        #Keep ONLY one of the Generalized function's below of reader's choice. One can
        #constuct functions of one's choice if needed
        # n3 = np.divide(n3 - np.full((width, height), a), np.full((width, height), 1) - np.full((width, height), a)*n3)*np.divide(n3 - np.full((width, height), a), np.full((width, height), 1) - np.full((width, height), a)*n3) + r3
        # n3 = np.sin(n3)*np.cosh(n3)*np.sin(n3)*np.cosh(n3) + r3
        n3 = np.sin(n3)*np.exp(-n3)*np.sin(n3)*np.exp(-n3) + c
        # n3 = n3*n3 + c
        n4[np.where(np.abs(n3) <= 2)] = i
        n3[np.where(np.abs(n3) > 2)] = np.nan
    return n4
# x = range(1,21,1)
# for a in x:
a=20
end1 = timeit.default_timer()
print('Time taken for Minor a=', a, ' : ',end1 - start1, ' seconds')
start = timeit.default_timer()
x = np.linspace(-2, 1, 100*a)
y = np.linspace(-1.5, 1.5, 100*a)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y
x = range(0, a*100, 1)
M = mandelbrot(Z ,100)
stop = timeit.default_timer()
print('Time taken for Major a=', a, ' : ',stop - start,' seconds')
#Plot the mandelbrot set
plt.imshow(M, cmap='plasma')
plt.axis('off')
plt.show()