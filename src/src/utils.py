class SampleLoader:
    def __init__(self, filename):
        #self._dir = "./data/"+filename+"/"
        self._dir = filename

    def getVideoFile(self):
        return self._dir+"test.avi"

    def getDir(self):
        return self._dir
