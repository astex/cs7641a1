"""Fit california housing data using SVMs."""

import sklearn.svm
from .. import data as datalib


SIZE_STEP = .01

GAMMA_MIN = -3
GAMMA_MAX = 3
GAMMA_STEP = .5

C_MIN = -1
C_MAX = 5
C_STEP = .5


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_STEP
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.svm.SVC(gamma=10**-.5, C=4)
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_STEP


def plot_gamma(data, plotter):
    ldata, tdata = datalib.partition(data, (.2, .2))
    gamma = GAMMA_MIN
    while gamma < GAMMA_MAX:
        classifier = sklearn.svm.SVC(gamma=10**gamma)
        plotter.plot(classifier, gamma, ldata, tdata)
        gamma += GAMMA_STEP


def plot_c(data, plotter):
    ldata, tdata = datalib.partition(data, (.2, .2))
    c = C_MIN
    while c < C_MAX:
        classifier = sklearn.svm.SVC(gamma="scale", C=10**c)
        plotter.plot(classifier, c, ldata, tdata)
        c += C_STEP


def register():
    datalib.register_plotfunc("svm", "size", plot_size)
    datalib.register_plotfunc("svm", "gamma", plot_gamma)
    datalib.register_plotfunc("svm", "c", plot_c)
