from os import listdir
from os.path import isfile, join
import time
import pandas as pd
import numpy as np

#%%
#Parameters

# Cryptographed files path 
path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

# Metric Tables destination
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\"

# Word size
b = 16

# Chosen metrics


#%%
#Generating vectors

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

vector_space = {f: [] for f in onlyfiles}

start_time = time.time()

count = 1

for f in onlyfiles:
    with open(path + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        for i in range(0, len(data), b):
            if data[i:min(i+b,len(data))] not in vector_space[f]:
                vector_space[f].append(data[i:min(i+b,len(data))])
                vector_space[f].append(0)
            else:
                vector_space[f][vector_space[f].index(data[i:min(i+b,len(data))])+1]+=1
    print(str(count) + " - " + f + " completed")
    count+=1
	
with open(path2 + "vector_space_" + str(4*b) + ".txt", "w") as text_file:
    for f in onlyfiles:
        for i in vector_space[f]:
            print(str(i) + ",", file=text_file, end='')
        print('\n', file=text_file, end='')

print(f'Finished. Elapsed time: {time.time() - start_time}')

#%%
# Useful functions

def norm(u):   

    v = []

    for i in range(0,int(len(u)/2)):
        v.append(u[2*i+1])
		
    return np.linalg.norm(v)

def inner(u,v):

    x = []
    y = []

    for i in range(0,int(len(u)/2)):
        x.append(u[2*i])

    for i in range(0,int(len(v)/2)):
        y.append(v[2*i])
    
    val = 0

    for i in x:
        for j in y:
            if i == j:
                val+=u[u.index(i)+1]*v[v.index(j)+1]

    return val

#%%
# Angulo Cosseno

df1 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df1[f1][f2] = 0

def cos(u,v):
    
    n1 = norm(u)
    n2 = norm(v)
    d = inner(u,v)
    
    return d/(n1*n2)
		
start_time = time.time()

for f1 in [*vector_space]:
    for f2 in [*vector_space][[*vector_space].index(f1):]:
        if f1 == f2:
            df1[f2][f1] = 1
            print('cos(' + f1 + ', ' + f2 + ') finished')
            continue
        df1[f2][f1] = cos(vector_space[f1],vector_space[f2])
        print('cos(' + f1 + ', ' + f2 + ') finished')

df1.to_csv(path2 + "Angulo_Cosseno_" + str(4*b) + ".csv", sep = ';')

print(f'Finished. Cos Elapsed time: {time.time() - start_time}')

#%%
# Euclidian Distance

df2 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df2[f1][f2] = 0
		
start_time = time.time()

def euclidian_distance(u,v):   

    x = []
    y = []

    for i in range(0,int(len(u)/2)):
        x.append(u[2*i])

    for i in range(0,int(len(v)/2)):
        y.append(v[2*i])

    val = []

    for i in x:
        for j in y:
            if i == j:
                val.append(u[u.index(i)+1]-v[v.index(j)+1])
		
    return np.linalg.norm(val)

for f1 in [*vector_space]:
    for f2 in [*vector_space][[*vector_space].index(f1):]:
        if f1 == f2:
            df2[f2][f1] = 1
            print('cos(' + f1 + ', ' + f2 + ') finished')
            continue
        df2[f2][f1] = euclidian_distance(vector_space[f1],vector_space[f2])
        print('euclidian_distance(' + f1 + ', ' + f2 + ') finished')

df2.to_csv(path2 + "Distancia_Euclidiana_" + str(4*b) + ".csv", sep = ';')
	
print(f'Finished. Euclidian Distance Elapsed time: {time.time() - start_time}')

#%%
# Dice Coefficient
df3 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df3[f1][f2] = 0
		
def dice(u,v):
	
    n1 = norm(u)
    n2 = norm(v)
    d = inner(u,v)
    
    return 2*d/(n1*n1+n2*n2)

start_time = time.time()

for f1 in [*vector_space]:
    for f2 in [*vector_space][[*vector_space].index(f1):]:
        if f1 == f2:
            df2[f2][f1] = 1
            print('cos(' + f1 + ', ' + f2 + ') finished')
            continue
        df2[f2][f1] = dice(vector_space[f1],vector_space[f2])
        print('dice(' + f1 + ', ' + f2 + ') finished')

df3.to_csv(path2 + "Coeficiente_Dice_" + str(4*b) + ".csv", sep = ';')

print(f'Finished. Dice Elapsed time: {time.time() - start_time}')
