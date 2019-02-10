"""Fit california housing data using SVMs."""

import sklearn.svm
from .. import data as datalib


SIZE_STEP = .01


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_STEP
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.svm.NuSVC(gamma="scale")
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_STEP


def register():
    datalib.register_plotfunc("svm", "size", plot_size)
