# Parallel Code
import numpy as np
import matplotlib.pyplot as plt
import timeit
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print("Size is: " + str(size))
a = 40
def mandelbrot(c,n):
    z = 0
    n3 = np.empty_like(c)
    n4 = np.empty_like(c)
    for i in range(n):
        #Keep ONLY one of the Generalized function's below of reader's choice. One can
        #Constuct functions of one's choice if needed
        # n3 = np.divide(n3 - np.full((width, height), a), np.full((width, height), 1) - np.full((width, height), a)*n3)*np.divide(n3 - np.full((width, height), a), np.full((width, height), 1) - np.full((width, height), a)*n3) + r3
        # n3 = np.sin(n3)*np.cosh(n3)*np.sin(n3)*np.cosh(n3) + r3
        n3 = np.exp(n3)*np.exp(n3) + c
        # n3 = n3*n3 + c
        n4[np.where(np.abs(n3) > 2)] = i
        n3[np.where(np.abs(n3) > 2)] = np.nan
    return n4


if rank == 0:
    start = timeit.default_timer()
    n_mtx = np.empty((0, a*100))
    for proc in range(1, size, 1):
        n_mtx = np.vstack((n_mtx, comm.recv(source=proc)))
    stop = timeit.default_timer()
    print('Time taken for a=', a, ' : ', stop - start, ' seconds')
    plt.imshow(np.abs(n_mtx), cmap='hot')
    plt.axis('off')
    plt.show()

if rank != 0:
    x = np.linspace(-2, 1, 100 * a)
    y = np.linspace(-1.5 + 2*(rank-1)*(1.5/(size-1)), -1.5 + 2*rank*(1.5/(size-1)), 100*(a//size))
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    M = mandelbrot(Z, 100)
    comm.send(M, dest=0)