# import nltk
# nltk.download('reuters')
from nltk.corpus import reuters 
from binascii import hexlify
from Crypto.Random import get_random_bytes
import time

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

for i in range(len(train_docs)):
    bases[algorithms[i % len(algorithms)]]['ids'].append(train_docs[i])
    text = reuters.raw(train_docs[i])
    text += ' ' * ((- len(text)) % 8)
    bases[algorithms[i % len(algorithms)]]['documents'].append(text)
    
for b in bases:
    bases[b]['text'] = ''.join(bases[b]['documents'])
    print('\n' + b + ' ' + str(len(bases[b]['text'])) + ' characters')
    print(b + ' ' + str(len(bases[b]['text'].split(' '))) + ' words')

#%%
# DES
    
from Crypto.Cipher import DES

key = get_random_bytes(8)
key = b'-8B key-'
cipher = DES.new(key, DES.MODE_ECB)
plaintext = b'lorem ipsum dolor sit amet, consectetur adipiscing elit.'
msg = cipher.encrypt(plaintext)
print(hexlify(msg))

start_time = time.time()

bases['DES']['encrypted_documents'] = []
for text in bases['DES']['documents']:
    bases['DES']['encrypted_documents'].append(hexlify(cipher.encrypt(bytes(text, encoding = 'utf-8'))).decode())
bases['DES']['encrypted_text'] = ''.join(bases['DES']['encrypted_documents'])

print(f'Finished. DES elapsed time: {time.time() - start_time}')

#%%
# RSA

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

message = b'Public and Private keys encryption'
private_key = RSA.generate(1024)
public_key = private_key.publickey()

# Converting the RsaKey objects to string 
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()

# Writing down the private and public keys to 'pem' files
with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)
with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)
    
# Importing keys from files, converting it into the RsaKey object   
pr_key = RSA.import_key(open('private_pem.pem', 'r').read())
pu_key = RSA.import_key(open('public_pem.pem', 'r').read())

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

block_size = 8 # bytes
bases['RSA']['encrypted_documents'] = []
for text in bases['RSA']['documents']:
    text = bytes(text, encoding = 'utf-8')
    blocks = [cipher.encrypt(text[i:i+block_size]) for i in range(0, len(text), block_size)]
    bases['RSA']['encrypted_documents'].append(''.join([hexlify(b).decode() for b in blocks]))
bases['RSA']['encrypted_text'] = ''.join(bases['RSA']['encrypted_documents'])

str_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
print(f'Finished. RSA elapsed time: {str_time}')

#%%
# ElGamal

