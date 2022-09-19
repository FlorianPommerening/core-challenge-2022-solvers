#!/bin/bash

cat dockerarchive.tar.gz | gzip -d | docker import - tigrisg-solver:latest
singularity build solver.sif solver.def
