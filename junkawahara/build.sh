#!/bin/bash

mkdir tmp
cd tmp
tar xvzf ../zdd-solver-container.tar.gz
cd zdd-solver-container
sed -i "s|zdd-solver.py|/2022solver/zdd-solver.py|g"  2022solver/run.sh
tar cvf ../../zdd-solver-container-fixed.tar *
cd ../..
rm -rf tmp
docker import zdd-solver-container-fixed.tar junkawahara-solver:latest
rm zdd-solver-container-fixed.tar
singularity build solver.sif solver.def
