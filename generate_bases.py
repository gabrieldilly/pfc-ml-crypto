# import nltk
# nltk.download('reuters')
from nltk.corpus import reuters 
from binascii import hexlify
from Crypto.Random import get_random_bytes
import time
import pandas as pd

#%%
documents = reuters.fileids()
print(str(len(documents)) + ' documents')

train_docs = list(filter(lambda doc: doc.startswith('train'), documents))
print(str(len(train_docs)) + ' total train documents')

test_docs = list(filter(lambda doc: doc.startswith('test'), documents))
print(str(len(test_docs)) + ' total test documents')

#%%
algorithms = ['DES', 'RSA', 'ElGamal']
#bases = {k:{'ids': [], 'documents': []} for k in algorithms}
train_texts = {k: "" for k in algorithms}
train_base = {k: [] for k in algorithms}
test_texts = {k: "" for k in algorithms}
test_base = {k: [] for k in algorithms}

for i in range(len(train_docs)):
    #bases[algorithms[i % len(algorithms)]]['ids'].append(train_docs[i])
    text = reuters.raw(train_docs[i])
    text += ' ' * ((- len(text)) % 8)
    #bases[algorithms[i % len(algorithms)]]['documents'].append(text)
    train_texts[algorithms[i % len(algorithms)]]+=text
	
for i in range(len(test_docs)):
    #bases[algorithms[i % len(algorithms)]]['ids'].append(train_docs[i])
    text = reuters.raw(test_docs[i])
    text += ' ' * ((- len(text)) % 8)
    #bases[algorithms[i % len(algorithms)]]['documents'].append(text)
    test_texts[algorithms[i % len(algorithms)]]+=text

n = 300000
    
for b in train_texts:
    #bases[b]['text'] = ''.join(bases[b]['documents'])
    #print('\n' + b + ' ' + str(len(bases[b]['text'])) + ' characters')
    #print(b + ' ' + str(len(bases[b]['text'].split(' '))) + ' words')
    print('\n' + b + ' ' + str(len(train_texts[b])) + ' characters')
    print(b + ' ' + str(len(train_texts[b].split(' '))) + ' words')
    for i in range(0, len(train_texts[b]), n):
        train_base[b].append(train_texts[b][i:min(i+n,len(train_texts[b]))])
		
for b in test_texts:
    #bases[b]['text'] = ''.join(bases[b]['documents'])
    #print('\n' + b + ' ' + str(len(bases[b]['text'])) + ' characters')
    #print(b + ' ' + str(len(bases[b]['text'].split(' '))) + ' words')
    print('\n' + b + ' ' + str(len(test_texts[b])) + ' characters')
    print(b + ' ' + str(len(test_texts[b].split(' '))) + ' words')
    for i in range(0, len(test_texts[b]), n):
        test_base[b].append(test_texts[b][i:min(i+n,len(test_texts[b]))])

for b in train_base:
	print('\n' + str(len(train_base[b])))

for b in test_base:
	print('\n' + str(len(train_base[b])))

#%%
# DES
    
from Crypto.Cipher import DES

encrypted_base = {k: {'train': [], 'test': []} for k in algorithms}

key = get_random_bytes(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_ECB)
plaintext = b'lorem ipsum dolor sit amet, consectetur adipiscing elit.'
msg = cipher.encrypt(plaintext)
print(hexlify(msg))

start_time = time.time()

#bases['DES']['encrypted_documents'] = []
#for text in bases['DES']['documents']:
#    bases['DES']['encrypted_documents'].append(hexlify(cipher.encrypt(bytes(text, encoding = 'utf-8'))).decode())
#bases['DES']['encrypted_text'] = ''.join(bases['DES']['encrypted_documents'])

for document in train_base['DES']:
    encrypted_base['DES']['train'].append(hexlify(cipher.encrypt(bytes(document, encoding = 'utf-8'))).decode())
encrypted_base['DES']['train'] = ''.join(encrypted_base['DES']['train'])

for document in test_base['DES']:
    encrypted_base['DES']['test'].append(hexlify(cipher.encrypt(bytes(document, encoding = 'utf-8'))).decode())
encrypted_base['DES']['test'] = ''.join(encrypted_base['DES']['test'])

path = "C:/Users/rafae/Documents/IME/Computação/PFC/pfc-ml-crypto/encrypted_documents"

i = 1
for document in encrypted_base['DES']['train']:
	pd.DataFrame(document).to_csv(path + "/DES_train_doc_" + str(i) + ".txt")
	i+=1
	
i = 1
for document in encrypted_base['DES']['test']:
	pd.DataFrame(document).to_csv(path + "/DES_test_doc_" + str(i) + ".txt")
	i+=1

print(f'Finished. DES elapsed time: {time.time() - start_time}')

#%%
# RSA

encrypted_base = {k: {'train': [], 'test': []} for k in algorithms}

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

message = b'Public and Private keys encryption'
private_key = RSA.generate(1024)
public_key = private_key.publickey()

# Converting the RsaKey objects to string 
private_pem = private_key.exportKey().decode()
public_pem = public_key.exportKey().decode()

# Writing down the private and public keys to 'pem' files
with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    
# Importing keys from files, converting it into the RsaKey object   
pr_key = RSA.importKey(open('private_pem.pem', 'r').read())
pu_key = RSA.importKey(open('public_pem.pem', 'r').read())

# Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key = pu_key)

# Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(message)
print(hexlify(cipher_text))

# Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key = pr_key)

# Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message)

start_time = time.time()

#block_size = 8 # bytes
#bases['RSA']['encrypted_documents'] = []
#for text in bases['RSA']['documents']:
#    text = bytes(text, encoding = 'utf-8')
#    blocks = [cipher.encrypt(text[i:i+block_size]) for i in range(0, len(text), block_size)]
#    bases['RSA']['encrypted_documents'].append(''.join([hexlify(b).decode() for b in blocks]))
#bases['RSA']['encrypted_text'] = ''.join(bases['RSA']['encrypted_documents'])

block_size = 8 # bytes
for document in train_base['RSA']:
    document = bytes(document, encoding = 'utf-8')
    blocks = [cipher.encrypt(document[i:i+block_size]) for i in range(0, len(document), block_size)]
    encrypted_base['RSA']['train'].append(''.join([hexlify(b).decode() for b in blocks]))
#encrypted_base['RSA']['train'] = ''.join(encrypted_base['RSA']['train'])

for document in test_base['RSA']:
    document = bytes(document, encoding = 'utf-8')
    blocks = [cipher.encrypt(document[i:i+block_size]) for i in range(0, len(document), block_size)]
    encrypted_base['RSA']['test'].append(''.join([hexlify(b).decode() for b in blocks]))
#encrypted_base['RSA']['test'] = ''.join(encrypted_base['RSA']['test'])

path = "C:/Users/rafae/Documents/IME/Computação/PFC/pfc-ml-crypto/encrypted_documents"

i=1
for document in encrypted_base['RSA']['train']:
    with open(path + "/RSA_train_doc_" + str(i) + ".txt", "w") as text_file:
	    print(document, file=text_file)	
    i+=1

i=1
for document in encrypted_base['RSA']['test']:
    with open(path + "/RSA_test_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. RSA elapsed time: {str_time}')

#%%
# ElGamal

