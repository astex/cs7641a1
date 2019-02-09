"""A library for working with the california data."""

import logging
import sklearn.datasets
from .. import data as datalib


def get_data(datadir):
    """Gets training and test data sets.

    Args:
        datadir: The directory where the data can be found.
        testprob: The probability that a given sample will be set aside for
            testing.

    Returns:
        ((test samples, test labels), (training samples, training labels))
    """
    return sklearn.datasets.fetch_california_housing(
        datadir,
        return_X_y=True)


def make_boolean(data):
    """Transforms labels into two classes (>avg, <avg)."""
    logging.info("transforming labels...")
    samples, labels = data
    average = sum(labels) / len(labels)
    labels = [1 if label > average else -1 for label in labels]
    return samples, labels


def normalize(data):
    """Scales inputs to [0, 1]."""
    logging.info("scaling...")
    samples, labels = data
    samples = list(zip(*samples))
    scale = [(lambda x: (x - min(s)) / (max(s) - min(s))) for s in samples]
    samples = [[f(x) for x in s] for f, s in zip(scale, samples)]
    samples = list(zip(*samples))
    return samples, labels
