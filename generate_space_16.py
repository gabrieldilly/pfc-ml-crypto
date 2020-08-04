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

vector_space = {f: [0]*int(pow(16,4)) for f in onlyfiles}

start_time = time.time()

count = 1

for f in onlyfiles:
    with open(path + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        for i in range(0, len(data), 4):
            vector_space[f][int(data[i:min(i+4,len(data))],16)] = 1
    print(str(count) + " - file completed")
    count+=1
	
with open(path2 + "vector_space_" + str(16) + ".txt", "w") as text_file:
    for f in onlyfiles:
        for i in vector_space[f]:
            print(str(i), file=text_file, end='')
        print('\n', file=text_file, end='')

print(f'Finished. Elapsed time: {time.time() - start_time}')

#%%
# Angulo Cosseno

df1 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df1[f1][f2] = 0
		
def cos(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return d/(n1*n2)

start_time = time.time()

for f1, u in vector_space.items():
    for f2, v in vector_space.items():
        df1[f1][f2] = cos(u,v)

df1.to_csv(path2 + "Angulo_Cosseno_" + str(16) + ".csv", sep = ';')

print(f'Finished. Cos Elapsed time: {time.time() - start_time}')

#%%
# Euclidian Distance

df2 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df2[f1][f2] = 0
		
start_time = time.time()

for f1, u in vector_space.items():
    for f2, v in vector_space.items():
        u = np.array(u, dtype='i4')
        v = np.array(v, dtype='i4')
        df2[f1][f2] = np.linalg.norm(u-v)

df2.to_csv(path2 + "Distancia_Euclidiana_" + str(16) + ".csv", sep = ';')
	
print(f'Finished. Euclidian Distance Elapsed time: {time.time() - start_time}')

#%%
# Dice Coefficient
df3 = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

for f1 in onlyfiles:
    for f2 in onlyfiles: 
        df3[f1][f2] = 0
		
def dice(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return 2*d/(n1*n1+n2*n2)

start_time = time.time()

for f1, u in vector_space.items():
    for f2, v in vector_space.items():
        df3[f1][f2] = dice(u,v)

df3.to_csv(path2 + "Coeficiente_Dice_" + str(16) + ".csv", sep = ';')

print(f'Finished. Dice Elapsed time: {time.time() - start_time}')