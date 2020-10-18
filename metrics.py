from binascii import hexlify
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

#%%
# Auxiliar functions for 32 and 64 bits

def norm(u):   

    v = []

    for i in [*u]:
        v.append(u[i])
		
    return np.linalg.norm(v)

def inner(u,v):

    val = 0

    for i in [*u]:
        for j in [*v]:
            if i == j:
                val+=u[i]*v[j]

    return val

#%%
# Metrics

metric_names = ['Cosseno', 'Simple-Matching', 'Dice', 'Jaccard', 'Euclidian', 'Manhattan', 'Canberra']

# Angulo Cosseno
def cos(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)
        
        n1 = np.linalg.norm(u)
        n2 = np.linalg.norm(v)
        d = np.inner(u,v)
        
        return d/(n1*n2)

    if B==32 or B==64:
        n1 = norm(u)
        n2 = norm(v)
        d = inner(u,v)
    
        return d/(n1*n2)

# Simple-Matching Coefficient
def simple_matching(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)

        return np.inner(u,v)
    
    if B==32 or B==64:
        return inner(u,v)

# Dice Coefficient
def dice(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)
        
        n1 = np.linalg.norm(u)
        n2 = np.linalg.norm(v)
        d = np.inner(u,v)
        
        return 2*d/(n1*n1+n2*n2)
    
    if B==32 or B==64:
        n1 = norm(u)
        n2 = norm(v)
        d = inner(u,v)
        
        return 2*d/(n1*n1+n2*n2)


# Jaccard Coefficient
def jaccard(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)

        n1 = np.linalg.norm(u)
        n2 = np.linalg.norm(v)

        return (np.inner(u,v))/(n1*n1 + n2*n2 - np.inner(u,v))
    
    if B==32 or B==64:
        n1 = norm(u)
        n2 = norm(v)

        return (inner(u,v))/(n1*n1 + n2*n2 - inner(u,v))


# Euclidian Distance
def euclidian_distance(B,u,v):
    if B==8 or B==16:
        u = np.array(u, dtype='i4')
        v = np.array(v, dtype='i4')
        
        return np.linalg.norm(u-v)
    
    if B==32 or B==64:
        val = []

        for i in [*u]:
            if i in [*v]:
                val.append(u[i]-v[i])
            else:
                val.append(u[i])		

        for i in [*v]:
            if i not in [*u]:
                val.append(v[i])

        return np.linalg.norm(val)


# Manhattan Distance
def manhattan_distance(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)
        res = 0

        for i in range(0, len(u)):
            res = res + abs(u[i]-v[i])
        
        return res

    if B==32 or B==64:
        val = []
        res = 0

        for i in [*u]:
            if i in [*v]:
                val.append(abs(u[i]-v[i]))
            else:
                val.append(abs(u[i]))		

        for i in [*v]:
            if i not in [*u]:
                val.append(abs(v[i]))
        
        for i in range (0, len(val)):
            res = res + val[i]
        
        return res


# Canberra Distance
def canberra_distance(B,u,v):
    if B==8 or B==16:
        u = np.array(u)
        v = np.array(v)
        res = 0

        for i in range(0, len(u)):
            res = res + abs(u[i]-v[i])/(abs(u[i])+abs(v[i]))
        
        return res

    if B==32 or B==64:
        val = []
        res = 0

        for i in [*u]:
            if i in [*v]:
                val.append(abs(u[i]-v[i])/(abs(u[i])+abs(v[i])))
            else:
                val.append(1)

        for i in [*v]:
            if i not in [*u]:
                val.append(1)
        
        for i in range (0, len(val)):
            res = res + val[i]
        
        return res
