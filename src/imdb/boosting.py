"""Fit california housing data using gradient descent boosting."""

import sklearn.ensemble
from .. import data as datalib


SIZE_STEP = .01
EST_STEP = 10
EST_MAX = 400
RATE_STEP = .01
RATE_MAX = .99

DEPTH_MAX = 10

ALPHA_STEP = .001
ALPHA_MAX = .05


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
        plotter.plot(classifier, est, ldata, tdata)


def plot_rate(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))

    rate = RATE_STEP
    while rate < RATE_MAX:
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            learning_rate=rate)
        plotter.plot(classifier, rate, ldata, tdata)
        rate += RATE_STEP


def plot_depth(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))
    for depth in range(1, DEPTH_MAX + 1):
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            max_depth=depth)
        plotter.plot(classifier, depth, ldata, tdata)


def plot_alpha(data, plotter):
    ldata, tdata = datalib.partition(data, (.8, .2))
    alpha = ALPHA_STEP
    while alpha < ALPHA_MAX:
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            ccp_alpha=alpha)
        plotter.plot(classifier, alpha, ldata, tdata)
        alpha += ALPHA_STEP


def register():
    datalib.register_plotfunc("boosting", "size", plot_size)
    datalib.register_plotfunc("boosting", "n_estimators", plot_est)
    datalib.register_plotfunc("boosting", "learning_rate", plot_rate)
    datalib.register_plotfunc("boosting", "ccp_alpha", plot_alpha)
    datalib.register_plotfunc("boosting", "max_depth", plot_depth)
