"""
Unit tests for the movieclasses module.
"""
import unittest
from MovieClasses import MvDoc, SeriDoc, Director, Creator

class TestMvDoc(unittest.TestCase):
    """
    Unit test class for MvDoc
    """
    def setUp(self): # Set up function to create an instance of MvDoc
        self.Movie = MvDoc(
            title='The Shawshank Redemption',
            director='Frank Darabont',
            rating=8.708,
            synopsis='Imprisoned in the 1940s for the double murder of his wife and her lover,...',
            release_date='1994-09-23',
            runtime=142
        )

    def testMvAtt(self):
        self.assertEqual(self.Movie.title, "The Shawshank Redemption")
        self.assertEqual(self.Movie.director, 'Frank Darabont')
        self.assertEqual(self.Movie.rating, 8.708)
        self.assertEqual(self.Movie.synopsis, 'Imprisoned in the 1940s for the double murder of his wife and her lover,...')
        self.assertEqual(self.Movie.release_date, '1994-09-23')
        self.assertEqual(self.Movie.runtime, 142)
        self.assertEqual(self.Movie.type, "Movie")
    
    # If the attribute tests pass, the str, repr and get type are not needed to test
    
class TestSeriDoc(unittest.TestCase):
    def setUp(self):# Set up function to create an instance of SeriDoc
        self.TV = SeriDoc(
            title="Breaking Bad",
            creator="Vince Gilligan",
            rating=9.5,
            synopsis="A high school chemistry teacher...",
            release_date="2008-01-20",
            runtime=47,
            num_seasons=5,
            num_episodes=62,
            status="Ended"
        )
    
    def testTVAtt(self):
        self.assertEqual(self.TV.title, "Breaking Bad")
        self.assertEqual(self.TV.creator, "Vince Gilligan")
        self.assertEqual(self.TV.rating, 9.5)
        self.assertEqual(self.TV.synopsis, "A high school chemistry teacher...")
        self.assertEqual(self.TV.release_date, "2008-01-20")
        self.assertEqual(self.TV.runtime, 47)
        self.assertEqual(self.TV.num_seasons, 5)
        self.assertEqual(self.TV.num_episodes, 62)
        self.assertEqual(self.TV.status, "Ended")
        self.assertEqual(self.TV.type, "TV Series")

    # If the attribute tests pass, the str, repr and get type are not needed to test

class TestDirector(unittest.TestCase):
    def setUp(self): # Set up function to create an instance of Director
        self.Dir = Director("Quentin Tarantino")
    
    def testDirAtt(self):
        self.assertEqual(self.Dir.name, "Quentin Tarantino")
        self.assertEqual(self.Dir.nbMovies, 0)
        self.assertEqual(self.Dir.bibli, [])
    
    def testAdd(self):
        movie = MvDoc("Pulp Fiction", "Quentin Tarantino", 8.9, "A Bad MF...", "1994-10-14", 154)
        self.Dir.add(movie)
        self.assertEqual(self.Dir.nbMovies, 1)
        self.assertIn(movie, self.Dir.bibli)
    
class TestCreator(unittest.TestCase):
    def setUp(self): # Set up function to create an instance of Creator
        self.Crt = Creator("Vince Gilligan")
    
    def testCrtAtt(self):
        self.assertEqual(self.Crt.name, "Vince Gilligan")
        self.assertEqual(self.Crt.nbSeries, 0)
        self.assertEqual(self.Crt.bibli, [])
    
    def testAdd(self):
        series = SeriDoc("Breaking Bad", "Vince Gilligan", 9.5, "A high school chemistry teacher...", "2008-01-20", 47, 5, 62, "Ended")
        self.Crt.add(series)
        self.assertEqual(self.Crt.nbSeries, 1)
        self.assertIn(series, self.Crt.bibli)

    