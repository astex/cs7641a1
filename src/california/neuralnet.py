"""Fit california housing data to a neural net."""

import pygal
import sklearn.neural_network
from .. import app
from .. import data as datalib
from . import data as caldata


SIZE_INTERVAL = .01
MAX_ITER = 400
ITER_STEP = 20
MAX_HIDDEN = 40
HIDDEN_STEP = 1


def plot_size(tdata, ldata, outdir):
    lerr = []
    terr = []

    size = SIZE_INTERVAL
    while size < 1.01:
        data, _ = datalib.partition(size, *ldata)
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(8,))
        classifier.fit(*data)
        lerr.append((size, 1 - classifier.score(*data)))
        terr.append((size, 1 - classifier.score(*tdata)))
        size += SIZE_INTERVAL

    plot = pygal.XY(stroke=False)
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/neraulnet_size.svg")


def plot_iter(tdata, ldata, outdir):
    lerr = []
    terr = []

    for max_iter in range(ITER_STEP, MAX_ITER, ITER_STEP):
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(8,),
            max_iter=max_iter)
        classifier.fit(*ldata)
        lerr.append((max_iter, 1 - classifier.score(*ldata)))
        terr.append((max_iter, 1 - classifier.score(*tdata)))

    plot = pygal.XY(stroke=False)
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/neuralnet_iter.svg")


def plot_hidden(tdata, ldata, outdir):
    lerr = []
    terr = []

    for hidden in range(HIDDEN_STEP, MAX_HIDDEN, HIDDEN_STEP):
        classifier = sklearn.neural_network.MLPClassifier(
            hidden_layer_sizes=(hidden,))
        classifier.fit(*ldata)
        lerr.append((hidden, 1 - classifier.score(*ldata)))
        terr.append((hidden, 1 - classifier.score(*tdata)))

    plot = pygal.XY(stroke=False)
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/neuralnet_hidden.svg")


PLOTFUNCS = {
    "size": plot_size,
    "iter": plot_iter,
    "hidden": plot_hidden,
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
