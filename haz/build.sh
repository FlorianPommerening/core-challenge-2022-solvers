#!/bin/bash

cd docker
docker build -t haz-shortest:latest -f Dockerfile.shortest . 
docker build -t haz-symbolic-search:latest -f Dockerfile.symbolic_search . 
docker build -t haz-astar-lm:latest -f Dockerfile.astar_lm . 
docker build -t haz-gbfs-lm:latest -f Dockerfile.gbfs_lm . 
docker build -t haz-mip:latest -f Dockerfile.mip . 
docker build -t haz-longest:latest -f Dockerfile.longest . 
docker build -t haz-symk:latest -f Dockerfile.symk . 
cd -

singularity build solver_shortest.sif solver_shortest.def
singularity build solver_symbolic_search.sif solver_symbolic_search.def
singularity build solver_gbfs_lm.sif solver_gbfs_lm.def
singularity build solver_mip.sif solver_mip.def
singularity build solver_longest.sif solver_longest.def
singularity build solver_symk.sif solver_symk.def
