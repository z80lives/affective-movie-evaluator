import unittest

from src.utils import MovieController


class TestSampleLoader(unittest.TestCase):
    def testMovies(self):
        sys = MovieController()
        sys.readMetadata()
        movie_list = sys.listMovies()
        assert len(movie_list) == 2
    
