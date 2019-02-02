#!/bin/bash

readonly YEARS=("2014" "2015" "2016" "2017" "2018");
readonly MONTHS=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12");
readonly URI="https://api.nytimes.com/svc/archive/v1";
readonly API_KEY="4Saf37nWCWXsNpra9anmrtX5EFCmxbBn";
readonly DATA_DIR="data/nyt"

for year in "${YEARS[@]}"; do
    for month in "${MONTHS[@]}"; do
        curl -s \
            "$URI/$year/$month.json?api-key=$API_KEY" > \
            "$DATA_DIR/$year-$month.json";
        sleep 10; # Avoid rate limiting on nyt servers.
    done
done
