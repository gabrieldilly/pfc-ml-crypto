# Support Vector Machine (SVM)

# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Available datasets
#print("\ninsira o caminho com as medidas de similaridade e dissimilaridade:\n")
#path = input()
#path = "c:/users/rafae/documents/ime/computação/pfc/pfc-ml-crypto/medidas"

#dfs = {}
#for file in glob.glob(path + '/*.csv'):
#    # key = file.split(' - ')[0]
#    key = file.split('\\')[-1].replace('.csv', '')
#    dfs[key] = pd.read_csv(file, delimiter = ';')
 
def compute_average(row, base):
    s = qtd = 0
    for key, val in row.items():
        if base in key and key != row['document']:
            s += val
            qtd += 1
    return s / qtd

def get_dataset(dfs, selected_base, test_resp, train_size):
    result = pd.DataFrame()
    for s in dfs:
        # df = df.set_index('Column1')
        df = dfs[s]
        df['document'] = df.index
        df['document'] = df['document'].apply(lambda x: x.replace('.txt', ''))
        df.columns = [c.replace('.txt', '') for c in df.columns]
        df = df.set_index('document')
        df = df + df.T
        for i in range(0, df.shape[0]):
            df.iloc[i, i] = 1 if df.iloc[i, i] == 2 else df.iloc[i, i]
        df = df[[c for c in df.columns if selected_base in c]]
        if train_size != None:
            df = df[[c for c in df.columns if list(df.columns).index(c) < train_size]]
        df['document'] = df.index
        df['response'] = df['document'].apply(lambda x: 1 if selected_base in x else (test_resp[int(x[(len(x)-2):])-1] if 'test' in x else 0))
        df[s] = df.apply(lambda row: compute_average(row, selected_base), axis = 1)
        # df = df[df['document'].apply(lambda c: c not in [selected_base + '_doc_' + str(x + 1) for x in range(0, training_qtd)])]
        if result.empty:
            result = df[['document', 'response', s]].reset_index(drop = True)
        else:
            result = pd.merge(result, df[['document', s]].reset_index(drop = True), how = 'inner', on = 'document')
    return result

#%%

def generate_model(dfs, selected_metrics, selected_base, test_resp, train_size = None):
    # Importing the dataset
    dataset = get_dataset(dfs, selected_base, test_resp, train_size)
    dataset = dataset[['document', 'response'] + [k + ' - ' + str(v) + ' bits' for k, v in selected_metrics.items()]]
    
    df_train = dataset[dataset['document'].apply(lambda c: 'test' not in c)]
    df_test = dataset[dataset['document'].apply(lambda c: 'test' in c)]
    #X = dataset.iloc[:, 2:].values
    #y = dataset.iloc[:, 1].values
    
    # Splitting the dataset into the Training set and Test set
    # from sklearn.model_selection import train_test_split
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
    # print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))
    
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy_score(y_test, y_pred)

    from matplotlib.colors import ListedColormap
    # X_set, y_set = sc.inverse_transform(X_train), y_train
    X_set, y_set = sc.inverse_transform(X_test), y_test
    print(X_set[:, 0].mean(), X_set[:, 1].mean())
    if X_set[:, 0].mean() < 10 and X_set[:, 1].mean() < 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.01, stop = X_set[:, 0].max() + 0.01, step = 0.00001),
                              np.arange(start = X_set[:, 1].min() - 0.01, stop = X_set[:, 1].max() + 0.01, step = 0.00001))
    elif X_set[:, 0].mean() >= 10 and X_set[:, 1].mean() < 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 300, stop = X_set[:, 0].max() + 300, step = 100),
                              np.arange(start = X_set[:, 1].min() - 0.01, stop = X_set[:, 1].max() + 0.01, step = 0.00001))
    elif X_set[:, 0].mean() < 10 and X_set[:, 1].mean() >= 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.01, stop = X_set[:, 0].max() + 0.01, step = 0.00001),
                              np.arange(start = X_set[:, 1].min() - 0, stop = X_set[:, 1].max() + 0, step = 100.25))
    elif X_set[:, 0].mean() >= 10 and X_set[:, 1].mean() >= 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 300, stop = X_set[:, 0].max() + 300, step = 100),
                              np.arange(start = X_set[:, 1].min() - 300, stop = X_set[:, 1].max() + 300, step = 100))      
        
    plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                    alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('SVM (Base de Teste)')
    plt.xlabel(dataset.columns[2])
    plt.ylabel(dataset.columns[3])
    plt.legend()
    plt.show()
    
    
    X_set, y_set = sc.inverse_transform(X_train), y_train
    # X_set, y_set = sc.inverse_transform(X_test), y_test
    print(X_set[:, 0].mean(), X_set[:, 1].mean())
    if X_set[:, 0].mean() < 10 and X_set[:, 1].mean() < 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.01, stop = X_set[:, 0].max() + 0.01, step = 0.0001),
                              np.arange(start = X_set[:, 1].min() - 0.01, stop = X_set[:, 1].max() + 0.01, step = 0.0001))
    elif X_set[:, 0].mean() >= 10 and X_set[:, 1].mean() < 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 300, stop = X_set[:, 0].max() + 300, step = 100),
                              np.arange(start = X_set[:, 1].min() - 0.01, stop = X_set[:, 1].max() + 0.01, step = 0.0001))
    elif X_set[:, 0].mean() < 10 and X_set[:, 1].mean() >= 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 0.01, stop = X_set[:, 0].max() + 0.01, step = 0.0001),
                              np.arange(start = X_set[:, 1].min() - 0, stop = X_set[:, 1].max() + 0, step = 100))
    elif X_set[:, 0].mean() >= 10 and X_set[:, 1].mean() >= 10:
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 300, stop = X_set[:, 0].max() + 300, step = 100),
                              np.arange(start = X_set[:, 1].min() - 300, stop = X_set[:, 1].max() + 300, step = 100))      
        
    plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                    alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('SVM (Base de Treino)')
    plt.xlabel(dataset.columns[2])
    plt.ylabel(dataset.columns[3])
    plt.legend()
    plt.show()
    

    return y_pred, accuracy_score(y_test, y_pred), cm

#%%

#def evaluate_model(test_resp):

# ## Plot 3D
# %matplotlib inline
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = plt.axes(projection='3d')

# # Data for a three-dimensional line
# zline = X_set[:, 2]
# xline = X_set[:, 0]
# yline = X_set[:, 1]
# ax.scatter3D(xline, yline, zline, c=y_set, cmap='viridis')
