# Data Sets for CS7641

## IMDB

[Details](https://www.imdb.com/interfaces/)

Titles, ratings, and principals from IMDB.

IMDB provides a daily dump of their database for personal non-commercial use as
a series of tsv files. In order to avoid accidentally redistributing these, I
do not include the datasets themselves in this repo. Instead, you can download
them:

```bash
$ ./data/imdb/get.sh
```

Assuming you have the commands `curl` and `tar` available, this will put the
data in the `data/imdb` directory as several tab separated value files. This
data takes up about two gigabytes of hard drive space.

## NYT

[Details](https://developer.nytimes.com/docs/archive-product/1/overview)

Article metadata for the New York Times.

The New York Times offrers an API to retrieve historical article data back to
1851. Since this is an API and it's still their data, I'm not including it in
the repository. But I have registered an API key and embedded it in a script
that will grab this data for you. I recommend you get your own key at the link
above since there is some serious rate limiting on this API, but this should do
in a pinch.

```bash
$ ./data/nyt/get.sh
```

Assuming you have `curl`, this will put the data for the last five years into
files named like `data/nyt/[year]-[month].json`.

The Times does some rate limiting here, so this will sleep for ten seconds
between each month (i.e it will take a while). Even at that rate, requests
will sometimes be rate limited resulting in some missing data (i.e the file
contains an error response). The parser for this data ignores errors, so this
data will need to be refreshed to be used.
