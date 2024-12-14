"""
Corpus class to manage movie data corpus
"""
import pandas as pd
import pickle
from MovieClasses import MvDoc, Director
import datetime

class MvCorpus:
    """
    Corpus class for movie data
    """
    def __init__(self, name):
        self.name = name # Name of the corpus
        self.directors = {} # Dictionary to store directors (Key: Director names, Value: Director object)
        self.id2mv = {} # Dictionary to store movies with their IDs ( Key: ID, Value: Movie object)
        self.nmov = 0 # Number of movies in the corpus
        self.ndir = 0 # Number of directors in the corpus

    def __str__(self):
        return f'Corpus Name: {self.name}\nNumber of movies: {self.nmov}\nNumber of directors: {self.ndir}\n'
    
    def __repr__(self):
        mvs = list(self.id2mv.values())
        mvs = list(sorted(mvs, key=lambda x: x.title.lower()))[:10]
        return "\n".join(list(map(str, mvs)))

    def add(self, movie):
        """
        Method to add a movie to the corpus.
        """
        if movie.director not in self.directors: # if the director is not in the directors dictionary,
            self.directors[movie.director] = Director(movie.director) # Create a director object and store it in the directors dictionary
            self.ndir += 1 # increment the number of directors
        self.directors[movie.director].add(movie)
        self.id2mv[self.nmov] = MvDoc(movie.title, movie.director, movie.rating, movie.synopsis, movie.release_date, movie.runtime) # store the movie object in the id2mv dictionary
        self.nmov += 1
    
    def show(self, n=-1, sortby='title'):
        """
        Method to display the contents of the corpus.  
        It can be sorted by the movie title, release date, Rating, Runtime, director.  
        By default it will display all the movies(-1), and sort by Movie title 'title'.  
        """
        movies = list(self.id2mv.values())
        if sortby == 'title': # Sorting by movie title
            movies = list(sorted(movies, key=lambda x: x.title.lower()))[:n]
        elif sortby == 'date': # Sorting by release date
            # since the release date is in Month day, year format, we need to consider the format
            movies = list(sorted(movies, key=lambda x: datetime.datetime.strptime(x.release_date, '%B %d, %Y')))[:n]
        elif sortby == 'rates': # Sorting by rating
            movies = list(sorted(movies, key=lambda x: float(x.rating.split()[0]), reverse=True))[:n]
        elif sortby == 'runtime': # Sorting by runtime
            # Since the run time was converted to a string, we need to treat it as a string
            movies = list(sorted(movies, key=lambda x: x.runtime, reverse=True))[:n]
        elif sortby == 'director': # Sorting by director
            movies = list(sorted(movies, key=lambda x: x.director))[:n]

        print("\n".join(list(map(repr, movies))))

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
            return pickle.load(f)
        print(f'Corpus loaded from {filename}.pkl')

    def PDsave(self, filename):
        """
        Method to save the corpus to a pandas Dataframe.
        """
        mvs = list(self.id2mv.values())
        mvs = list(sorted(mvs, key=lambda x: x.title.lower()))
        df = pd.DataFrame(columns=['Title', 'Director', 'Rating', 'Synopsis', 'Release Date', 'Runtime'])
        for i, mv in enumerate(mvs):
            df.loc[i] = [mv.title, mv.director, mv.rating, mv.synopsis, mv.release_date, mv.runtime]
        df = df.set_index('Title')
        df.to_csv(filename+'.csv')
        print(f'Corpus saved as {filename}.csv')
    
    def PDload(self, filename):
        """
        Method to load a corpus from a pandas Dataframe.
        """
        df = pd.read_csv(filename+'.csv')
        corpus = MvCorpus(filename)
        for i, row in df.iterrows():
            movie = MvDoc(row['Title'], row['Director'], row['Rating'], row['Synopsis'], row['Release Date'], row['Runtime'])
            self.add(movie)
        print(f'Corpus loaded from {filename}.csv')
