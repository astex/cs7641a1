"""Fit california housing data using gradient descent boosting."""

import pygal
import sklearn.ensemble
from .. import app
from .. import data as datalib
from . import data as caldata


SIZE_STEP = .01
EST_STEP = 10
EST_MAX = 400
RATE_STEP = .01
RATE_MAX = .99


def plot_size(tdata, ldata, outdir):
    lerr = []
    terr = []

    size = SIZE_STEP
    while size < 1.01:
        data, _ = datalib.partition(size, *ldata)
        classifier = sklearn.ensemble.GradientBoostingClassifier()
        classifier.fit(*data)
        lerr.append((size, 1 - classifier.score(*data)))
        terr.append((size, 1 - classifier.score(*tdata)))
        size += SIZE_STEP

    plot = pygal.XY(
        stroke=False,
        x_title="data_portion",
        y_title="score")
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/boosting_size.svg")


def plot_est(tdata, ldata, outdir):
    lerr = []
    terr = []

    for est in range(EST_STEP, EST_MAX, EST_STEP):
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            n_estimators=est)
        classifier.fit(*ldata)
        lerr.append((est, 1 - classifier.score(*ldata)))
        terr.append((est, 1 - classifier.score(*tdata)))

    plot = pygal.XY(
        stroke=False,
        x_title="n_estimators",
        y_title="score")
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/boosting_est.svg")


def plot_rate(tdata, ldata, outdir):
    lerr = []
    terr = []

    rate = RATE_STEP
    while rate < RATE_MAX:
        classifier = sklearn.ensemble.GradientBoostingClassifier(
            learning_rate=rate)
        classifier.fit(*ldata)
        lerr.append((rate, 1 - classifier.score(*ldata)))
        terr.append((rate, 1 - classifier.score(*tdata)))
        rate += RATE_STEP

    plot = pygal.XY(
        stroke=False,
        x_title="learning_rate",
        y_title="score")
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/boosting_rate.svg")


PLOTFUNCS = {
    "size": plot_size,
    "est": plot_est,
    "rate": plot_rate,
}


def main(args):
    data = caldata.get_data(args.datadir)
    data = caldata.make_boolean(data)
    tdata, ldata = datalib.partition(args.testprob, *data)
    PLOTFUNCS[args.plotfunc](tdata, ldata, args.outdir)


def register(parser):
    parser.add_argument(
        "--datadir",
        help="cache directory for scikit data",
        default="data/california")
    parser.add_argument(
        "--testprob",
        help="probability of a sample being used for testing",
        type=float,
        default=.2)
    parser.add_argument(
        "--outdir",
        help="dir for output plots",
        default="data/california")
    parser.add_argument(
        "plotfunc",
        help="variable to plot against",
        choices=PLOTFUNCS)


if __name__ == "__main__":
    app.run(main, register)
