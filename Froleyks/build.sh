#!/bin/bash

cat reconfaigeration-ex-container.tar.gz | gzip -d | docker import - froleyks-solver:latest
singularity build solver_existent.sif solver_existent.def
singularity build solver_shortest.sif solver_shortest.def
singularity build solver_longest.sif solver_longest.def
