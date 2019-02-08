"""Fits the imdb data using various learners."""

import logging
import pygal
from sklearn import tree
import sqlite3

from .. import app
from . import read


TEST_SIZE = .2


def score(conn, depth):
    """Scores the dataset at a given probability of choice."""
    data = read.load_dataset(conn, .01)
    # scikit-learn doesn't understand null.
    data.labels = [l or 0 for l in data.labels]
    avg = sum(data.labels) / len(data.labels)
    # determine if the rating is above average or not (for easier scoring)
    data.labels = [1 if l > avg else -1 for l in data.labels]

    test_data, train_data = data.partition(.2)
    classifier = tree.DecisionTreeClassifier(max_depth=depth)
    classifier.fit(train_data.samples, train_data.labels)
    return (
        classifier.score(test_data.samples, test_data.labels),
        classifier.score(train_data.samples, train_data.labels))


def main(args):
    conn = sqlite3.connect(args.database_uri)
    lscores = []
    tscores = []
    try:
        depth = 1
        while depth < 50:
            lscore, tscore = score(conn, depth)
            lscores.append((depth, lscore))
            tscores.append((depth, tscore))
            logging.info("scored depth %s", depth)
            depth += 1
    finally:
        conn.close()

    plot = pygal.XY(stroke=False)
    plot.add("training set", lscores)
    plot.add("testing set", tscores)
    plot.render_to_file("data/imdb/tree_depth.svg")


def register(parser):
    """Register flags for main() above."""
    parser.add_argument(
        "--database-uri",
        help="sqlite database uri",
        default="data/imdb/imdb.db",
        dest="database_uri")


if __name__ == "__main__":
    app.run(main, register)
