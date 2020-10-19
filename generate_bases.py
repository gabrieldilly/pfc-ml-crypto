from binascii import hexlify
from Crypto.Random import get_random_bytes
import time
from os import listdir
from os.path import isfile, join

#%%
# Parameters

# Cryptographed files path
path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"

# Base path
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Base"
		
# Number of documents
d = 30

# % Tests, Train, Validation
#teste =
#train =
#validation = 

# Cryptographed document size
n = 500*1024

# Block size
RSA_block_size = 86 #bytes
Elgamal_block_size = 64 #bits

# Remark: DES has default block size (64 bits)

#%%

algorithms = ['RSA', 'DES', 'ElGamal']
text = ""
encrypted_base = {k: [] for k in algorithms}
onlyfiles = [f for f in listdir(path2) if isfile(join(path2, f))]

for f in onlyfiles:
    with open(path2 + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        text+=data

#%%
# DES
    
from Crypto.Cipher import DES

key = get_random_bytes(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_ECB)

start_time = time.time()

DES_text = bytes(text, encoding = 'utf-8')

encrypted_text = cipher.encrypt(DES_text[0:(16*int(len(DES_text)/16))])
encrypted_text = hexlify(encrypted_text).decode()

for i in range(0,len(encrypted_text), n):
    encrypted_base['DES'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['DES']:
    with open(path + "\\DES_doc_" + (('0'+str(i)) if i<10 else str(i)) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1
    if i == d+1:
        break

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

encrypted_text=''

for i in range(0, len(text), RSA_block_size):
    try:
        RSA_text = bytes(text[i:min(i+RSA_block_size, len(text)-1)], encoding = 'utf-8')
        block = cipher.encrypt(RSA_text)
        encrypted_text+=hexlify(block).decode()
    except Exception as e:
        print(e)
        continue

for i in range(0,len(encrypted_text), n):        
    encrypted_base['RSA'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['RSA']:
    with open(path + "\\RSA_doc_" + (('0'+str(i)) if i<10 else str(i)) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1
    if i == d+1:
        break

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. RSA elapsed time: {str_time}')

#%%
# ElGamal

#from .elgamal import ElGamal

el = ElGamal()

start_time = time.time()

encrypted_text = el.encrypt(text, Elgamal_block_size)

for i in range(0,len(encrypted_text), n):
    encrypted_base['ElGamal'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['ElGamal']:
    with open(path + "\\ElGamal_doc_" + (('0'+str(i)) if i<10 else str(i)) + ".txt", "w") as text_file:
	    print(document, file=text_file)	
    i+=1
    if i == d+1:
        break

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. ElGamal elapsed time: {str_time}')