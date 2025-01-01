######### PROTOTYPE FILE FOR SEARCH ENGINE BEFORE IMPLEMENTING AS A CLASS#######
import numpy as np
import scipy as sp
import pandas as pd
import re
import string
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from Corpus import MdCorpus as mdc

corpus = mdc('test').PKLload('300MVTV')

def simple_clean(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\n', ' ', text)
    return text

def deep_clean( doc):
    # split into tokens by white space
    tokens = doc.split()
    # prepare regex for char filtering
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    # remove punctuation from each word
    tokens = [re_punc.sub('',word) for word in tokens]
    # remove tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # fliter stop words (english)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    # filter tokens with one character
    tokens = [word for word in tokens if len(word) > 1]
    # stemming words
    # stemmed = [SnowballStemmer('english').stem(word) for word in tokens]
    cleaned = ' '.join(tokens)
    return cleaned

Vocab = {}

for text in corpus.id2Med.values():
    texts = text.title + ' ' + (text.director if text.type == 'Movie' else text.creator) + ' ' + text.synopsis
    texts = deep_clean(texts)
    for word in texts.split():
        if word not in Vocab:
            Vocab[word] = {"UniqueID":len(Vocab), "Occurences":1}
        else:
            Vocab[word]["Occurences"] += 1

# Create the Term Frequency matrix
rows = []
columns = []
data = []

# We have to add index values to the rows list, UniqueID to the columns list and Occurences to the data list
for id, text in enumerate(corpus.id2Med.values()):
    texts = text.title + ' ' + (text.director if text.type == 'Movie' else text.creator) + ' ' + text.synopsis
    texts = deep_clean(texts)
    for word in texts.split():
        if word in Vocab:
            rows.append(id)
            columns.append(Vocab[word]["UniqueID"])
            data.append(1)

# Debugging
# print(f'Rows: {len(rows)}')
# print(f'Columns: {len(columns)}')
# print(f'Data: {len(data)}')
# print(f'Vocab length: {len(Vocab)}')
# print(f'Vocab: {Vocab}')

# Create the sparse matrix
mat_TF = sp.sparse.csr_matrix((data, (rows, columns)), shape=(len(corpus.id2Med), len(Vocab)))

# print(f'TF matrix shape: {mat_TF.shape}')
# print(mat_TF.todense())

total_occurences = np.array(mat_TF.sum(axis=0)).flatten()
doc_occurences = np.array((mat_TF > 0).sum(axis=0)).flatten()

for word, data in Vocab.items():
    index = data["UniqueID"]
    data["TotalOccurences"] = total_occurences[index]
    data["DocOccurences"] = doc_occurences[index]

idf_values = np.log(len(corpus.id2Med) / doc_occurences)

mat_TFxIDF = mat_TF.multiply(idf_values)
mat_TFxIDF = mat_TFxIDF.tocsr()

# Debugging
# print(f'TF matrix shape: {mat_TF.shape}')
# print(f'TFxIDF matrix shape: {mat_TFxIDF.shape}')
# print(f'Vocab length: {len(Vocab)}')

def search(mat_TFxIDF,Vocab):
    query = input('Enter your search query: ')
    query = deep_clean(query)
    # Create a vector for the query
    query_vector = np.zeros(len(Vocab))
    # Fill the query vector
    for word in query.split():
        if word in Vocab:
            query_vector[Vocab[word]["UniqueID"]] = 1 
    
    # Calculate the cosine similarity between the query vector and the documents
    query_norm = np.linalg.norm(query_vector)
    if query_norm == 0:
        print('No match found')
        return pd.DataFrame(columns=['ID','Title','Synopsis','Cosine Similarity'])
    
    doc_norms =np.linalg.norm(mat_TFxIDF.todense(), axis=1)
    cos_sim = np.zeros(len(doc_norms))

    for i, doc_norm in tqdm(enumerate(doc_norms), total=len(doc_norms),desc="Caluclating ..."):
        if doc_norm != 0:
            cos_sim[i] = np.array(mat_TFxIDF[i, :].todense()).flatten().dot(query_vector) / (doc_norm * query_norm)
        
    # most_sim_doc = np.argsort(cos_sim)[::-1][:10]

    valid_indices = np.where(cos_sim > 0.0)[0]
    res = []
    medKeys = list(corpus.id2Med.keys())

    for i in valid_indices:
        title = corpus.id2Med[medKeys[i]].title
        text = corpus.id2Med[medKeys[i]].synopsis
        res.append([medKeys[i],title,text,cos_sim[i]])
    if not res:
        print('No match found')
        return pd.DataFrame(columns=['ID','Title','Synopsis','Cosine Similarity'])
    
    res = sorted(res, key=lambda x: x[3], reverse=True)
    return pd.DataFrame(res, columns=['ID','Title','Synopsis','Cosine Similarity'])

print(search(mat_TFxIDF,Vocab))