"""Fit california housing data to a neural net."""

import sklearn.exceptions
import sklearn.neural_network
import warnings
from .. import data as datalib


SIZE_INTERVAL = .01
MAX_ITER = 400
ITER_STEP = 20
MAX_HIDDEN = 40
HIDDEN_STEP = 1


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_INTERVAL
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(8,))
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_INTERVAL


def plot_iter(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    for max_iter in range(ITER_STEP, MAX_ITER, ITER_STEP):
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(8,),
            max_iter=max_iter)
        plotter.plot(classifier, max_iter, ldata, tdata)


def plot_hidden(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    for hidden in range(HIDDEN_STEP, MAX_HIDDEN, HIDDEN_STEP):
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(hidden,))
        plotter.plot(classifier, hidden, ldata, tdata)


def register():
    warnings.simplefilter(
        "ignore",
        category=sklearn.exceptions.ConvergenceWarning)
    datalib.register_plotfunc("neuralnet", "size", plot_size)
    datalib.register_plotfunc("neuralnet", "max_iter", plot_iter)
    datalib.register_plotfunc("neuralnet", "hidden_size", plot_hidden)
