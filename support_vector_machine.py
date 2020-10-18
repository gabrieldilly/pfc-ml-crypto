# Support Vector Machine (SVM)

# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Available datasets
print("\nInsira o caminho com as medidas de similaridade e dissimilaridade:\n")
path = input()

dfs = {}
for file in glob.glob(path + '/*.csv'):
    # key = file.split(' - ')[0]
    key = file.split('\\')[-1].replace('.csv', '')
    dfs[key] = pd.read_csv(file, delimiter = ';')

metric_names = ['Cosseno', 'Simple-Matching', 'Dice', 'Jaccard', 'Euclidian', 'Manhattan', 'Canberra']
    
# df_8b_cos = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'COS')
# df_8b_dice = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'DICE')
# df_8b_ed = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'ED')

# df_16b_cos = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'COS')
# df_16b_dice = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'DICE')
# df_16b_ed = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'ED')

# def get_dataset(df, selected_base):
#     df = df.set_index('Column1')
#     df = df + df.T
#     df = df.replace(2, 1)
#     df = df[[c for c in df.columns if selected_base in c]]
#     df['document'] = df.index
#     df['response'] = df['document'].apply(lambda x: 1 if selected_base in x else 0)
#     return df

def compute_average(row, base):
    s = qtd = 0
    for key, val in row.items():
        if base in key and key != row['document']:
            s += val
            qtd += 1
    return s / qtd

def get_dataset(dfs, selected_base, training_qtd = 12):
    result = pd.DataFrame()
    for s in dfs:
        # df = df.set_index('Column1')
        df = dfs[s]
        df['Unnamed: 0'] = df['Unnamed: 0'].apply(lambda x: x.replace('.txt', ''))
        df.columns = [c.replace('.txt', '') for c in df.columns]
        df = df.set_index('Unnamed: 0')
        df = df + df.T
        df = df.replace(2, 1)
        df = df[[c for c in df.columns if selected_base in c and c in [selected_base + '_doc_' + ('0' if x < 10 else '') + str(x + 1) for x in range(0, training_qtd)]]]
        df['document'] = df.index
        df['response'] = df['document'].apply(lambda x: 1 if selected_base in x else 0)
        df[s] = df.apply(lambda row: compute_average(row, selected_base), axis = 1)
        # df = df[df['document'].apply(lambda c: c not in [selected_base + '_doc_' + str(x + 1) for x in range(0, training_qtd)])]
        if result.empty:
            result = df[['document', 'response', s]].reset_index(drop = True)
        else:
            result = pd.merge(result, df[['document', s]].reset_index(drop = True), how = 'inner', on = 'document')
    return result

#%%
selected_metrics = {
    'Cosseno': 16,
    'Dice': 8
    }
def generate_model(dfs, selected_metrics, selected_base):
    # Importing the dataset
    training_qtd = 40
    test_qtd = 10
    dataset = get_dataset(dfs, selected_base, training_qtd + test_qtd)
    dataset = dataset[['document', 'response'] + [k + ' - ' + str(v) + ' bits' for k, v in selected_metrics.items()]]
    
    df_train = dataset[dataset['document'].apply(lambda c: c.split('_doc_')[1] in [str(x + 1) for x in range(0, training_qtd)])]
    df_test = dataset[dataset['document'].apply(lambda c: c.split('_doc_')[1] not in [str(x + 1) for x in range(0, training_qtd)])]
    X = dataset.iloc[:, 2:].values
    y = dataset.iloc[:, 1].values
    
    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
    X_train, X_test = df_train.iloc[:, 2:].values, df_test.iloc[:, 2:].values
    y_train, y_test = df_train.iloc[:, 1].values, df_test.iloc[:, 1].values
    # print(X_train)
    # print(y_train)
    # print(X_test)
    # print(y_test)
    
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    # print(X_train)
    # print(X_test)
    
    # Training the SVM model on the Training set
    from sklearn.svm import SVC
    classifier = SVC(kernel = 'linear', random_state = 0)
    classifier.fit(X_train, y_train)
    
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
    print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))
    
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy_score(y_test, y_pred)
    
#%%
generate_model(df_8b_cos, 'DES')
generate_model(df_8b_dice, 'DES')
generate_model(df_8b_ed, 'DES')

generate_model(df_16b_cos, 'DES')
generate_model(df_16b_dice, 'DES')
generate_model(df_16b_ed, 'DES')

generate_model(df_8b_cos, 'RSA')
generate_model(df_8b_dice, 'RSA')
generate_model(df_8b_ed, 'RSA')

generate_model(df_16b_cos, 'RSA')
generate_model(df_16b_dice, 'RSA')
generate_model(df_16b_ed, 'RSA')

generate_model(df_8b_cos, 'ElGamal')
generate_model(df_8b_dice, 'ElGamal')
generate_model(df_8b_ed, 'ElGamal')

generate_model(df_16b_cos, 'ElGamal')
generate_model(df_16b_dice, 'ElGamal')
generate_model(df_16b_ed, 'ElGamal')

dataset = get_dataset(df_8b_cos, 'DES')

#%%
# Visualising the Training set results
from matplotlib.colors import ListedColormap
X_set, y_set = sc.inverse_transform(X_train), y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 0.25))
plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('SVM (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

# Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = sc.inverse_transform(X_test), y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 0.25))
plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('SVM (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()