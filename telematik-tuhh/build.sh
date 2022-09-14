#!/bin/bash

cd docker
docker build -t telematik-tuhh-solver:latest .
cd -

singularity build solver.sif solver.def