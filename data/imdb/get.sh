#!/bin/bash

readonly DATA_DIR="data/imdb/"
readonly IMDB_URL="https://datasets.imdbws.com/"
readonly DATASETS=(
    "name.basics"
    "title.akas"
    "title.basics"
    "title.crew"
    "title.episode"
    "title.principals"
    "title.ratings")

for dataset in "${DATASETS[@]}"; do
    curl -s "$IMDB_URL$dataset.tsv.gz" > "$DATA_DIR$dataset.tsv.gz";
    gunzip -f "$DATA_DIR$dataset.tsv.gz";
done
