"""A common module for working with data sets."""

import random


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
