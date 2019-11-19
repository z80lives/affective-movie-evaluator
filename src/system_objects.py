class Movie:
    def __init__(self, filename,
                 name="", genre="", year="",
                 ar=0.0, cr=0.0, youtube=None,
                 internetScore=None,
                 tags="",
                 id=None
    ):
        self.id = id
        self.filename = filename
        self.name = name
        self.genre = genre
        self.year=year
        self.averageRating = ar
        self.currentRating = cr
        self.youtube = youtube
        self.internetScore = internetScore
        self.tags=tags

    def getAttributes(self):
        attr = {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "year": self.year,
            "averageRating": self.averageRating,
            "currentRating": self.currentRating,
            "filename": self.filename,
            "tags": self.tags
        }
        if self.youtube is not  None:
            attr["youtube"] = self.youtube
        if self.internetScore is not None:
            attr["internetScore"] = self.youtube
        return attr

    def __str__(self):
        return "(%s, %s, %s)" % (self.filename,
                                 self.name, self.genre )
    def __repr__(self):
        return self.__str__()

class Sample:
    def __init__(self, movie_file, filename, subject, size, length):
        self.filename = filename
        self.subject = subject
        self.movie = Movie(movie_file)
        self.size = size
        self.length = length

class Person:
    def __init__(self, id, name, gender, age="adult", occupation="Student"):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation

    def __str__(self):
        return "(%s, %s, %s, %s, %s)" % (self.id,
                                 self.name, self.gender, self.age, self.occupation)
    def __repr__(self):
        return self.__str__()