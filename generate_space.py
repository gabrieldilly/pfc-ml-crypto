from os import listdir
from os.path import isfile, join, isdir
from shutil import copyfile, copytree, rmtree
import time
import pandas as pd
import numpy as np

#%%
#Generating vectors

mypath = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\encrypted_documents"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

block_size = [2,4]
complete_dict = {n: [] for n in block_size}
partial_dict = {n: {f: [] for f in onlyfiles} for n in block_size}

start_time = time.time()

for f in onlyfiles:
    with open(mypath + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        for n in block_size:
            for i in range(0, len(data), n):
                if data[i:min(i+n,len(data))] not in complete_dict[n] and len(data[i:min(i+n,len(data))])==n:
                    complete_dict[n].append(data[i:min(i+n,len(data))])
                if data[i:min(i+n,len(data))] not in partial_dict[n][f] and len(data[i:min(i+n,len(data))])==n:
                    partial_dict[n][f].append(data[i:min(i+n,len(data))])
    print("file completed")
	
vector_space = {n: {f: [0]*len(complete_dict[n]) for f in onlyfiles} for n in block_size}
                    
for f in onlyfiles:
    for n in block_size:
        for b in complete_dict[n]:
            if b in partial_dict[n][f]:
                vector_space[n][f][complete_dict[n].index(b)] = 1

print(f'Finished. Elapsed time: {time.time() - start_time}')


#%%
# Angulo Cosseno

df = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df[f1][f2] = 0
		
def cos(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return d/(np.sqrt(n1*n2))

start_time = time.time()

for n in block_size:
    for f1, u in vector_space[n].items():
        for f2, v in vector_space[n].items():
            df[f1][f2] = cos(u,v)

print(f'Finished. Cos Elapsed time: {time.time() - start_time}')