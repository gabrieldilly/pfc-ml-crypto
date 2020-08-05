from binascii import hexlify
from Crypto.Random import get_random_bytes
import time
from os import listdir
from os.path import isfile, join

path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\encrypted_documents"
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\pfc-ml-crypto\\Base"

#%%
algorithms = ['DES', 'RSA', 'ElGamal']
total_texts = ""
total_base = []
train_base = {k: [] for k in algorithms}
test_base = {k: [] for k in algorithms}
validation_base = {k: [] for k in algorithms}
encrypted_base = {k: {'train': [], 'test': [], 'validation': []} for k in algorithms}

onlyfiles = [f for f in listdir(path2) if isfile(join(path2, f))]

for f in onlyfiles:
    with open(path2 + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        total_texts+=data

n = 300000
   
for i in range(0, len(total_texts), n):
	total_base.append(total_texts[i:min(i+n,len(total_texts))])
    
j = 0

## 60% train - 20% test - 20% validation
for k in algorithms:
    for t in range(j,j+6):
        validation_base[k].append(total_base[t])
    for t in range(j+6, j+12):
        test_base[k].append(total_base[t])
    for t in range(j+12,j+30):
        train_base[k].append(total_base[t])
    j+=30

for b in train_base:
	print('\n' + b + ' Train Base has ' + str(len(train_base[b])) + " documents")

for b in test_base:
	print('\n' + b + ' Test Base has ' + str(len(test_base[b])) + " documents")
	
for b in validation_base:
	print('\n' + b + ' Validation Base has ' + str(len(validation_base[b])) + " documents")

#%%
# DES
    
from Crypto.Cipher import DES

key = get_random_bytes(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_ECB)

start_time = time.time()

for document in train_base['DES']:
    document = bytes(document, encoding = 'utf-8')
    encrypted_base['DES']['train'].append(hexlify(cipher.encrypt(document)).decode())
    print("document encrypted")
	
for document in test_base['DES']:
    document = bytes(document, encoding = 'utf-8')
    encrypted_base['DES']['test'].append(hexlify(cipher.encrypt(document)).decode())
    print("document encrypted")
	
for document in validation_base['DES']:
    document = bytes(document, encoding = 'utf-8')
    encrypted_base['DES']['validation'].append(hexlify(cipher.encrypt(document)).decode())
    print("document encrypted")
	
i=1
for document in encrypted_base['DES']['train']:
    with open(path + "\\DES_train_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

i=1
for document in encrypted_base['DES']['test']:
    with open(path + "\\DES_test_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

i=1
for document in encrypted_base['DES']['validation']:
    with open(path + "\\DES_validation_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

print(f'Finished. DES elapsed time: {time.time() - start_time}')

#%%
# RSA

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

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

start_time = time.time()

block_size = 64 # bytes
for document in train_base['RSA']:
    document = bytes(document, encoding = 'utf-8')
    blocks = [cipher.encrypt(document[i:i+block_size]) for i in range(0, len(document), block_size)]
    encrypted_base['RSA']['train'].append(''.join([hexlify(b).decode() for b in blocks]))
    print("document encrypted")
	
for document in test_base['RSA']:
    document = bytes(document, encoding = 'utf-8')
    blocks = [cipher.encrypt(document[i:i+block_size]) for i in range(0, len(document), block_size)]
    encrypted_base['RSA']['test'].append(''.join([hexlify(b).decode() for b in blocks]))
    print("document encrypted")
	
for document in validation_base['RSA']:
    document = bytes(document, encoding = 'utf-8')
    blocks = [cipher.encrypt(document[i:i+block_size]) for i in range(0, len(document), block_size)]
    encrypted_base['RSA']['validation'].append(''.join([hexlify(b).decode() for b in blocks]))
    print("document encrypted")
	
i=1
for document in encrypted_base['RSA']['train']:
    with open(path + "\\RSA_train_doc_" + str(i) + ".txt", "w") as text_file:
	    print(document, file=text_file)
    i+=1

i=1
for document in encrypted_base['RSA']['test']:
    with open(path + "\\RSA_test_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1
	
i=1
for document in encrypted_base['RSA']['validation']:
    with open(path + "\\RSA_validation_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. RSA elapsed time: {str_time}')

#%%
# ElGamal

#from .elgamal import ElGamal

el = ElGamal()

start_time = time.time()

for document in train_base['ElGamal']:
    encrypted_base['ElGamal']['train'].append(el.encrypt(document))
    print("document encrypted")
	
for document in test_base['ElGamal']:  
    encrypted_base['ElGamal']['test'].append(el.encrypt(document))
    print("document encrypted")
	
for document in validation_base['ElGamal']:
    encrypted_base['ElGamal']['validation'].append(el.encrypt(document))
    print("document encrypted")
	
i=1
for document in encrypted_base['ElGamal']['train']:
    with open(path + "\\ElGamal_train_doc_" + str(i) + ".txt", "w") as text_file:
	    print(document, file=text_file)	
    i+=1

i=1
for document in encrypted_base['ElGamal']['test']:
    with open(path + "\\ElGamal_test_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1
	
i=1
for document in encrypted_base['ElGamal']['validation']:
    with open(path + "\\ElGamal_validation_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. ElGamal elapsed time: {str_time}')