"""A common module for working with data sets."""

import logging
import pygal
import random
import time


class DataSet:
    """A collection of imdb data."""

    def __init__(self, features, samples, names, labels):
        """Initialize.

        Args:
            features: An array of length N with string descriptions of what
                each feature means.
            samples: An array of M x N where each element contains the value of
                each feature in a list.
            names: An array of length M where each element is the name of the
                sample of the same index.
            labels: An array of length M where each element is the label for
                the sample of the same index.
        """
        if len(names) != len(labels):
            raise TypeError("Names and labels differ in length.")
        if len(names) != len(samples):
            raise TypeError("Names and samles differ in length.")
        if any(len(sample) != len(features) for sample in samples):
            raise TypeError("A sample differs in length from the features.")

        self.features = features
        self.samples = samples
        self.names = names
        self.labels = labels

    def partition(self, prob):
        """Partitions samples based on a uniform distribution.
        
        Args:
            prob: The probability of a given sample being in the left return
                set. Otherwise, the sample is placed in the right return set.

        Returns:
            (left dataset, right datset)
        """
        ldata = DataSet(self.features, [], [], [])
        rdata = DataSet(self.features, [], [], [])
        for sample, name, label in zip(self.samples, self.names, self.labels):
            data = ldata if random.uniform(0, 1) < prob else rdata
            data.samples.append(sample)
            data.names.append(name)
            data.labels.append(label)
        return ldata, rdata


def partition(datasets, probs):
    """Splits data into two partitions.
    
    Args:
        datasets: Any number of datasets of the same size. These will be
            partitioned together, so if the first element of one dataset goes
            to the right then the first element of all the other datasets will
            do the same.
        probs: The probability that the data is split into each of the buckets.
        
    Returns:
        A number of buckets containing some portion of the datasets according
        to probs.
    """
    buckets = [[] for _ in probs]
    for item in zip(*datasets):
        coin = random.uniform(0, 1)
        ptotal = 0
        for bucket_index, pcurr in enumerate(probs):
            ptotal += pcurr
            if coin < ptotal:
                break
        else:
            continue
        buckets[bucket_index].append(item)
    return [list(zip(*d)) for d in buckets]


def make_boolean(data):
    """Transforms labels into two classes (>avg, <avg)."""
    samples, labels = data
    average = sum(labels) / len(labels)
    labels = [1 if label > average else -1 for label in labels]
    return samples, labels


def normalize(data):
    """Scales inputs to [0, 1]."""
    samples, labels = data
    samples = list(zip(*samples))
    mins = [min(s) for s in samples]
    maxs = [max(s) for s in samples]
    scale = [
        (lambda x: (x - mi) / (ma - mi))
        for mi, ma, s in zip(mins, maxs, samples)]
    samples = [[f(x) for x in s] for f, s in zip(scale, samples)]
    samples = list(zip(*samples))
    return samples, labels


PLOTFUNCS = {}


def register_plotfunc(prefix, x_title, plotfunc):
    PLOTFUNCS["%s_%s" % (prefix, x_title)] = (plotfunc, x_title)


def get_plotfuncs():
    return list(PLOTFUNCS.keys())


def get_plotfunc(plotfunc):
    return PLOTFUNCS[plotfunc][0]


def get_xtitle(plotfunc):
    return PLOTFUNCS[plotfunc][1]


def _timer():
    def backend():
        curr = None
        prev = time.time()
        while True:
            curr = time.time()
            yield curr - prev
            prev = curr
    timer = backend()
    next(timer)
    return timer


class Plotter:
    def __init__(self, xtitle):
        self.lerr = []
        self.terr = []
        self.ftimes = []
        self.stimes = []
        self.xtitle = xtitle

    @property
    def learning_plot(self):
        plot = pygal.XY(
            stroke=False,
            x_title=self.xtitle,
            y_title="error")
        plot.add("training", self.lerr)
        plot.add("testing", self.terr)
        return plot

    @property
    def fit_timing_plot(self):
        plot = pygal.XY(
            stroke=False,
            show_legend=False,
            x_title=self.xtitle,
            y_title="fit_time")
        plot.add("", self.ftimes)
        return plot

    @property
    def score_timing_plot(self):
        plot = pygal.XY(
            stroke=False,
            show_legend=False,
            x_title=self.xtitle,
            y_title="score_time")
        plot.add("", self.stimes)
        return plot

    def plot(self, classifier, xval, ldata, tdata):
        logging.info("plotting data point %s...", xval)
        timer = _timer()
        classifier.fit(*ldata)
        self.ftimes.append((xval, next(timer)))
        self.lerr.append((xval, 1 - classifier.score(*ldata)))
        self.terr.append((xval, 1 - classifier.score(*tdata)))
        self.stimes.append((xval, next(timer)))
