"""
Search Engine class for the media corpus
"""
import numpy as np
import scipy as sp
import pandas as pd
import re
from tqdm import tqdm
import string
from nltk.corpus import stopwords

class SearchEngine:
    """
    A search engine class for the media corpus
    """
    def __init__(self, corpus):
        self.corpus = corpus
        self.Vocab = {}
        self.mat_TF = None # Term Frequency matrix
        self.mat_TFxIDF = None # Term Frequency x Inverse Document Frequency matrix
        self.create_matrix(self.corpus, self.Vocab) # Create the matrix in the first call

    def __simple_clean(self,text):
        """
        simple class method to clean text
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\n', ' ', text)
        return text
    
    def __deep_clean(self,doc):
        """
        More complex method to clean the text (removes stopwords, punctuations, single characters)
        """
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
        # create a continuous string to return
        cleaned = ' '.join(tokens)
        return cleaned

    def create_matrix(self,corpus,Vocab):
        for media in corpus.id2Med.values():
            doc = media.title + ' ' + (media.director if media.type == 'Movie' else media.creator) + ' ' + media.synopsis
            doc = self.__deep_clean(doc)
            for word in doc.split():
                if word not in Vocab:
                    Vocab[word] = {"UniqueID":len(Vocab), "Occurences":1}
                else:
                    Vocab[word]["Occurences"] += 1
        # create the term frequency matrix
        rows = []
        columns = []
        data = []

        for id, media in enumerate(corpus.id2Med.values()):
            doc = media.title + ' ' +  (media.director if media.type == 'Movie' else media.creator) + ' ' + media.synopsis
            doc = self.__deep_clean(doc)
            for word in doc.split():
                if word in Vocab:
                    rows.append(id)
                    columns.append(Vocab[word]["UniqueID"])
                    data.append(1)

        self.mat_TF = sp.sparse.csr_matrix((data, (rows, columns)), shape=(len(corpus.id2Med), len(Vocab)))

        total_occurences = np.array(self.mat_TF.sum(axis=0)).flatten()
        doc_occurences = np.array((self.mat_TF > 0).sum(axis=0)).flatten()

        for word, data in Vocab.items():
            index = data["UniqueID"]
            data["TotalOccurences"] = total_occurences[index]
            data["DocOccurences"] = doc_occurences[index]

        idf_values = np.log(len(corpus.id2Med) / doc_occurences)

        self.mat_TFxIDF = self.mat_TF.multiply(idf_values)
        self.mat_TFxIDF = self.mat_TFxIDF.tocsr()

    def search(self, query):
        query = self.__deep_clean(query)
        query_vector = np.zeros(len(self.Vocab))

        for word in query.split():
            if word in self.Vocab:
                query_vector[self.Vocab[word]["UniqueID"]] = 1

        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            print('No results found')
            return pd.DataFrame(columns=['ID','Title','Synopsis','Cosine Similarity'])
        
        doc_norms = np.linalg.norm(self.mat_TFxIDF.todense(), axis=1)
        cos_sim = np.zeros(len(doc_norms))

        for i, doc_norm in tqdm(enumerate(doc_norms), total=len(doc_norms),desc="Caluclating ..."):
            if doc_norm != 0:
                cos_sim[i] = np.array(self.mat_TFxIDF[i, :].todense()).flatten().dot(query_vector) / (doc_norm * query_norm)
        
        valid_indices = np.where(cos_sim > 0.00)[0]
        res = []
        medKeys = list(self.corpus.id2Med.keys())
        for i in valid_indices:
            title = self.corpus.id2Med[medKeys[i]].title
            text = self.corpus.id2Med[medKeys[i]].synopsis
            res.append([medKeys[i],title,text,cos_sim[i]])
        res = sorted(res, key=lambda x: x[3], reverse=True)
        return pd.DataFrame(res, columns=['ID','Title','Synopsis','Cosine Similarity'])

    

