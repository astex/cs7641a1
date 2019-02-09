"""Fit california housing data to a tree."""

import sklearn.tree
from .. import data as datalib


MAX_DEPTH = 26
SIZE_INTERVAL = .01


def plot_depth(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))
    for depth in range(1, MAX_DEPTH):
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=depth)
        plotter.plot(classifier, depth, ldata, tdata)


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_INTERVAL
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=8)
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_INTERVAL


def register():
    datalib.register_plotfunc("tree", "depth", plot_depth)
    datalib.register_plotfunc("tree", "size", plot_size)
