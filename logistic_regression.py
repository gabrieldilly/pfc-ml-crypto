# Logistic Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Available datasets
df_8b_cos = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'COS')
df_8b_dice = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'DICE')
df_8b_ed = pd.read_excel('Medidas - 8 bits - 500KB.xlsx', sheet_name = 'ED')

df_16b_cos = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'COS')
df_16b_dice = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'DICE')
df_16b_ed = pd.read_excel('Medidas - 16 bits - 500KB.xlsx', sheet_name = 'ED')

def get_dataset(df, base_selected):
    df = df.set_index('Column1')
    df = df + df.T
    df = df.replace(2, 1)
    df = df[[c for c in df.columns if base_selected in c]]
    df['document'] = df.index
    df['response'] = df['document'].apply(lambda x: 1 if base_selected in x else 0)
    return df

# def get_dataset(df, base_selected):
#     df = df.set_index('Column1')
#     df = df + df.T
#     df = df.replace(2, 1)
#     df = df[[c for c in df.columns if base_selected in c and c in [base_selected + '_doc_' + str(x + 1) + '.txt' for x in range(0, 8)]]]
#     df['document'] = df.index
#     df['response'] = df['document'].apply(lambda x: 1 if base_selected in x else 0)
#     df = df[df['document'].apply(lambda c: c not in [base_selected + '_doc_' + str(x + 1) + '.txt' for x in range(0, 8)])]
#     return df

#%%
# Importing the dataset
dataset = get_dataset(df_8b_ed, 'RSA')

X = dataset.iloc[:, :-2].values
y = dataset.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
print(X_train)
print(y_train)
print(X_test)
print(y_test)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print(X_train)
print(X_test)

# Training the Logistic Regression model on the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
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
plt.title('Logistic Regression (Training set)')
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
plt.title('Logistic Regression (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()