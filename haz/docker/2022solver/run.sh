#!/usr/bin/bash

#---------------------------------
# CoRe Challenge 2022
# solver execution script
#
# Input:
#  col file (as $1)
#  dat file (as $2)
# Output:
#  as in https://core-challenge.github.io/2022/#example-of-output
#---------------------------------

#cd /2022solver
/usr/bin/time -v python3 /2022solver/run.py submission sas split $1 $2

