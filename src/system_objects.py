class Movie:
    def __init__(self):
        self.name = ""
        self.genre = ""
        self.averageRating = 0.0
        self.currentRating = 0.0

class Sample:
    def __init__(self, filename, subject, movie, size, length):
        self.filename = filename
        self.subject = subject
        self.movie = Movie()
        self.size = 0.0
        self.length = 0.0
