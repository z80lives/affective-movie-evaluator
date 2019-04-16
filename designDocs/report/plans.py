def makeStr(data):
    return "\n".join(data)
def plan1():
    overview = "The purpose of the SampleLoader is to aid the SampleController load the Sample\n" +"files from the directory. Inspite of it's name the actual responsibility  of\n" + "the class is to resolve the directory path of of a sample folder and nothing else."

    inp = "Input 'param1' will passed as argument 1 of the constructor. \n" + " sys = SampleLoader(param1) "                                  
    op = ""
    
    lf = """ 
\\begin{minted}{python}
  class SampleLoader(object):
    \"\"\" SampleLoader is responsible for aiding the load process of individual
    sample data from our directory.
    \"\"\"

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
\\end{minted}
"""                                                 
    data_desc = """
\\begin{itemize}
  \\item \\path{./data/test/}
  \\item \\path{./data/test/}
\\end{itemize}
"""
    pve = """
\\begin{itemize}
 \\item CASE 1: testGetDir()           
 \\item CASE 2: testGetVideoFile() 
 \\item CASE 3: testDirSlash()     
\end{itemize}l
"""
    nve = "None"
    int_mod = "Python unittest"
    tools="Test Tools"

    data = [overview, inp, op, lf, data_desc, pve, nve, int_mod, tools]
    return data
