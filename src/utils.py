""" utils module contains code related to operating system functions. """
import os
import json
import os.path
from src.system_objects import Movie, Sample, Person
from tinydb import TinyDB, Query
import pandas as pd #for returning the sample features
import os.path #to check if file exist

class SampleLoader(object):
    """ SampleLoader is responsible for aiding the load process of individual
    sample data from our directory.
    """

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


class SampleController(object):
    """Sample Controller handles crud operations for the sample dataset."""    
    def __init__(self, sample_dir="./data/"):        
        self.sample_dir = sample_dir
        self._init = False
        self.data = {}

    def init(self):
        self.read_dirs()

    def getSamplesByPerson(self, personId):
        return [{"id": id, **self.data[id]} for id in self.data if self.data[id]["subject_name"] == int(personId)]

    def getSamplesByMovie(self, movieId):
        return [{"id": id, **self.data[id]} for id in self.data if self.data[id]["movie_id"] == movieId]

    def getSampleIdsByMovie(self, movieId):
        return [id for id in self.data if self.data[id]["movie_id"] == movieId]

    def getSampleIdsByPerson(self, personId):
        return [id for id in self.data if self.data[id]["subject_name"] == int(personId)]


    def read_dirs(self):
        """  Fetch all the directories in data folder and store it in class variables.    
        """
        self.dirs = [os.path.join(self.sample_dir, f) for f in os.listdir(self.sample_dir) 
               if os.path.isdir(os.path.join(self.sample_dir,f))]
        self._ids = [x[len(self.sample_dir):] for x in self.dirs if os.path.isfile(x+"/meta.json") ]
       
        for k in self._ids:
            self.data[k] = (self.read_metadata(k))            

        self.__init = True

    def list_all(self):
        if not self._init:
            self.read_dirs()        
        return self._ids

    def read_metadata(self, _id):
        #with openself.dir+_id
        d = []
        with open(self.sample_dir+_id+'/meta.json', 'r') as fp:
            data = json.load(fp)
            d.append(data)
        return d[0]

    def get_metadata(self, _id):
        return self.data[_id]

    def getFeatures(self, sample_id, metrics="emotions"):
        """
        metrics: 'emotions', 'eda', 'affdex.facs', 'affdex.age', "affdex.va", "affdex.emotions"
        """
        if metrics=="emotions":
            sample_file = self.sample_dir+sample_id+"/cat_face_emotions.csv"
            if not os.path.exists(sample_file):
                return None
            return pd.read_csv(sample_file, header=0, index_col=0)
        if len(metrics) > len("affdex") and metrics[:6] == "affdex":
            sample_file = self.sample_dir+sample_id+"/affdex_output/features.csv"
            arg_split = metrics.split(".")
            param = ""
            df = pd.read_csv(sample_file, header=0, index_col=0)
            if len(arg_split)==2:
                param = arg_split[1]
            if param == "va":
                return df[["timestamp","valence","engagement"]]
            elif param == "facs":
                return df[["timestamp","facs", "attention", "eyeWiden"]]
            elif param == "emotions":
                return df[["timestamp","facs", "attention", "eyeWiden"]]
            return df[["timestamp","joy","fear" "anger","contempt","disgust","sadness","surprise"]]
        return None
        
    def hasFeatures(self, sample_id, feature_type):
        """
        returns whether given feature is implemented.
        """
        pass

class PersonController(object):
    """
    Responsible for providing data access methods
    related to people in the system.
    """
    def __init__(self, data_dir="./data/"):
        self.db = TinyDB(data_dir+"db.json")
        self.table = self.db.table("person")

    def createPerson(self, *args):
        return Person(*args)

    def getPerson(self, id):
        Person = Query()
        return self.table.get(Person.id == id) 

    def savePerson(self, person):
        if person.id is None:            
            id = self.table.insert(person.__dict__)            
            self.table.update({"id": id}, doc_ids=[id])
        else:            
            self.table.update(person.__dict__, doc_ids=[person.id])   

    def removePerson(self, person_id):
        self.table.remove(doc_ids=[person_id])

    def getAll(self):
        return self.table.all()
    


class MovieController(object):
    def __init__(self, movie_dir="./movies/"):
        self.movie_dir = movie_dir
        self.metadatafile = "movie_index.json"
        self.files = []
        self.metadata = None
        self.data = []
        self.__init = False
        self.indexed_data = {}
        self.indexed_data2 = {}

    def init(self):
        self.read_files()

    def get_dir(self):
        return self.movie_dir

    def read_files(self):
        """  Fetch all the directories in data folder and store it in class variables.    
        """
        valid_filetypes = [".mp4", ".avi", "webm"]
        self.files = [f for f in os.listdir(self.movie_dir) if f[-4:] in valid_filetypes ]
        self.readMetadata()
        
        self.data = []
        for f in self.files:
            row = Movie(f)
            
            try:
                md  = self.metadata[f]
                row = Movie(f, md['name'],
                            genre=md['genre'], year=md['year'],
                            tags=md["tags"],
                            id = md["id"]
                )               
                self.indexed_data[md["id"]] = md
                self.indexed_data2[md["id"]] = row
            except KeyError:
                pass
            self.data.append(row)
        return self.files

    def getMovieByFile(self, filename):
        if "/" in filename:
            filename = filename[filename.rindex("/")+1:]
            
        try:
            return self.metadata[filename]
        except KeyError:
            return self.indexed_data[filename]
        
    def getMovieObjById(self, _id):
        return self.indexed_data2[_id]
        
    def updateMetadata(self):
        with open(self.movie_dir+self.metadatafile, 'w') as fp:
            json.dump(self.metadata, fp)            


    """Adds the metadata of a movie given a movie file"""
    def addMovie(self, movie):        
        self.metadata[movie.movie] = movie.getAttributes()
    
    def readMetadata(self):
        d = []
        with open(self.movie_dir+self.metadatafile, 'r') as fp:
            data = json.load(fp)
            d.append(data)
        self.metadata=d[0]
        return d[0]

    def listMovies(self):
        if self.__init == False:
            self.read_files()
            self.__init = True
        return [m.getAttributes() for m in self.data]
            
    
if __name__ == "__main__":
    #sys = SampleController()
    #s = "1d989665-80ae-4bff-bf59-b5f7691fb3b9"
    #sys.read_dirs()
    #print(sys.get_metadata(s))

    sys = MovieController()
    sys.read_files()
    #print(len(sys.readMetadata()))
