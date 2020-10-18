from binascii import hexlify
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from metrics import *

#%%
#Generating vectors

def generate_space_8_16(B, path):
    
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    vector_space = {f: [0]*int(pow(16,int(int(B)/4))) for f in onlyfiles}

    start_time = time.time()
    count = 1

    for f in onlyfiles:
        with open(path + "\\" + f, 'r') as file:
            data = file.read().replace('\n', '')
            for i in range(0, len(data), int(int(B)/4)):
                vector_space[f][int(data[i:min(i+int(int(B)/4),len(data))],16)] += 1
        print(str(count) + " - " + f + " completed")
        count+=1

    print(f'Finished. Elapsed time: {time.time() - start_time}')
    return vector_space

def generate_space_32_64(B, path):
    
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    vector_space = {f: {} for f in onlyfiles}

    start_time = time.time()
    count = 1

    for f in onlyfiles:
        with open(path + "\\" + f, 'r') as file:
            data = file.read().replace('\n', '')
            for i in range(0, len(data), int(int(B)/4)):
                if data[i:min(i+int(int(B)/4),len(data))] not in [*vector_space[f]]:
                    vector_space[f][data[i:min(i+int(int(B)/4),len(data))]] = 1
                else:
                    vector_space[f][data[i:min(i+int(int(B)/4),len(data))]]+=1
        print(str(count) + " - " + f + " completed")
        count+=1

    print(f'Finished. Elapsed time: {time.time() - start_time}')

    return vector_space

#%%
# Generate Metric

def generate_metric(n, vector_space, B, src_path, dest_path):
    onlyfiles = [f for f in listdir(src_path) if isfile(join(src_path, f))]
    df = pd.DataFrame(index=[f for f in onlyfiles], columns=[f for f in onlyfiles])

    for f1 in onlyfiles:
        for f2 in onlyfiles: 
            df[f1][f2] = 0

    start_time = time.time()

    for f1 in [*vector_space]:
        for f2 in [*vector_space][[*vector_space].index(f1):]:
            if f1 == f2:
                df[f2][f1] = 1
                continue
            if n==1:
                df[f2][f1] = cos(B, vector_space[f1],vector_space[f2])
            if n==2:
                df[f2][f1] = simple_matching(B, vector_space[f1],vector_space[f2])
            if n==3:
                df[f2][f1] = dice(B, vector_space[f1],vector_space[f2])
            if n==4:
                df[f2][f1] = jaccard(B, vector_space[f1],vector_space[f2])
            if n==5:
                df[f2][f1] = euclidian_distance(B, vector_space[f1],vector_space[f2])
            if n==6:
                df[f2][f1] = manhattan_distance(B, vector_space[f1],vector_space[f2])
            if n==7:
                df[f2][f1] = canberra_distance(B, vector_space[f1],vector_space[f2])

    df.to_csv(dest_path + "\\" + metric_names[n-1] + " - " + str(B) + " bits.csv", sep = ';')

    print("\nMedida " +  metric_names[n-1] + " finalizada!")

    print(f'Finished. Elapsed time: {time.time() - start_time}')
    return df

#%%
#Interface

print("\nInsira o caminho da pasta com os documentos de treino criptografados:")
print("(Recomenda-se colocar igual quantidade de documentos com cada algoritmo, todos de mesmo tamanho, em torno de 500 KB)\n")
path1 = input()
path1 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

print("\nInsira o tamanho de palavra a ser usado na geração do espaço de vetores:\n")
print("(8, 16, 32 ou 64 bits)")
B = input()

print('\nGerando o espaço de palavras...\n')

if int(B)==8 or int(B)==16:
    vector_space = generate_space_8_16(B, path1)

if int(B)==32 or int(B)==64:
    vector_space = generate_space_32_64(B, path1)

print('\nPronto! Espaço gerado!\n')

print("\nInsira o caminho de destino para as tabelas de medidas de similaridade e dissimilaridade:\n")
path2 = input()
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Medidas"

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

df1 = generate_metric(1, vector_space, B, path1, path2)
df2 = generate_metric(2, vector_space, B, path1, path2)
df3 = generate_metric(3, vector_space, B, path1, path2)
df4 = generate_metric(4, vector_space, B, path1, path2)
df5 = generate_metric(5, vector_space, B, path1, path2)
df6 = generate_metric(6, vector_space, B, path1, path2)
df7 = generate_metric(7, vector_space, B, path1, path2)

print('\nPronto! Medidas calculadas!\n')

print("\nInsira o caminho da pasta com os documentos de teste criptografados:")
print("(Recomenda-se colocar igual quantidade de documentos com cada algoritmo, todos de mesmo tamanho, em torno de 500 KB)\n")
path3 = input()

print("\nInsira o caminho de destino para os resultados do modelo para identificar os algoritmos criptográficos:\n")
path4 = input()
path4 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Resultados"

print('\nGerando o modelo...\n')