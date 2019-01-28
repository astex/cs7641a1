#!/bin/bash

# IMDB
./data/imdb/get.sh

# NYT
#
# Sleep for a minute between each fetch to get around rate limiting.
./data/nyt/get.sh 2018; sleep 1m;
./data/nyt/get.sh 2017; sleep 1m;
./data/nyt/get.sh 2016; sleep 1m;
./data/nyt/get.sh 2015; sleep 1m;
./data/nyt/get.sh 2014; sleep 1m;
