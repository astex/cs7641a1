"""A module to read imdb data into features."""

import logging
import os


def listall(curs):
    """Yields results from cursor with appropriate nulls."""
    row = curs.fetchone()
    while row:
        row = tuple(r if r != "\\N" else None for r in row)
        yield row
        row = curs.fetchone()


def list_ratings(conn):
    """Yields from the ratings table.

    Args:
        conn: A sqlite connection.

    Yields:
        (tcons, rating)
    """
    curs = conn.cursor()
    curs.execute("SELECT tconst, averageRating FROM ratings;")
    for tconst, rating in listall(curs):
        rating = float(rating) if rating else None
        yield tconst, rating


def list_titles(conn):
    """Yields from the titles table.

    Args:
        conn: A sqlite connection.
    
    Yields:
        (tconst, title, year, runtime, genres)
    """
    curs = conn.cursor()
    curs.execute("""
        SELECT tconst, primaryTitle, startYear, runtimeMinutes, genres
            FROM titles
            WHERE titleType = "movie";
    """)
    for row in listall(curs):
        id_, title, year, runtime, genres = row
        genres = set(genres.split(',')) if genres else set()
        year = int(year) if year else None
        runtime = float(runtime) if runtime else None
        yield id_, title, year, runtime, genres


def list_name_counts(conn, rating):
    """Lists the number of big-name actors in each title.

    Only actors who have starred in at least five movies of higher-than-average
    rating are considered.

    Args:
        conn: A sqlite connection.
        rating: Only consider actors that have been in more than five movies
            with at least this rating.

    Yields:
        (tconst, count)
    """
    curs = conn.cursor()
    curs.execute("""
        SELECT p.tconst, count(*) FROM principals AS p
            WHERE p.nconst IN (
                SELECT nconst FROM (SELECT np.nconst, count(*) AS c
                    FROM principals AS np
                    INNER JOIN titles AS t ON t.tconst = np.tconst
                    INNER JOIN ratings AS r ON r.tconst = np.tconst
                    WHERE
                        t.titleType = "movie" AND
                        np.category IN ("actor", "self", "director") AND
                        CAST(r.averageRating AS REAL) > ?
                    GROUP BY np.nconst
                    HAVING c > ?))
            GROUP BY p.tconst;
    """, (rating, 5))
    yield from listall(curs)


def read_cache(cachedir):
    """Read results from a cache."""
    if (
            not os.path.isfile(cachedir + "/samples.csv") or
            not os.path.isfile(cachedir + "/labels.csv")):
        return None

    logging.info("reading from cache...")

    samples = []
    labels = []

    with open(cachedir + "/samples.csv", "r") as samplecache:
        for sample in samplecache:
            parsed_sample = []
            for i, s in enumerate(sample.split(",")):
                if i == 2:
                    parsed_sample.append(float(s))
                else:
                    parsed_sample.append(int(s))
            samples.append(parsed_sample)

    with open(cachedir + "/labels.csv", "r") as labelcache:
        labels.extend(int(l) for l in labelcache)

    return samples, labels


def write_cache(cachedir, samples, labels):
    """Write results to a cache."""
    with open(cachedir + "/samples.csv", "w+") as samplecache:
        samplecache.write(
            "\n".join(",".join(str(f) for f in s) for s in samples))
    with open(cachedir + "/labels.csv", "w+") as labelcache:
        labelcache.write("\n".join(str(l) for l in labels))


def get_data(conn, cachedir):
    """Gets some movie data from the database.

    Args:
        conn: A sqlite connection.

    Returns:
        (samples, labels)

        Samples is a 2D matrix where each row represents a movie title and each
        column is a feature as follows:

            - n_actors: The number of big name (in at least five movies with a
                higher-than-average rating) actors in the film.
            - year: The year the movie came out.
            - runtime: The runtime of the movie.
            - genre1, genre2, ...: Boolean (0/1) features indicating whether
              the movie is associated with a genre for all genres in the
              database. There are presently twenty-eight of these.

        Labels is a list indicating whether the sample with the same index has
        above-average (1), below-average (0), or no (-1) rating.
    """
    data = read_cache(cachedir)
    if data is not None:
        return data

    logging.info("getting ratings...")
    ratings = dict(list_ratings(conn))

    logging.info("getting titles...")
    titles = list(list_titles(conn))
    titles = [(i, _, y, r, gs) for i, _, y, r, gs in titles if y and r]
    tconsts = {i for i, _, _, _, _ in titles}
    genres = list(set(g for _, _, _, _, gs in titles for g in gs))
    genre_features = lambda gs: [1 if g in gs else 0 for g in genres]

    logging.info("averaging ratings...")
    rating_values = [
        v for t, v in ratings.items()
        if v is not None and t in tconsts]
    average_rating = sum(rating_values) / len(rating_values)
    normalized_rating = lambda i: (
        -1 if ratings.get(i) is None else
        0 if ratings[i] < average_rating else
        1)

    logging.info("getting big names...")
    namecounts = dict(list_name_counts(conn, average_rating))
    name_feature = lambda i: namecounts.get(i, 0)

    logging.info("building samples...")
    samples = [
        [name_feature(i), y, r] + genre_features(gs)
        for i, _, y, r, gs in titles]
    labels = [normalized_rating(i) for i, _, _, _, _ in titles]

    logging.info("updating cache...")
    write_cache(cachedir, samples, labels)

    return samples, labels
