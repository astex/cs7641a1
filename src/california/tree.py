"""Fit california housing data to a tree."""

import sklearn.tree
from .. import data as datalib


MAX_DEPTH = 26
SIZE_INTERVAL = .01

ALPHA_STEP = .01
ALPHA_MAX = .2


def plot_depth(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))
    for depth in range(1, MAX_DEPTH):
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=depth)
        plotter.plot(classifier, depth, ldata, tdata)


def plot_depth_entropy(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))
    for depth in range(1, MAX_DEPTH):
        classifier = sklearn.tree.DecisionTreeClassifier(
            max_depth=depth,
            criterion="entropy")
        plotter.plot(classifier, depth, ldata, tdata)


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_INTERVAL
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=8)
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_INTERVAL


def plot_ccp_alpha_prune(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    alpha = ALPHA_STEP
    while alpha < ALPHA_MAX:
        classifier = sklearn.tree.DecisionTreeClassifier(
            max_depth=8,
            ccp_alpha=alpha)
        plotter.plot(classifier, alpha, ldata, tdata)
        alpha += ALPHA_STEP


def register():
    datalib.register_plotfunc("tree", "depth", plot_depth)
    datalib.register_plotfunc("tree", "size", plot_size)
    datalib.register_plotfunc("tree_prune", "alpha", plot_ccp_alpha_prune)
    datalib.register_plotfunc("tree_entropy", "depth", plot_depth_entropy)
