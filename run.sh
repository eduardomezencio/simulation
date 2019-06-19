#!/bin/bash

OUT_EXT="csv"

mkdir -p output

for SCENARIO in scenarios/*
do
    OUT=${SCENARIO/scenarios/output}
    OUT=${OUT/txt/$OUT_EXT}
    python -m simulation --header > "$OUT"
    for i in {1..100}
    do
        python -m simulation "$SCENARIO" >> "$OUT"
    done
done
