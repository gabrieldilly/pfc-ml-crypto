from binascii import hexlify
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from metrics import *
from support_vector_machine import *

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

print("\nInsira o caminho da pasta com os documentos de treino e teste criptografados:\n")
print("- Recomenda-se colocar igual quantidade de documentos com cada algoritmo, todos de mesmo tamanho, em torno de 500 KB;")
print("- Escreva no padrão:")
print("    * Exemplos documentos de treino: RSA_doc_11.txt, DES_doc_13.txt, ElGamal_doc_33.txt;")
print("    * Exemplos documentos de teste: test_doc_1.txt, test_doc_5.txt, test_doc_33.txt.")

path1 = input()
path1 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

print("\nInsira o tamanho de palavra a ser usado na geração do espaço de vetores (8, 16, 32 ou 64 bits):")
B = input()

print('\nGerando o espaço de palavras...\n')

if int(B)==8 or int(B)==16:
    vector_space = generate_space_8_16(B, path1)

if int(B)==32 or int(B)==64:
    vector_space = generate_space_32_64(B, path1)

print('\nPronto! Espaço gerado!\n')

print("\nInsira o caminho de destino para as tabelas de medidas de similaridade e dissimilaridade:")
path2 = input()
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Medidas"

print("\nEscreva o número das medidas que deseja usar (aperte 0 para terminar):\n")

print("1 - Ângulo Cosseno")
print("2 - Coeficiente Simple-Matching")
print("3 - Coeficiente Dice")
print("4 - Coeficiente Jaccard")
print("5 - Distância Euclidiana")
print("6 - Distância Manhattan")
print("7 - Distância Canberra\n")

selected_metrics = {}
choice = ''
metric_list = []
dfs = {}

while True:
    choice = input()
    if choice == '' or int(choice) == 0:
        break
    metric_list.append(int(choice))        
    selected_metrics[metric_names[int(choice) - 1]] = B

print('\nCalculando as medidas...\n')

for m in metric_list:
    dfs[metric_names[m - 1] + ' - ' + str(B) + ' bits'] = generate_metric(m, vector_space, B, path1, path2)

print('\nPronto! Medidas calculadas!\n')

print("\nInsira o caminho de destino para os resultados do modelo para identificar os algoritmos criptográficos:")
path3 = input()
path3 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Resultados"

print('\nGerando o modelo...\n')

generate_model(dfs, selected_metrics, 'DES', [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0])
generate_model(dfs, selected_metrics, 'ElGamal',[0,0,1,0,0,1,0,0,1,0,0,1,0,0,1])
generate_model(dfs, selected_metrics, 'RSA', [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0])





