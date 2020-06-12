import nltk
nltk.download('reuters')
from nltk.corpus import reuters 

#%%
documents = reuters.fileids()
print(str(len(documents)) + ' documents')

train_docs = list(filter(lambda doc: doc.startswith('train'), documents))
print(str(len(train_docs)) + ' total train documents')
 
test_docs = list(filter(lambda doc: doc.startswith('test'), documents))
print(str(len(test_docs)) + ' total test documents')

#%%
algorithms = ['DES', 'RSA', 'ElGamal']
bases = {k:{'ids': [], 'documents': []} for k in algorithms}

for i in range(0, len(train_docs)):
    bases[algorithms[i % len(algorithms)]]['ids'].append(train_docs[i])
    bases[algorithms[i % len(algorithms)]]['documents'].append(reuters.raw(train_docs[i]))
    
for b in bases:
    bases[b]['text'] = ''.join(bases[b]['documents'])
    print('\n' + b + ' ' + str(len(bases[b]['text'])) + ' characters')
    print(b + ' ' + str(len(bases[b]['text'].split(' '))) + ' words')

#%%
# DES
    
from Crypto.Cipher import DES3
from Crypto import Random

key = b'Sixteen byte key'
cipher = DES3.new(key, DES3.MODE_ECB)
plaintext = b'lorem ipsum dolor sit amet'
msg = cipher.encrypt(plaintext)


#%%
# RSA


#%%
# ElGamal

