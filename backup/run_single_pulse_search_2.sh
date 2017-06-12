#!/bin/bash

IN_FILE_NAME="$1"
IN_FILE_ROOT="${1%.*}"
MASK_NAME="${IN_FILE_ROOT}_rfifind.mask"
OUT_FILE_ROOT="$IN_FILE_ROOT"
#OUT_FILE_NAME="${OUT_FILE_ROOT}.dat"

echo "Reading: $IN_FILE_NAME"

rfifind -time 1.0 -o $IN_FILE_ROOT $IN_FILE_NAME

echo "Apply Mask: $MASK_NAME"

prepsubband -lodm 0.0 -numdms 10 -dmstep 1 -mask $MASK_NAME -o $OUT_FILE_ROOT -nobary $IN_FILE_NAME

echo "Data Prepared: ${OUT_FILE_ROOT}_DMs.dat"

single_pulse_search.py $OUT_FILE_ROOT*.dat

echo "Done single pulse search"
