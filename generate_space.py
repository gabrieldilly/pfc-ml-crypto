from os import listdir
from os.path import isfile, join, isdir
from shutil import copyfile, copytree, rmtree
import time

mypath = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\encrypted_documents"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

block_size = [4] #2,4
complete_dict = {n: [] for n in block_size}
partial_dict = {n: {f: [] for f in onlyfiles} for n in block_size}

start_time = time.time()

for f in onlyfiles:
    with open(mypath + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        for n in block_size:			   
            for i in range(0, len(data), n):
                if data[i:min(i+n,len(data))] not in complete_dict[n] and len(data[i:min(i+n,len(data))])>=n:
                    complete_dict[n].append(data[i:min(i+n,len(data))])
                    partial_dict[n][f].append(data[i:min(i+n,len(data))])
    print("file completed")
	
vector_space = {n: {f: [0]*len(complete_dict[n]) for f in onlyfiles} for n in block_size}
                    
for f in onlyfiles:
    for n in block_size:
        for b in complete_dict[n]:
            if b in partial_dict[f]:
                vector_space[n][f][complete_dict[n].find(b)] = 1

print(f'Finished. Elapsed time: {time.time() - start_time}')

#%%
# Angulo Cosseno
