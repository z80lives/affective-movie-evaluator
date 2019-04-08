##tests directory path finder scripts loader
import unittest

from src.utils import SampleLoader
#from src.src.utils import SampleLoader

sys = SampleLoader("./data/test/")

class TestSampleLoader(unittest.TestCase):
    def testgetDir(self):
        assert sys._dir == "./data/test/"

    def testGetVideoFile(self):
        assert sys.getVideoFile() == "./data/test/test.avi"

    def testDir2(self):
        s = SampleLoader("./data/1234")
        #assert sys._dir == "./data/1234/"
        #assert sys.getVideoFile() == "./data/1234/test.avi"
        

if __name__ == "__main__":
    unittest.main()
