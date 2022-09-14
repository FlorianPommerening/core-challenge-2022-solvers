#!/bin/bash

DOWNWARD=$DOWNWARD_REPO/fast-downward.py
COL_FILE=$1
DAT_FILE=$2
INSTANCE=$(basename $DAT_FILE .dat)

./compile.py $COL_FILE $DAT_FILE ${INSTANCE}.sas
$DOWNWARD --plan-file ${INSTANCE}.plan ${INSTANCE}.sas --search "astar(lmcut())" > ${INSTANCE}.log 2> ${INSTANCE}.err
echo $?
