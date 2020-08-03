from os import listdir
from os.path import isfile, join
import time
import pandas as pd
import numpy as np

path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\encrypted_documents"
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\"

#%%
#Generating vectors

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

block_size = [8] #4,8
complete_dict = {n: [] for n in block_size}
partial_dict = {n: {f: [] for f in onlyfiles} for n in block_size}

start_time = time.time()

count = 1

for f in onlyfiles:
    with open(path + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        for n in block_size:
            for i in range(0, len(data), n):
                if data[i:min(i+n,len(data))] not in complete_dict[n] and len(data[i:min(i+n,len(data))])==n:
                    complete_dict[n].append(data[i:min(i+n,len(data))])
                if data[i:min(i+n,len(data))] not in partial_dict[n][f] and len(data[i:min(i+n,len(data))])==n:
                    partial_dict[n][f].append(data[i:min(i+n,len(data))])
    print(str(count) + " - file completed")
    count+=1
	
vector_space = {n: {f: [0]*len(complete_dict[n]) for f in onlyfiles} for n in block_size}
                    
for f in onlyfiles:
    for n in block_size:
        for b in complete_dict[n]:
            if b in partial_dict[n][f]:
                vector_space[n][f][complete_dict[n].index(b)] = 1

for n in block_size:	 
    with open(path2 + "vector_space_" + str(n) + ".txt", "w") as text_file:
        for f in onlyfiles:
            for i in vector_space[n][f]:
                print(str(i), file=text_file, end='')
            print('\n', file=text_file, end='')  

print(f'Finished. Elapsed time: {time.time() - start_time}')

#%%
# Angulo Cosseno

df = {n: pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles]) for n in block_size}

for n in block_size:
    for f1 in onlyfiles:
        for f2 in onlyfiles: 
            df[n][f1][f2] = 0
		
def cos(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return d/(n1*n2)

start_time = time.time()

for n in block_size:
    for f1, u in vector_space[n].items():
        for f2, v in vector_space[n].items():
            df[n][f1][f2] = cos(u,v)

for n in block_size:
    df[n].to_csv(path2 + "Angulo_Cosseno_" + str(n) + ".csv", sep = ';')

print(f'Finished. Cos Elapsed time: {time.time() - start_time}')
      				
#%%
# Euclidian Distance

df2 = {n: pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles]) for n in block_size}

for n in block_size:
    for f1 in onlyfiles:
        for f2 in onlyfiles: 
            df2[n][f1][f2] = 0
		
start_time = time.time()

for n in block_size:
    for f1, u in vector_space[n].items():
        for f2, v in vector_space[n].items():
            u = np.array(u, dtype='i4')
            v = np.array(v, dtype='i4')
            df2[n][f1][f2] = np.linalg.norm(u-v)

for n in block_size:
    df2[n].to_csv(path2 + "Distancia_Euclidiana_" + str(n) + ".csv", sep = ';')
	
print(f'Finished. Euclidian Distance Elapsed time: {time.time() - start_time}')