from src.utils import MovieController, SampleController, PersonController
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

import matplotlib.pyplot as plt

movie_controller = MovieController()
movie_controller.read_files()
sample_controller = SampleController()
sample_controller.read_dirs()
person_controller = PersonController() #actually uses TinyDB

movie_id = "1"

movie = movie_controller.getMovieObjById(movie_id)
samples = sample_controller.getSamplesByMovie(movie_id)

demotions = []
for sample in samples:
    demotions.append(sample_controller.getFeatures(sample["id"]))

df_concat = pd.concat(demotions)
#print(df_concat.describe())

X = np.array(df_concat.values)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X).transform(X)

#arr = np.array(demotions)
X = []
for df in demotions:
    X.append(df.values)

X = np.array(X)
np.save("./alive_in_joburg.npy", X)

#print(kmeans)

#plt.scatter(X[:, 0], X[:, 1], s=50, cmap='viridis')
#demotions[0].plot()
#demotions[2].plot()
#plt.show()
#print(person_controller.getPerson(3))
