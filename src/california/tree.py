"""Fit california housing data to a tree."""

import pygal
import sklearn.tree
from .. import app
from .. import data as datalib
from . import data as caldata


MAX_DEPTH = 26
SIZE_INTERVAL = .01


def plot_depth(tdata, ldata, outdir):
    lerr = []
    terr = []

    for depth in range(1, MAX_DEPTH):
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=depth)
        classifier.fit(*ldata)
        lerr.append((depth, 1 - classifier.score(*ldata)))
        terr.append((depth, 1 - classifier.score(*tdata)))

    plot = pygal.XY(stroke=False)
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/tree_depth.svg")


def plot_size(tdata, ldata, outdir):
    lerr = []
    terr = []

    size = SIZE_INTERVAL
    while size < 1.01:
        data, _ = datalib.partition(size, *ldata)
        classifier = sklearn.tree.DecisionTreeClassifier(max_depth=8)
        classifier.fit(*data)
        lerr.append((size, 1 - classifier.score(*data)))
        terr.append((size, 1 - classifier.score(*tdata)))
        size += SIZE_INTERVAL

    plot = pygal.XY(stroke=False)
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/tree_size.svg")


def main(args):
    tdata, ldata = caldata.get_data(args.datadir, args.testprob)
    tdata, ldata = caldata.make_boolean(tdata, ldata)

    plot_depth(tdata, ldata, args.outdir)
    plot_size(tdata, ldata, args.outdir)


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


if __name__ == "__main__":
    app.run(main, register)
