# Data Sets for CS7641

## IMDB

Titles, ratings, and principals from IMDB.

IMDB provides a daily dump of their database for personal non-commercial use as
a series of tsv files
([https://www.imdb.com/interfaces/](https://www.imdb.com/interfaces/)). In
order to avoid accidentally redistributing these, I do not include the datasets
themselves in this repo. Instead, you can download them:

```bash
$ ./data/imdb/get.sh
```

Assuming you have the commands `curl` and `tar` available, this will put the
data in the `data/imdb` directory as several tab separated value files. This
data takes up about two gigabytes of hard drive space.
