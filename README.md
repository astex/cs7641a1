# OMSCS CS7641 Assignment 1 - Supervised Learning

The first assignment for the OMSCS machine learning class, in which I implement
(steal) a ML library and muck around with it. Specifically, I steal
[`scikit-learn`](https://scikit-learn.org/) (BSD License) since it handily
implements all of the required functionality. Namely,

- Decision Trees
- Neural Networks
- Gradient Boosting
- Support Vector Machines
- k-Nearest Neighbors

## Setup

I'm writing and testing all of this using Python 3.7.2, so you'll need to have
that (other python versions >=3.4 may work, but no guarantees). The
instructions for getting it vary by OS and by distribution within each OS. The
general idea is to use the standard package manager for whatever you use. But
[this](https://wiki.python.org/moin/BeginnersGuide) should help if you're
feeling lost.

You should also get the code:

```bash
$ git clone https://github.com/astex/cs7641a1 .
```

There are a number of ways you can install the required libraries.  I
personally prefer to use a virtual environment so that the dependencies of my
project stay isolated from any software needed elsewhere on the system. Some
folks of a more scientific bent may prefer conda. But, the simplest way I can
think of is this (run from the project directory):

```bash
$ pip install -r builddeps.txt
$ pip install -r deps.txt
```

## Running

Everything you need in order to generate the plots is included, so you can go
ahead and run the scripts.

```bash
$ python -m src.california.main all; python -m src.imdb.main all;
```

This will take around a day to execute and will use an awful lot of memory and
processing power. Alternatively, you can regenerate specific plots by passing a
list of plot names instead of `all`. You can see the plot names in the
applications' help texts:

```bash
$ python -m src.california.main -h
$ python -m src.imdb.main -h
```

## License

This is a homework assignment, not production software. You may run it and look
at it, but may not redistribute it or use it in any system for any reason.
