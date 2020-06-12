# TO INSTALL
# pip install nltk
# import nltk
# nltk.download('reuters')
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
    print(b + ' ' + str(len(bases[b]['text'])) + ' characters')
    print(b + ' ' + str(len(bases[b]['text'].split(' '))) + ' words\n')

#%%
# TO INSTALL
# pip install pycryptodome

from Crypto.Cipher import DES3
from Crypto import Random

key = b'Sixteen byte key'
iv = Random.new().read(DES3.block_size)
cipher = DES3.new(key, DES3.MODE_ECB, iv)
plaintext = b'sona si latine loqueris '
msg = iv + cipher.encrypt(plaintext)


def collection_stats():
    # List of documents
    documents = reuters.fileids()
    print(str(len(documents)) + ' documents')
 
    train_docs = list(filter(lambda doc: doc.startswith('train'), documents))
    print(str(len(train_docs)) + ' total train documents')
 
    test_docs = list(filter(lambda doc: doc.startswith('test'), documents))
    print(str(len(test_docs)) + ' total test documents')
 
    # List of categories
    categories = reuters.categories()
    print(str(len(categories)) + ' categories')
 
    # Documents in a category
    category_docs = reuters.fileids('acq')
 
    # Words for a document
    document_id = category_docs[0]
    document_words = reuters.words(category_docs[0])
    print(document_words)  
 
    # Raw document
    print(reuters.raw(document_id))
    
#%%
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
 
cachedStopWords = stopwords.words('english')
 
def tokenize(text):
    min_length = 3
    words = map(lambda word: word.lower(), word_tokenize(text))
    words = [word for word in words if word not in cachedStopWords]
    tokens = (list(map(lambda token: PorterStemmer().stem(token), words)))
    p = re.compile('[a-zA-Z]+')
    filtered_tokens = list(filter(lambda token: p.match(token) and len(token)>=min_length, tokens))
    return filtered_tokens

# Return the representer, without transforming
def tf_idf(docs):
    tfidf = TfidfVectorizer(tokenizer=tokenize, min_df=3,
                        max_df=0.90, max_features=3000,
                        use_idf=True, sublinear_tf=True,
                        norm='l2')
    tfidf.fit(docs)
    return tfidf

def feature_values(doc, representer):
    doc_representation = representer.transform([doc])
    features = representer.get_feature_names()
    return [(features[index], doc_representation[0, index])
                 for index in doc_representation.nonzero()[1]]

def main():
    train_docs = []
    test_docs = []
 
    for doc_id in reuters.fileids():
        if doc_id.startswith('train'):
            train_docs.append(reuters.raw(doc_id))
        else:
            test_docs.append(reuters.raw(doc_id))
 
    representer = tf_idf(train_docs)
 
    for doc in test_docs:
        print(feature_values(doc, representer))