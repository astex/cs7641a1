"""Fit california housing data using SVMs."""

import pygal
import sklearn.svm
from .. import app
from .. import data as datalib
from . import data as caldata


SIZE_STEP = .01


def plot_size(tdata, ldata, outdir):
    logging.info("plotting size...")
    lerr = []
    terr = []

    size = SIZE_STEP
    while size < 1.01:
        data, _ = datalib.partition(size, *ldata)
        classifier = sklearn.svm.NuSVC(gamma="scale")
        classifier.fit(*data)
        lerr.append((size, 1 - classifier.score(*data)))
        terr.append((size, 1 - classifier.score(*tdata)))
        logging.trace("plotted size %s", size)
        size += SIZE_STEP

    plot = pygal.XY(
        stroke=False,
        x_title="data_portion",
        y_title="error")
    plot.add("training", lerr)
    plot.add("testing", terr)
    plot.render_to_file(outdir + "/svm_size.svg")


PLOTFUNCS = {
    "size": plot_size,
}


def main(args):
    data = caldata.get_data(args.datadir)
    data = caldata.normalize(data)
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
