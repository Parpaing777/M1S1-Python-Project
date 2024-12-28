"""
Corpus class to manage movie data corpus
"""
import pandas as pd
import pickle
from MovieClasses import MvDoc, Director, SeriDoc, Creator
import datetime
import re

class MdCorpus:
    """
    Corpus class for movie data
    """
    def __init__(self, name):
        self.name = name # Name of the corpus
        self.directors = {} # Dictionary to store directors (Key: Director names, Value: Director object)
        self.creators = {} # Dictionary to store TV series creators (Key: Creator names, Value: Creator object)
        self.id2Med = {} # Dictionary to store movies and TV series with their IDs ( Key: ID, Value: Movie/TV series object)
        self.nmov = 0 # Number of movies in the corpus
        self.nser = 0 # Number of TV series in the corpus
        self.ncrt = 0 # Number of creators in the corpus
        self.ndir = 0 # Number of directors in the corpus

    def __str__(self):
        return f'Corpus Name: {self.name}\t\nNumber of TV series: {self.nser}\t\nNumber of Movies: {self.nmov}\t\nTotal number of Medias: {self.nmov+self.nser}\t\nNumber of directors/creators: {self.ndir + self.ncrt}\t\n'
    
    def __repr__(self):
        mvs = list(self.id2Med.values())
        mvs = list(sorted(mvs, key=lambda x: x.title.lower()))[:10]
        return "\n".join(list(map(str, mvs)))
    
    def addMedia(self, media):
        """
        Method to add movies or TV series to the corpus
        """
        if media.type == 'Movie':
            if media.director not in self.directors:
                self.directors[media.director] = Director(media.director)
                self.ndir += 1
            self.directors[media.director].add(media)
            self.id2Med[self.nmov] = MvDoc(media.title, media.director, media.rating, media.synopsis, media.release_date, media.runtime)
            self.nmov += 1
        elif media.type == 'TV Series':
            if media.creator not in self.creators:
                self.creators[media.creator] = Creator(media.creator)
                self.ncrt += 1
            self.creators[media.creator].add(media)
            self.id2Med[self.nmov+self.nser] = SeriDoc(media.title, media.creator, media.rating, media.synopsis, media.release_date, media.runtime, media.num_seasons, media.num_episodes, media.status)
            self.nser += 1

    def show(self, n=-1, sortby='title'):
        """
        Method to display the contents of the corpus.  
        It can be sorted by the movie title, release date, Rating, Runtime, director.  
        By default it will display all the movies(-1), and sort by Movie title 'title'.  
        """
        medias = list(self.id2Med.values())
        if sortby == 'title': # Sorting by movie title
            medias = list(sorted(medias, key=lambda x: x.title.lower()))[:n]
        elif sortby == 'date': # Sorting by release date
            # since the release date is in Month day, year format, we need to consider the format
            medias = list(sorted(medias, key=lambda x: datetime.datetime.strptime(x.release_date, '%B %d, %Y')))[:n]
        elif sortby == 'rates': # Sorting by rating
            medias = list(sorted(medias, key=lambda x: float(x.rating.split()[0]), reverse=True))[:n]
        elif sortby == 'runtime': # Sorting by runtime
            # Since the run time was converted to a string, we need to treat it as a string
            # For medias with 'N/A' runtime, they are placed at the end of the list
            valid = [x for x in medias if x.runtime != 'N/A']
            invalid = [x for x in medias if x.runtime == 'N/A']

            valid = list(sorted(valid, key=lambda x: x.runtime, reverse=True))[:n]
            medias = valid + invalid[:n-len(valid)] if n != -1 else valid + invalid
            
            # medias = list(sorted(medias, key=lambda x: x.runtime, reverse=True))[:n]
        elif sortby == 'maker': # Sorting by director/creator
            if medias[0].type == 'Movie':
                medias = list(sorted(medias, key=lambda x: x.director.lower()))[:n]
            elif medias[0].type == 'TV Series':
                medias = list(sorted(medias, key=lambda x: x.creator.lower()))[:n]

        print("\n".join(list(map(repr, medias))))

    def PKLsave(self, filename):
        """
        Method to save the corpus to a pickle file.
        """
        with open(filename+'.pkl', 'wb') as f:
            pickle.dump(self, f)
        print(f'Corpus saved as {filename}.pkl')

    def PKLload(self, filename):
        """
        Method to load a corpus from a pickle file.
        """
        with open(filename+'.pkl', 'rb') as f:
            corpus =  pickle.load(f)
        print(f'Corpus loaded from {filename}.pkl')
        return corpus
    
    def get_textData(self):
        """
        Method to get useful text data from the corpus
        (Title, Director/Creator, Synopsis)
        """
        try:
            return self.allText
        except:
            self.allText = ' '.join([media.title + ' ' + (media.director if media.type == 'Movie' else media.creator) + ' ' + media.synopsis for media in self.id2Med.values()])
            return self.allText

    def Search(self, pattern):
        """
        Method to search keywords in the movies/TV series
        """
        texts = self.get_textData()
        pattern = re.compile(pattern, re.IGNORECASE) # Compile the pattern and ignore case
        # Search for the pattern in the text string
        results = pattern.finditer(texts)
        # Get the start pos of the pattern in the text
        startPos = [match.start() for match in results]
        # Print the results
        print(f'{len(startPos)} results found')
        # Return the passages where the pattern was found as a list
        return[texts[i-20:i+20] for i in startPos]
    
    def concorde(self, pattern, context_size=20):
        """
        Similar method to the Search but returns a pandas dataframe
        """
        texts = self.get_textData()
        pattern = re.compile(pattern, re.IGNORECASE)

        results = pattern.finditer(texts)
        startPos = [match.span() for match in results]

        context_left = []
        context_right = []
        motif_found = []

        for i,j in startPos:
            context_left.append(texts[i-context_size:i])
            motif_found.append(texts[i:j])
            context_right.append(texts[j:j+context_size])

        df = pd.DataFrame({'Left Context': context_left, 'Pattern': motif_found, 'Right Context': context_right})
        return df

    def clean_text(self, text):
        """
        Simple method to clean text 
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\n', ' ', text)
        return text
    
    def vocabularize(self):
        """
        Method to build a vocabulary dictionary from the text data
        """
        texts = self.get_textData()
        # Clean the text
        texts = self.clean_text(texts)
        # Split the text into words (tokenization)
        words = texts.split()
        # Build the vocabulary dictionary
        self.vocab = {}
        # Stock the split words in the dictionary. But pass by the set to avoid duplicates
        for word in set(words):
            self.vocab[word] = words.count(word)
        return self.vocab
    
    def stats(self, nreturn=10):
        """
        Method to display total number of words in the Vocabulary and the most frequent words
        """
        # Get the text data
        text_data = self.get_textData()
        
        # Split the text data into words and clean the text
        words = self.clean_text(text_data)
        words = re.sub(r'[^\w\s]', '', text_data).split()
        
        # Calculate word frequencies
        word_freq = pd.Series(words).value_counts()
        
        # Print the total number of words and the most frequent words
        print(f'Total number of words in the Vocabulary: {len(words)}')
        print(f'The {nreturn} most frequent words are:')
        print(word_freq.head(nreturn).index.tolist())
        
        return word_freq.to_dict()

