"""Classify california housing data using k-Nearest Neighbors."""

import sklearn.neighbors
from .. import data as datalib


N_MAX = 20


def plot_n_dist(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    for n in range(1, N_MAX + 1):
        classifier = sklearn.neighbors.KNeighborsClassifier(
            n_neighbors=n,
            p=1,
            weights="distance")
        plotter.plot(classifier, n, ldata, tdata)


def plot_n_uniform(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    for n in range(1, N_MAX + 1):
        classifier = sklearn.neighbors.KNeighborsClassifier(
            n_neighbors=n,
            p=1,
            weights="uniform")
        plotter.plot(classifier, n, ldata, tdata)


def register():
    datalib.register_plotfunc("knn", "n_neighbors_distance", plot_n_dist)
    datalib.register_plotfunc("knn", "n_neighbors_uniform", plot_n_uniform)
