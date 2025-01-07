"""
Unit test class for SearchEngine module
"""
import unittest
from searchEngine import SearchEngine
from Corpus import MdCorpus as mdc
from MovieClasses import MvDoc, SeriDoc, Director, Creator
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd

class TestSearchEngine(unittest.TestCase):
    """
    Unit test class for SearchEngine
    """
    def setUp(self):
        self.corpus = mdc('TestMockCorpus')
        self.movie1 = MvDoc("Inception", "Christopher Nolan", "9.0 out of 10", "Movie about dreams", "July 16, 2010", "1h 30m")
        self.movie2 = MvDoc("The Dark Knight", "Christopher Nolan", "9.5 out of 10", "Test Synopsis for The Dark Knight", "July 18, 2008", "2h 30m")
        self.tv1 = SeriDoc("Breaking Bad", "Vince Gilligan", "9.7 out of 10", "Test Synopsis for Breaking Bad", "January 20, 2008", "47 minutes per episode", 5, 62, "Ended")

        self.corpus.addMedia(self.movie1)
        self.corpus.addMedia(self.movie2)
        self.corpus.addMedia(self.tv1)
        
        self.search = SearchEngine(self.corpus)

    def test_deep_clean(self):
        """
        Test the __deep_clean method of SearchEngine
        """
        text = "This is a test string with some punctuations, and stopwords like 'is' and 'a'."
        cleaned = self.search._SearchEngine__deep_clean(text)
        self.assertEqual(cleaned, "test string punctuations stopwords like")
    

    def test_create_matrix(self):
        """
        Test the create_matrix method of SearchEngine
        """
        vocab_size = len(self.search.Vocab)
        self.assertGreater(vocab_size, 0)
        self.assertEqual(self.search.mat_TF.shape, (3, 13))
        self.assertEqual(self.search.mat_TFxIDF.shape, (3, 13))
        self.assertIsInstance(self.search.mat_TF, csr_matrix)
        self.assertIsInstance(self.search.mat_TFxIDF, csr_matrix)
    
    def test_search_valid(self):
        """
        Test the search method with a valid query
        """
        res = self.search.search('Inception')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertGreater(len(res), 0)
        res1 = self.search.search('Christopher Nolan')
        self.assertEqual(len(res1), 2)

    def test_search_invalid(self):
        """
        Test the search method with an invalid query
        """
        res = self.search.search('Tarantino')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 0)