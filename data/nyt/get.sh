#!/bin/bash

readonly MONTHS=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12");
readonly URI="https://api.nytimes.com/svc/archive/v1";
readonly API_KEY="4Saf37nWCWXsNpra9anmrtX5EFCmxbBn";
readonly DATA_DIR="data/nyt"

for month in "${MONTHS[@]}"; do
    curl \
        "$URI/$1/$month.json?api-key=$API_KEY" > \
        "$DATA_DIR/$1-$month.json";
done
