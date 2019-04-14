##tests directory path finder scripts loader
import unittest

from src.utils import SampleLoader, SampleController
#from src.src.utils import SampleLoader

sys = SampleLoader("./data/test/")

class TestSampleLoader(unittest.TestCase):
    def testgetDir(self):
        assert sys._dir == "./data/test/"

    def testGetVideoFile(self):
        assert sys.getVideoFile() == "./data/test/test.avi"

    """ Test whether the path finder works regardless of the final backslash """
    def testDirSlash(self):
        s = SampleLoader("./data/test")
        assert s._dir == "./data/test/"
        assert s.getVideoFile() == "./data/test/test.avi"

        s = SampleLoader("./data/test/")
        assert s._dir == "./data/test/"
        assert s.getVideoFile() == "./data/test/test.avi"

        

class TestSampleController(unittest.TestCase):
    def test1(self):
        expected_result = ['661737f0-3bf4-41ac-9c5e-a9f2147086d6', '1d989665-80ae-4bff-bf59-b5f7691fb3b9']
        sys = SampleController("./tests/data/")
        assert expected_result == sys.list_all()
        
if __name__ == "__main__":
    unittest.main()
