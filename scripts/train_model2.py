from src.utils import MovieController, SampleController, PersonController
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm


def feature_to_histogram(time_series, window_size=200, bins=10):
    time_range = (0, len(time_series))
    last_time = 0
    feature_history_slices = []
    histogram_slices = []
    for time_start in range(*time_range, window_size):
        time_end = time_start+window_size
        if time_end > time_range[1]:
            time_end = time_range[1]
        time_slice = np.arange(time_start, time_end)
        w = time_series[time_start:time_end]
        #plt.plot(time_slice, w)
        feature_history_slices.append(w)
        histogram_slices = np.histogram(w, bins=bins)
    return feature_history_slices, histogram_slices

movie_controller = MovieController()
movie_controller.read_files()
sample_controller = SampleController()
sample_controller.read_dirs()
person_controller = PersonController() #actually uses TinyDB

#movie_id = "1"

#movie = movie_controller.getMovieObjById(movie_id)
sample_list = []
for movie in movie_controller.data:    
    samples =sample_controller.getSamplesByMovie(movie.id)
    sample_list.append(samples)
samples = np.concatenate(sample_list)


X = []
y = []
for sample in samples:
    features = sample_controller.getFeatures(sample["id"], metrics="affdex.va")
    target = sample_controller.data[sample["id"]]["score_5"] 
    eng = features["engagement"]
    t = np.arange(len(eng))
    time_slices, histograms = feature_to_histogram(eng)
    histograms = np.concatenate(histograms)
    X.append(histograms)
    y.append(target)

#plt.hist(time_slices[3], bins=10)
#plt.show()

#plt.plot(t, x1[:,0], "pink")
#X = np.array(df_concat.values)


kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
y_kmeans = kmeans.predict(X)
X = np.array(X)

cols = np.uint8(y)
#plt.scatter(X[:,1], X[:,2], c=cols, cmap='viridis')
#plt.show()

from sklearn.decomposition import PCA
X = np.array(X)
pca = PCA(n_components=2)
X_t = pca.fit_transform(X) 
#plt.scatter(X_t[:,0], X_t[:,1], c=cols, cmap='viridis')
#plt.show()
from sklearn.metrics import r2_score

from sklearn import linear_model
reg = linear_model.Ridge(alpha=.5)
reg.fit(X, y) 
y_hat = reg.predict(X)
r2 = r2_score(y, y_hat) 
print("Linear model (RIDGE) r2= ", r2)
#np.save("./models/ridge_model.npy", reg)

from sklearn import linear_model
reg = linear_model.SGDRegressor(max_iter=1000)
reg.fit(X, y) 
y_hat = reg.predict(X)
r2 = r2_score(y, y_hat) 
print("Linear model (SGD) r2= ", np.round(r2,3))


from sklearn.ensemble import GradientBoostingRegressor
reg = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0, loss='ls')
reg.fit(X, y) 
y_hat = reg.predict(X)
r2 = r2_score(y, y_hat) 
print("Gradient boost r2= ", np.round(r2,3))

from sklearn.neural_network import MLPRegressor
reg = MLPRegressor()
reg.fit(X, y) 
y_hat = reg.predict(X)
r2 = r2_score(y, y_hat) 
print("Neural Network(MLP) Regressor r2= ", np.round(r2,3))

from sklearn import svm
reg = svm.SVR(gamma="auto")
reg.fit(X, y) 
y_hat = reg.predict(X)
r2 = r2_score(y, y_hat) 
print("Support Vector Regressor model r2= ", r2)

#arr = np.array(demotions)
#X = []
#for df in demotions:
#    X.append(df.values)

#X = np.array(X)
#np.save("./alive_in_joburg.npy", X)

#print(kmeans)

#plt.scatter(X[:, 0], X[:, 1], s=50, cmap='viridis')
#demotions[0].plot()
#demotions[2].plot()
#plt.show()
#print(person_controller.getPerson(3))
