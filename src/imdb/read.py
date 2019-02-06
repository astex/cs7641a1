"""A module to read imdb data into features."""

import itertools
import random
import sqlite3
from .. import app
from .. import data as data_lib


def get_titles(conn):
    """Gets the titles to consider for this problem.

    Only movies made in the last ten years are considered.

    Args:
        conn: A sqlite database connection.

    Returns:
        [(tconst, title), ...]
    """
    curs = conn.cursor()
    curs.execute(
        "SELECT tconst, primaryTitle FROM titles\n"
        "\tWHERE\n"
        "\t\tCAST(startYear AS INTEGER) > 2008 AND\n"
        "\t\ttitleType = \"movie\";")
    row = curs.fetchone()
    while row:
        yield row
        row = curs.fetchone()


def get_names(conn, nconsts):
    """Gets the names to use for this problem.

    Args:
        conn: A sqlite database connection.
        names: Only include names with these nconsts.

    Returns:
        [(nconst, name), ...]
    """
    curs = conn.cursor()
    curs.execute(
        "SELECT nconst, primaryName FROM names\n"
        "\tWHERE nconst IN (%s);" %
        (", ".join("?" for _ in nconsts)),
        nconsts)
    row = curs.fetchone()
    while row:
        yield row
        row = curs.fetchone()


def get_ratings(conn, tconsts):
    """Gets the rating of each of the indicated titles.

    Args:
        conn: A sqlite database connection.
        tconsts: Only include ratings for these tconsts.

    Returns:
        [(tconst, rating), ...]
    """
    curs = conn.cursor()
    curs.execute(
        "SELECT tconst, averageRating FROM ratings\n"
        "\tWHERE tconst IN (%s);" %
        (", ".join("?" for _ in tconsts)),
        tconsts)
    row = curs.fetchone()
    while row:
        yield row
        row = curs.fetchone()


def get_principals(conn, tconsts):
    """Gets the name/title associations for a list of titles.

    Only actors and directors are considered.

    Args:
        conn: A sqlite database connection.
        tconsts: Only include names for these tconsts.

    Returns:
        [(tconst, nconst), ...] sorted by tconst.
    """
    curs = conn.cursor()
    curs.execute(
        ("SELECT tconst, nconst FROM principals\n"
         "\tWHERE\n"
         "\t\ttconst IN (%s) AND\n"
         "\t\tcategory IN (\"actor\", \"director\", \"self\")\n"
         "\tORDER BY tconst;") %
        (", ".join("?" for _ in tconsts)),
        tconsts)
    row = curs.fetchone()
    while row:
        yield row
        row = curs.fetchone()


def load_dataset(conn, prob):
    """Load a uniform learning and test subset of titles from imdb.

    The features for each dataset are whether or not a given actor or director
    participated in the title.
    
    Args:
        conn: A sqlite database connection.
        prob: The probability of selecting a given title.

    Returns:
        A dataset populated from the database.
    """
    # [(tconst, title), ...]
    titles = [t for t in get_titles(conn) if random.uniform(0, 1) < prob]
    tconsts = [k for k, _ in titles]
    # {tconst: rating, ...}
    ratings = dict(
        (t, int(round(float(r))) if r else None) for t, r in
        get_ratings(conn, tconsts))
    # {tconst: [nconst, ...], ...}
    principals = {
        k: set(n for t, n in v)
        for k, v in itertools.groupby(
            get_principals(conn, tconsts),
            lambda p: p[0])}
    # {nconst: name, ...}
    names = dict(get_names(
        conn,
        list(set(n for ns in principals.values() for n in ns))))

    return data_lib.DataSet(
        ["%s is involved in the film." % (v,) for v in names.values()],
        [
            [n in principals.get(i, set()) for n in names.keys()]
            for i, _ in titles],
        [t for _, t in titles],
        [ratings.get(i, None) for i, _ in titles])


def main(args):
    """Load a dataset and print some stuff about it."""
    conn = sqlite3.connect(args.database_uri)
    try:
        data = load_dataset(conn, args.prob)
    finally:
        conn.close()
    print(
        ("N: %s\n"
         "M: %s\n"
         "First twenty names (with ratings and true feature count):\n%s\n"
         "First twenty features:\n%s\n") %
        (
            len(data.names),
            len(data.features),
            "\n".join(
                "\t%s (%s) (%s)" % (n, r, c) for n, r, c in
                zip(
                    data.names[:20],
                    data.labels[:20],
                    [len([f for f in fs if f]) for fs in data.features[:20]])),
            "\n".join("\t%s" % (f,) for f in data.features[:20])))


def register(parser):
    """Register flags for main() above."""
    parser.add_argument(
        "--database-uri",
        help="sqlite database uri",
        default="data/imdb/imdb.db",
        dest="database_uri")
    parser.add_argument(
        "--prob",
        help="probability of choosing a given title",
        default=.05,
        type=float,
        dest="prob")


if __name__ == "__main__":
    app.run(main, register)
