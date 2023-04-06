#!/usr/bin/env python3

import Image
import pickle
import matplotlib.pyplot as plt
from mpi4py import MPI
import math

# ENTER THE DEGREE OF RESOLUTION  #
n = 4
# !IMPORTANT! Use np= n*n + 2 here #
# -------------------------------  #

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

w, h = 1000, 1000
maxIter = 200
#cX, cY = -0.8696, 0.26
cX, cY = -0.40779853277402167, 0.6082356466183947

moveX, moveY = -1.5, -1
order = 2
for a in range(n*n):
    if rank == a:
        zoom = n-1
        bitmap = Image.new("RGB", (w, h), "white")
        pix1 = bitmap.load()
        for x in range(w):
            for y in range(h):
                zx = 1.5*(x - w/2)/(0.5*zoom*w) + moveX
                zy = 1.0*(y - h/2)/(0.5*zoom*h) + moveY
                i = maxIter
                while abs(zx*zx + zy*zy) < 4 and i > 1:
                    tmp = abs((zx*zx - zy*zy))**(order/2)*(math.cos(order*math.atan2(zy, zx))) + cX
                    zy,zx = abs((zx*zx - zy*zy))**(order/2)*(math.sin(order*math.atan2(zy, zx))), tmp
                    i -= 1
                pix1[x,y] = (i << 21) + (i << 10) + i*8
        plt.axis('off')
        plt.imshow(bitmap, extent=[-2.0, 2.0, -1.5, 1.5])
        # plt.savefig('bitmap'+str(a)+'.jpeg', bbox_inches='tight', pad_inches=0)
        comm.send(bitmap, dest=(n*n+1), tag=a)
        print("Object {0} sent".format(a+1))
        print("Rank "+str(a)+" finished job")

    if moveX < 1.5:
        moveX = moveX + (3/(n-1))
    elif moveX == 1.5:
        moveX = -1.5
        moveY = moveY + (2/(n-1))
    elif moveY == 2:
        exit()

if rank == (n*n + 1):
    items = []
    for x in range(n*n):
        items.append(comm.recv(source=x, tag=x))
        print("Object {0} received".format(x+1))
    img = items[0]
    (width, height) = img.size
    (pro_width, pro_height) = (width*n, height*n)
    result = Image.new('RGB', (pro_width, pro_height))
    a = 0
    b = 0
    for x in range(n*n):
        img = items[x]
        result.paste(im=img, box=(a, b))
        if a < (pro_width-width):
            a = a + width
        elif a == (pro_width-width):
            a = 0
            b = b + height
    result.show()
#bitmap(-0.40779853277402167,0.6082356466183947,)
