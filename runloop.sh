#!/bin/sh

iter=0

while [ $iter -lt 150 ]; do
    python3 run.py --nogui
    iter=$(expr $iter + 1)
done
