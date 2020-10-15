from binascii import hexlify
#from Crypto.Random import get_random_bytes
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

#%%
#Generating vectors

def generate_space_8_16(B, path):
    
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    vector_space = {f: [0]*int(pow(16,int(int(B)/4))) for f in onlyfiles}

    #start_time = time.time()
    count = 1

    for f in onlyfiles:
        with open(path + "\\" + f, 'r') as file:
            data = file.read().replace('\n', '')
            for i in range(0, len(data), int(int(B)/4)):
                vector_space[f][int(data[i:min(i+int(int(B)/4),len(data))],16)] += 1
        print(str(count) + " - " + f + " completed")
        count+=1

    return vector_space
    #print(f'Finished. Elapsed time: {time.time() - start_time}')

#%%
# Metrics

metric_names = ['Cosseno', 'Simple-Matching', 'Dice', 'Jaccard', 'Euclidian', 'Manhattan', 'Canberra']

# Angulo Cosseno
def cos(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return d/(n1*n2)

# Simple-Matching Coefficient
def simple_matching(u,v):
    u = np.array(u)
    v = np.array(v)

    return np.inner(u,v)

# Dice Coefficient
def dice(u,v):
    u = np.array(u)
    v = np.array(v)
    
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    d = np.inner(u,v)
    
    return 2*d/(n1*n1+n2*n2)

# Jaccard Coefficient
def jaccard(u,v):
    u = np.array(u)
    v = np.array(v)

    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)

    return (np.inner(u,v))/(n1*n1 + n2*n2 - np.inner(u,v))

# Euclidian Distance
def euclidian_distance(u,v):
    u = np.array(u, dtype='i4')
    v = np.array(v, dtype='i4')
    
    return np.linalg.norm(u-v)
11
# Manhattan Distance
def manhattan_distance(u,v):
    u = np.array(u)
    v = np.array(v)
    res = 0

    for i in range(0, len(u)):
        res = res + abs(u[i]-v[i])
    
    return res

# Canberra Distance
def canberra_distance(u,v):
    u = np.array(u)
    v = np.array(v)
    res = 0

    for i in range(0, len(u)):
        res = res + abs(u[i]-v[i])/(abs(u[i])+abs(v[i]))
    
    return res

#%%
# Generate Metric

def generate_metric(n, vector_space, B, src_path, dest_path):
    onlyfiles = [f for f in listdir(src_path) if isfile(join(src_path, f))]
    df = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

    for f1 in onlyfiles:
        for f2 in onlyfiles: 
            df[f1][f2] = 0

    for f1 in [*vector_space]:
        for f2 in [*vector_space][[*vector_space].index(f1):]:
            if f1 == f2:
                df[f2][f1] = 1
                continue
            if n==1:
                df[f2][f1] = cos(vector_space[f1],vector_space[f2])
            if n==2:
                df[f2][f1] = simple_matching(vector_space[f1],vector_space[f2])
            if n==3:
                df[f2][f1] = dice(vector_space[f1],vector_space[f2])
            if n==4:
                df[f2][f1] = jaccard(vector_space[f1],vector_space[f2])
            if n==5:
                df[f2][f1] = euclidian_distance(vector_space[f1],vector_space[f2])
            if n==6:
                df[f2][f1] = manhattan_distance(vector_space[f1],vector_space[f2])
            if n==7:
                df[f2][f1] = canberra_distance(vector_space[f1],vector_space[f2])

    df.to_csv(dest_path + "\\" + metric_names[n-1] + " - " str(B) + " bits.csv", sep = ';')

    return df

#%%

print("\nInsira o caminho da pasta com os arquivos criptografados:\n")
path = input()
path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

print("\nInsira o caminho de destino para as tabelas de medidas:\n")
path2 = input()
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Medidas"

print("\nInsira o tamanho de palavra a ser usado na geração do espaço de vetores:\n")
B = input()

print('\nGerando o espaço de palavras...\n')

vector_space = generate_space_8_16(B, path)

print("\nEscreva o número das medidas que deseja usar:\n")
print("1 - Ângulo Coesseno\n")
print("2 - Coeficiente Simple-Matching\n")
print("3 - Coeficiente Dice\n")
print("4 - Coeficiente Jaccard\n")
print("5 - Distância Euclidiana\n")
print("6 - Distância Manhattan\n")
print("7 - Distância Canberra\n")

n = input()
m = input()

print('\nCalculando as medidas...\n')

generate_metric(1, vector_space, B, path, path2)

print('\nPronto! Medidas calculadas!\n')