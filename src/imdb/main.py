"""Run analyses on imdb data."""

import logging
import sqlite3

from .. import app
from .. import data as datalib

from . import boosting
from . import knn
from . import neuralnet
from . import read as readlib
from . import svm
from . import tree


def register(parser):
    boosting.register()
    knn.register()
    neuralnet.register()
    svm.register()
    tree.register()

    parser.add_argument(
        "--database_uri",
        help="cache directory for scikit data",
        default="data/imdb/imdb.db")
    parser.add_argument(
        "--outdir",
        help="dir for output plots",
        default="paper/plots/imdb")
    parser.add_argument(
        "--cachedir",
        help="dir for cache files",
        default="data/imdb")
    parser.add_argument(
        "plotfuncs",
        nargs="+",
        help="variables to plot against",
        choices=datalib.get_plotfuncs() + ["all"])


def main(args):
    logging.info("prepping data...")
    conn = sqlite3.connect(args.database_uri)
    try:
        data = readlib.get_data(conn, args.cachedir)
    finally: 
        conn.close()
    data = datalib.normalize(data)
    # Filter out null ratings.
    data = tuple(zip(*[(s, l) for s, l in zip(*data) if l != -1]))

    plotfuncs = (
        datalib.get_plotfuncs() if args.plotfuncs == ["all"] else
        args.plotfuncs)

    for plotfunc in plotfuncs:
        plot = datalib.get_plotfunc(plotfunc)
        xtitle = datalib.get_xtitle(plotfunc)

        logging.info("plotting %s...", plotfunc)
        plotter = datalib.Plotter(xtitle)
        try:
            plot(data, plotter)
        except KeyboardInterrupt:
            logging.info("caught keyboard interrupt. plotting and continuing.")
            plotter.write(args.outdir, plotfunc)
            continue
        except Exception:
            logging.exception("error in %s. continuing...", plotfunc)
            continue

        plotter.write(args.outdir, plotfunc)


if __name__ == "__main__":
    app.run(main, register)
