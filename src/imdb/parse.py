"""A utility to handle IMDB data.

See https://www.imdb.com/interfaces/.
"""

import logging
import sqlite3

from .. import app


# table name, file name
FILES = [
    ("names", "name.basics.tsv"),
    ("principals", "title.principals.tsv"),
    ("ratings", "title.ratings.tsv"),
    ("titles", "title.basics.tsv")]


def read_header(filename):
    with open(filename, "r") as file_:
        return next(file_).split("\t")


def read_tsv(filename):
    with open(filename, "r") as file_:
        keys = next(file_).split("\t")
        for line in file_:
            fields = line.split("\t")
            fields = [f.strip() for f in fields]
            fields = [None if f == "\\N" or not f else f for f in fields]
            yield dict(zip(keys, fields))


def name_predicate(name_dict):
    """Only include names that pass this predicate."""
    professions = name_dict["primaryProfession"]
    return (
        professions and
        ("actor" in professions or
         "actress" in professions or
         "director" in professions))


def create_schema(conn, path):
    """Creates the database schema from file headers."""
    curs = conn.cursor()
    for table_name, file_name in FILES:
        cols = read_header(path + file_name)
        curs.execute(
            "CREATE TABLE %s (\n" % (table_name,) +
            ",\n".join("\t%s" % (col,) for col in cols) +
            "\n);")
    curs.execute("CREATE INDEX titles_by_titleid ON titles(tconst);")
    curs.execute("CREATE INDEX principals_by_titleid ON principals(tconst);")
    curs.execute("CREATE INDEX ratings_by_titleid ON ratings(tconst);")
    curs.execute("CREATE INDEX names_by_nameid ON names(nconst);")
    conn.commit()


def parse_data(conn, path):
    """Parses data from a directory into a sqlite database."""
    curs = conn.cursor()
    for table_name, file_name in FILES:
        logging.info("parsing %s...", table_name)
        cols = read_header(path + file_name)
        query = "INSERT INTO %s (%s) VALUES (%s);" % (
            table_name,
            ", ".join(cols),
            ", ".join("?" for _ in cols))

        for count, data in enumerate(read_tsv(path + file_name)):
            curs.execute(query, tuple(data.values()))
            if count and not count % 1e6:
                logging.info("parsed %s million %s rows...", count, table_name)

        logging.info("finished parsing %s", table_name)
    conn.commit()


def main(args):
    """Parse imdb data into a sqlite database."""
    conn = sqlite3.connect(args.data_path + args.database_uri)
    try:
        create_schema(conn, args.data_path)
        parse_data(conn, args.data_path)
    finally:
        conn.close()


def register(parser):
    """Register flags for main() above."""
    parser.add_argument(
        "--database-uri",
        help="sqlite database uri",
        default="imdb.db",
        dest="database_uri")
    parser.add_argument(
        "--data-path",
        help="path to imdb data files",
        default="data/imdb/",
        dest="data_path")


if __name__ == "__main__":
    app.run(main, register)
