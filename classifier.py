from binascii import hexlify
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from datetime import datetime
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
print("    * Exemplos documentos de teste: test_doc_01.txt, test_doc_05.txt, test_doc_33.txt.")

path1 = input()
path1 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

print("\nInsira o tamanho de palavra a ser usado na geração do espaço de vetores (8, 16, 32 ou 64 bits):")
# B = input()
B = 8

print('\nGerando o espaço de palavras...\n')

# if int(B)==8 or int(B)==16:
#     vector_space = generate_space_8_16(B, path1)

# if int(B)==32 or int(B)==64:
#     vector_space = generate_space_32_64(B, path1)

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

selected_metrics = {}
choice = ''
metric_list = []
dfs = {}

# while True:
#     choice = input()
#     if choice == '' or int(choice) == 0:
#         break
#     metric_list.append(int(choice))
#     selected_metrics[metric_names[int(choice) - 1]] = B

print('\nCalculando as medidas...\n')

# for m in metric_list:
#     dfs[metric_names[m - 1] + ' - ' + str(B) + ' bits'] = generate_metric(m, vector_space, B, path1, path2)

def format_df(df):
    df['document'] = df.index
    df['document'] = df['document'].apply(lambda x: x.replace('.txt', ''))
    df.columns = [c.replace('.txt', '') for c in df.columns]
    df = df.set_index('document')
    df = df + df.T
    for i in range(0, df.shape[0]):
        df.iloc[i, i] = 1 if df.iloc[i, i] == 2 else df.iloc[i, i]
    df['document'] = df.index
    return df
    
df_committee = format_df(df_committee)

# for m in metric_list:
#     dfs[metric_names[m - 1] + ' - ' + str(B) + ' bits'] = pd.read_csv(metric_path + metric_names[m - 1] + ' - ' + str(B) + ' bits.csv', delimiter = ';')

print('\nPronto! Medidas calculadas!\n')

import pickle
# # Saving the objects:
# with open(B + 'bits.pkl', 'wb') as f:
#     pickle.dump([selected_metrics, dfs], f)
# Getting back the objects:
with open(B + 'bits.pkl', 'rb') as f:
    selected_metrics, dfs = pickle.load(f)

# Euclidian_Distance for committee
df_committee = dfs['Euclidian - ' + str(B) + ' bits']

print('\nGerando o modelo...\n')


pairs = [
    {
        'Cosseno': B,
        'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        'Cosseno': B,
        # 'Simple-Matching': B,
        'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        'Simple-Matching': B,
        'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        'Simple-Matching': B,
        # 'Dice': B,
        'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        'Dice': B,
        'Jaccard': B,
        # 'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        'Dice': B,
        # 'Jaccard': B,
        'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        'Dice': B,
        # 'Jaccard': B,
        # 'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        'Jaccard': B,
        'Euclidian': B,
        # 'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        'Jaccard': B,
        # 'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    }, {
        # 'Cosseno': B,
        # 'Simple-Matching': B,
        # 'Dice': B,
        # 'Jaccard': B,
        'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    }, {
        'Cosseno': B,
    }, {
        'Simple-Matching': B,
    }, {
        'Dice': B,
    }, {
        'Jaccard': B,
    }, {
        'Euclidian': B,
    }, {
        'Manhattan': B,
    }, {
    #     'Canberra': B,
    # }, {
        'Cosseno': B,
        'Simple-Matching': B,
        'Dice': B,
        'Jaccard': B,
        'Euclidian': B,
        'Manhattan': B,
        # 'Canberra': B,
    # }, {
    #     'Cosseno': B,
    #     'Simple-Matching': B,
    #     'Dice': B,
    #     'Jaccard': B,
    #     'Euclidian': B,
    #     'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     'Cosseno': B,
    #     # 'Simple-Matching': B,
    #     # 'Dice': B,
    #     # 'Jaccard': B,
    #     # 'Euclidian': B,
    #     # 'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     # 'Cosseno': B,
    #     'Simple-Matching': B,
    #     # 'Dice': B,
    #     # 'Jaccard': B,
    #     # 'Euclidian': B,
    #     # 'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     # 'Cosseno': B,
    #     # 'Simple-Matching': B,
    #     'Dice': B,
    #     # 'Jaccard': B,
    #     # 'Euclidian': B,
    #     # 'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     # 'Cosseno': B,
    #     # 'Simple-Matching': B,
    #     # 'Dice': B,
    #     'Jaccard': B,
    #     # 'Euclidian': B,
    #     # 'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     # 'Cosseno': B,
    #     # 'Simple-Matching': B,
    #     # 'Dice': B,
    #     # 'Jaccard': B,
    #     'Euclidian': B,
    #     # 'Manhattan': B,
    #     'Canberra': B,
    # }, {
    #     # 'Cosseno': B,
    #     # 'Simple-Matching': B,
    #     # 'Dice': B,
    #     # 'Jaccard': B,
    #     # 'Euclidian': B,
    #     'Manhattan': B,
    #     'Canberra': B,
    }]

train_sizes = np.arange(start = 10, stop = 81, step = 10)

for selected_metrics in pairs:
    for train_size in train_sizes:
    
        # Evaluating model
        resp_des = []
        resp_rsa = []
        resp_elgamal = []
        
        count_tests = 0
        onlyfiles = [f for f in listdir(path1) if isfile(join(path1, f))]
        for f in onlyfiles:
            if 'test' in f:
                count_tests+=1
        
        for i in range(0,count_tests):
            if i<20:
                resp_des.append(1)
                resp_rsa.append(0)
                resp_elgamal.append(0)
            if i>=20 and i<40:
                resp_des.append(0)
                resp_rsa.append(1)
                resp_elgamal.append(0)
            if i>=40:
                resp_des.append(0)
                resp_rsa.append(0)
                resp_elgamal.append(1)
        
        pred_des, accuracy_des, cm_des = generate_model(dfs, selected_metrics, 'DES', resp_des, train_size)
        pred_rsa, accuracy_rsa, cm_rsa = generate_model(dfs, selected_metrics, 'RSA', resp_rsa, train_size)
        pred_elgamal, accuracy_elgamal, cm_elgamal = generate_model(dfs, selected_metrics, 'ElGamal', resp_elgamal, train_size)
        
        # Committee
        des_result = []
        rsa_result = []
        elgamal_result = []
        
        for i in range(0, count_tests):
            if pred_des[i] + pred_rsa[i] + pred_elgamal[i] <= 1:
                des_result.append(pred_des[i])
                rsa_result.append(pred_rsa[i])
                elgamal_result.append(pred_elgamal[i])
            else:
                row = df_committee[df_committee.index == 'test_doc_' + (('0'+str(i+1)) if i+1<10 else str(i+1))].iloc[0]
                des_dist = compute_average(row, 'DES')
                rsa_dist = compute_average(row, 'RSA')
                elgamal_dist = compute_average(row, 'ElGamal')

                dist = float('inf')
                if pred_des[i] == 1 and des_dist < dist:
                    dist = des_dist
                if pred_rsa[i] == 1 and rsa_dist < dist:
                    dist = rsa_dist
                if pred_elgamal[i] == 1 and elgamal_dist < dist:
                    dist = elgamal_dist

                if dist == des_dist:
                    des_result.append(1)
                    rsa_result.append(0)
                    elgamal_result.append(0)
                elif dist == rsa_dist:
                    des_result.append(0)
                    rsa_result.append(1)
                    elgamal_result.append(0)
                elif dist == elgamal_dist:
                    des_result.append(0)
                    rsa_result.append(0)
                    elgamal_result.append(1)
                else:
                    des_result.append(0)
                    rsa_result.append(0)
                    elgamal_result.append(0)
        
        classifier_test = []
        classifier_pred = []
        # evaluating classifier
        for i in range(0, count_tests):
            if resp_des[i] == 1:
                classifier_test.append(1)
            elif resp_rsa[i] == 1:
                classifier_test.append(2)
            elif resp_elgamal[i] == 1:
                classifier_test.append(3)
            else:
                classifier_test.append(0)
                
            if des_result[i] == 1:
                classifier_pred.append(1)
            elif rsa_result[i] == 1:
                classifier_pred.append(2)
            elif elgamal_result[i] == 1:
                classifier_pred.append(3)
            else:
                classifier_pred.append(0)
            
        if len(classifier_test) + len(classifier_pred) != 2 * count_tests:
            print('Erro no tamanho dos vetores de respota do classificador!!')
        
        y_test = classifier_test
        y_pred = classifier_pred
        
        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm_comitee = confusion_matrix(y_test, y_pred)
        print(cm_comitee)
        accuracy_comitee = accuracy_score(y_test, y_pred)
        
        df_accuracy = pd.read_csv('accuracy.csv', sep = ';')
        df_accuracy = df_accuracy.append({
            'selected_metrics': str(selected_metrics),
            'accuracy_des': accuracy_des,
            'accuracy_rsa': accuracy_rsa,
            'accuracy_elgamal': accuracy_elgamal,
            'accuracy_comitee': accuracy_comitee,
            'cm_des': str(cm_des),
            'cm_rsa': str(cm_rsa),
            'cm_elgamal': str(cm_elgamal),
            'cm_comitee': str(cm_comitee),
            'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'train_size': train_size
        }, ignore_index = True)
        df_accuracy.to_csv('accuracy.csv', sep = ';', index = False)
        