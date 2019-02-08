"""A library for working with the california data."""

import sklearn.datasets
from .. import data as datalib


def get_data(datadir, testprob):
    """Gets training and test data sets.

    Args:
        datadir: The directory where the data can be found.
        testprob: The probability that a given sample will be set aside for
            testing.

    Returns:
        ((test samples, test labels), (training samples, training labels))
    """
    data = sklearn.datasets.fetch_california_housing(
        datadir,
        return_X_y=True)
    return datalib.partition(testprob, *data)


def make_boolean(tdata, ldata):
    """Transforms labels into two classes (>avg, <avg)."""
    tsamples, tlabels = tdata
    lsamples, llabels = ldata

    average = sum(llabels + tlabels) / len(llabels + tlabels)
    llabels = [1 if llabel > average else -1 for llabel in llabels]
    tlabels = [1 if tlabel > average else -1 for tlabel in tlabels]

    tdata = (tsamples, tlabels)
    ldata = (lsamples, llabels)

    return tdata, ldata
