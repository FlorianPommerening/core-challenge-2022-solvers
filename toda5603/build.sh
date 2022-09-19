#!/bin/bash

cat bmcsolver-container.tar.gz | gzip -d | docker import - toda5603-solver:latest
singularity build solver.sif solver.def
