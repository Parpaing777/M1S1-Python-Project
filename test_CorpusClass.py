"""
Unit tests for the Corpus module.
"""
import unittest
from Corpus import MdCorpus as mdc
from MovieClasses import MvDoc, SeriDoc, Director, Creator
import pandas as pd
import os

class TestMdCorpus(unittest.TestCase):
    """
    Unit test class for MdCorpus
    """
    def setUp(self):
        self.corpus = mdc('600Test')
        self.movie1 = MvDoc("Inception", "Christopher Nolan", "9.0 out of 10", "Movie about dreams", "July 16, 2010", "1h 30m")
        self.movie2 = MvDoc("The Dark Knight", "Christopher Nolan", "9.5 out of 10", "Test Synopsis for The Dark Knight", "July 18, 2008", "2h 30m")
        self.tv1 = SeriDoc("Breaking Bad", "Vince Gilligan", "9.7 out of 10", "Test Synopsis for Breaking Bad", "January 20, 2008", "47 minutes per episode", 5, 62, "Ended")

        self.corpus.addMedia(self.movie1)
        self.corpus.addMedia(self.movie2)
        self.corpus.addMedia(self.tv1)

    def test_addMedia(self):
        """
        Test the addMedia method of MdCorpus
        """       
        self.assertEqual(self.corpus.nmov, 2) # Check if the number of movies in the corpus is 2
        self.assertEqual(self.corpus.nser, 1) # Check if the number of TV series in the corpus is 1
        self.assertEqual(len(self.corpus.directors), 1) # Check if the number of directors in the corpus is 1. Same as checking ndir
        self.assertEqual(len(self.corpus.creators), 1)

    def test_show(self):
        """
        Test the show method of MdCorpus
        """
        self.corpus.show(2, 'title')
        self.corpus.show(2, 'date')
        self.corpus.show(2, 'rating')
        self.corpus.show(2, 'runtime')
        self.corpus.show(2, 'maker')

    def test_getTextData(self):
        """
        Test the get_textData method
        """
        text = self.corpus.get_textData()
        self.assertIn("Inception", text)
        self.assertIn("Movie about dreams", text)
        self.assertIn("Christopher Nolan", text)

    def test_search(self):
        """
        Test the search method of MdCorpus
        """
        res = self.corpus.Search('Inception')
        self.assertGreater(len(res), 0)
        res1 = self.corpus.Search('Christopher Nolan')
        self.assertEqual(len(res1), 2)
    
    def test_concorde(self):
        """
        Test the concorde method of MdCorpus
        """
        df = self.corpus.concorde('about') # Since the concorde method returns a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_clean_text(self):
        text = "Hello, World!\n"
        clean = self.corpus.clean_text(text)
        self.assertEqual(clean, "hello world ")

    def test_vocabularize(self):
        """
        Test the vocabularize method of MdCorpus
        """
        voc=self.corpus.vocabularize()
        self.assertGreater(len(voc), 0)
        self.assertIn('inception', voc)
        self.assertIn('christopher', voc)
        self.assertIn('dreams', voc)

    def test_stats(self):
        """
        Test the stats method of MdCorpus
        """
        stats = self.corpus.stats(nreturn=5)
        self.assertIsInstance(stats, dict)
        self.assertGreater(len(stats), 0)
    
    def test_save_load(self):
        """
        Test both the save and load methods of MdCorpus
        """
        filename = 'unittest10'
        # We will use the try finally block to ensure that the file is deleted after the test
        try:
            self.corpus.PKLsave(filename) # Save the corpus
            load = self.corpus.PKLload(filename) # Load the corpus
            # Check if the number of movies and TV series are the same
            self.assertEqual(self.corpus.nmov, load.nmov)
            self.assertEqual(self.corpus.nser, load.nser)
        
        finally:
            if os.path.exists(filename+'.pkl'):
                os.remove(filename+'.pkl')
        
    def tearDown(self):
        """
        Clean up method to delete the corpus after the tests
        """
        self.corpus = None
