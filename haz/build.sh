#!/bin/bash

cd docker
docker build -t haz-shortest:latest -f Dockerfile.shortest . 
docker build -t haz-longest:latest -f Dockerfile.longest . 
cd -

singularity build solver_shortest.sif solver_shortest.def
singularity build solver_longest.sif solver_longest.def
