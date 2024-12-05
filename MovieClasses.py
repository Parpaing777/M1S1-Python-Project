# Class for handling Movie data

# Class for movies
class MvDoc: 
    def __init__(self, title, director, rating, synopsis, release_date, runtime):
        self.title = title
        self.director = director
        self.rating = rating
        self.synopsis = synopsis
        self.release_date = release_date
        self.runtime = runtime

    def __str__(self):
        return f'Title:{self.title}\t\nRelease Date: {self.release_date}\t\nRating - {self.rating}\t\n'
    
    def __repr__(self):
        return f'Title:{self.title}\t\nDirector:{self.director}\t\nRating:{self.rating}\t\nSynopsis:{self.synopsis[:50]}\t\nRelease Date:{self.release_date}\t\nRuntime:{self.runtime}\t\n'
    

# Class for directors

class Director:
    def __init__(self, name):
        self.name = name
        self.nbMovies = 0 # Number of movies directed
        self.bibli= [] # List of movies directed

    def __str__(self):
        return f'Director: {self.name}\nNumber of movies directed: {self.nbMovies}\n\t'
    
    def __repr__(self):
        return f'Director: {self.name}\n\tNumber of movies directed: {self.nbMovies}\n\tList of movies directed: {self.bibli}\n\t'
    
    def add(self, movie): # simple method to add a movie to the director's bibliography
        self.bibli.append(movie)
        self.nbMovies += 1
    
        