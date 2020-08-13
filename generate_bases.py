from binascii import hexlify
from Crypto.Random import get_random_bytes
import time
from os import listdir
from os.path import isfile, join

path = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\encrypted_documents"
path2 = "C:\\Users\\rafae\\Documents\\IME\\Computação\\PFC\\pfc-ml-crypto\\Base"

#%%
algorithms = ['RSA', 'DES', 'ElGamal']
total_texts = ""
total_base = {k: '' for k in algorithms}
encrypted_base = {k: [] for k in algorithms}

onlyfiles = [f for f in listdir(path2) if isfile(join(path2, f))]

for f in onlyfiles:
    with open(path2 + "\\" + f, 'r') as file:
        data = file.read().replace('\n', '')
        total_texts+=data

total_base['DES']+=(total_texts[0:int(len(total_texts)/3)-1])
total_base['RSA']+=(total_texts[int(len(total_texts)/3):2*int(len(total_texts)/3)-1])
total_base['ElGamal']+=(total_texts[2*int(len(total_texts)/3):len(total_texts)])

#%%
# DES
    
from Crypto.Cipher import DES

key = get_random_bytes(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_ECB)

start_time = time.time()

total_base['DES'] = bytes(total_base['DES'], encoding = 'utf-8')

encrypted_text = cipher.encrypt(total_base['DES'][0:(len(total_base['DES'])-5)])
encrypted_text = hexlify(encrypted_text).decode()

n = 500000

for i in range(0,len(encrypted_text), n):
    encrypted_base['DES'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['DES']:
    with open(path + "\\DES_doc_" + str(i) + ".txt", "w") as text_file:
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

block_size = 86 # bytes
blocks = [cipher.encrypt(bytes(total_base['RSA'][i:i+block_size], encoding = 'utf-8')) for i in range(0, len(total_base['RSA']), block_size)]

encrypted_text=''
for b in blocks:
    encrypted_text+=hexlify(b).decode()

n = 500000

for i in range(0,len(encrypted_text), n):
    encrypted_base['RSA'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['RSA']:
    with open(path + "\\RSA_doc_" + str(i) + ".txt", "w") as text_file:
        print(document, file=text_file)
    i+=1

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. RSA elapsed time: {str_time}')

#%%
# ElGamal

#from .elgamal import ElGamal

el = ElGamal()

start_time = time.time()

encrypted_text = el.encrypt(total_base['ElGamal'])
		
n = 500000

for i in range(0,len(encrypted_text), n):
    encrypted_base['ElGamal'].append(encrypted_text[i:i+n-1])

i=1
for document in encrypted_base['ElGamal']:
    with open(path + "\\ElGamal_doc_" + str(i) + ".txt", "w") as text_file:
	    print(document, file=text_file)	
    i+=1

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. ElGamal elapsed time: {str_time}')