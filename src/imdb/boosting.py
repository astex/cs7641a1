"""Fit california housing data using gradient descent boosting."""

import sklearn.ensemble
from .. import data as datalib


SIZE_STEP = .01
EST_STEP = 10
EST_MAX = 400
RATE_STEP = .01
RATE_MAX = .99


def plot_size(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    size = SIZE_STEP
    while size < 1.01:
        data, = datalib.partition(ldata, (size,))
        classifier = sklearn.ensemble.GradientBoostingClassifier()
        plotter.plot(classifier, size, data, tdata)
        size += SIZE_STEP


def plot_est(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    for est in range(EST_STEP, EST_MAX, EST_STEP):
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            n_estimators=est)
        plotter.plot(classifier, est, data, tdata)


def plot_rate(data):
    ldata, tdata = datalib.partition(data, (.8, .2))

    rate = RATE_STEP
    while rate < RATE_MAX:
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            learning_rate=rate)
        plotter.plot(classifier, size, data, tdata)
        rate += RATE_STEP


def register():
    datalib.register_plotfunc("boosting", "size", plot_size)
    datalib.register_plotfunc("boosting", "n_estimators", plot_est)
    datalib.register_plotfunc("boosting", "learning_rate", plot_rate)
