"""The main executable for california data."""

import logging
import sklearn.datasets

from .. import app
from .. import data as datalib

from . import boosting
from . import neuralnet
from . import svm
from . import tree


def get_data(datadir):
    """Gets california housing samples and labels."""
    return sklearn.datasets.fetch_california_housing(
        datadir,
        return_X_y=True)


def register(parser):
    boosting.register()
    neuralnet.register()
    svm.register()
    tree.register()

    parser.add_argument(
        "--datadir",
        help="cache directory for scikit data",
        default="data/california")
    parser.add_argument(
        "--outdir",
        help="dir for output plots",
        default="paper/plots/california")
    parser.add_argument(
        "plotfuncs",
        nargs="+",
        help="variables to plot against",
        choices=datalib.get_plotfuncs() + ["all"])


def main(args):
    logging.info("preping data...")
    data = get_data(args.datadir)
    data = datalib.normalize(data)
    data = datalib.make_boolean(data)

    plotfuncs = (
        datalib.get_plotfuncs() if args.plotfuncs == ["all"] else
        args.plotfuncs)

    for plotfunc in args.plotfuncs:
        plot = datalib.get_plotfunc(plotfunc)
        xtitle = datalib.get_xtitle(plotfunc)

        logging.info("plotting %s...", plotfunc)
        plotter = datalib.Plotter(xtitle)
        plot(data, plotter)

        plotter.learning_plot.render_to_file(
            args.outdir + "/%s.svg" % (plotfunc,))
        plotter.fit_timing_plot.render_to_file(
            args.outdir + "/%s_ftime.svg" % (plotfunc,))
        plotter.score_timing_plot.render_to_file(
            args.outdir + "/%s_stime.svg" % (plotfunc,))


if __name__ == "__main__":
    app.run(main, register)
