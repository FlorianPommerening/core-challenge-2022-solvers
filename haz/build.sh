#!/bin/bash

cd docker
docker build -t haz-shortest:latest -f Dockerfile.shortest . 
docker build -t haz-longest:latest -f Dockerfile.longest . 
docker build -t haz-symk:latest -f Dockerfile.symk . 
cd -

singularity build solver_shortest.sif solver_shortest.def
singularity build solver_longest.sif solver_longest.def
singularity build solver_symk.sif solver_symk.def
