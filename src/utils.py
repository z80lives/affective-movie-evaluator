class SampleLoader:
    def __init__(self, filename):
        #self._dir = "./data/"+filename+"/"
        f = filename
        if f[-1] != '/':
            f = f + "/"
        self._dir = f

    def getVideoFile(self):
        return self._dir+"test.avi"

    def getDir(self):
        return self._dir
