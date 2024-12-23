"""
Classes for handling Media data
"""


class MvDoc: 
    """
    class for movie data
    """
    def __init__(self, title, director, rating, synopsis, release_date, runtime):
        self.title = title
        self.director = director
        self.rating = rating
        self.synopsis = synopsis
        self.release_date = release_date
        self.runtime = runtime
        self.type = 'Movie'

    def __str__(self):
        return f'Title:{self.title}\t\nRelease Date: {self.release_date}\t\nRating - {self.rating}\t\n'
    
    def __repr__(self):
        return f'Title:{self.title}\t\nDirector:{self.director}\t\nRating:{self.rating}\t\nSynopsis:{self.synopsis[:50]}...\t\nRelease Date:{self.release_date}\t\nRuntime:{self.runtime}\t\n'
    
    def getType(self):
        return self.type
        
class Director:
    """
    Class for Directors and their bibliography
    """
    def __init__(self, name):
        self.name = name # Director's name
        self.nbMovies = 0 # Number of movies directed
        self.bibli= [] # List of movies directed

    def __str__(self):
        return f'Director: {self.name}\nNumber of movies directed: {self.nbMovies}\n\t'
    
    def __repr__(self):
        return f'Director: {self.name}\n\tNumber of movies directed: {self.nbMovies}\n\tList of movies directed: {self.bibli}\n\t'
    
    def add(self, movie): 
        """
        simple method to add a movie to the director's bibliography
        """
        self.bibli.append(movie)
        self.nbMovies += 1
    
class SeriDoc(MvDoc):
    """
    Child class for TV series data
    """
    def __init__(self, title, creator, rating, synopsis, release_date, runtime, num_seasons, num_episodes, status):
        super().__init__(title, creator, rating, synopsis, release_date, runtime)
        self.creator = creator
        self.num_seasons = num_seasons
        self.num_episodes = num_episodes
        self.status = status
        self.type = 'TV Series'
    
    def __repr__(self):
        return f'Title:{self.title}\t\nCreator:{self.creator}\t\nRating:{self.rating}\t\nSynopsis:{self.synopsis[:50]}...\t\nRelease Date:{self.release_date}\t\nRuntime:{self.runtime}\t\nNumber of seasons:{self.num_seasons}\t\nNumber of episodes:{self.num_episodes}\t\nStatus:{self.status}\t\n'
        
    def __str__(self):
        return f'Title:{self.title}\t\nRelease Date: {self.release_date}\t\nRating - {self.rating}\t\n'
    
    def getType(self):
        return self.type

class Creator(Director):
    """
    Child class of Director for TV series creators
    """
    def __init__(self, name):
        super().__init__(name)
        self.nbSeries = 0 # Number of TV series created
        self.bibli = [] # List of TV series created

    def __str__(self):
        return f'Creator: {self.name}\nNumber of TV series created: {self.nbSeries}\n\t'
    
    def __repr__(self):
        return f'Creator: {self.name}\n\tNumber of TV series created: {self.nbSeries}\n\tList of TV series created: {self.bibli}\n\t'
    
    def add(self, series):
        """
        simple method to add a TV series to the creator's bibliography
        """
        self.bibli.append(series)
        self.nbSeries += 1
    
    