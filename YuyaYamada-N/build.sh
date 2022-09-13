#!/bin/bash

cat 2022solver_existent-container.tar.gz | gzip -d | docker import - yuya-yamada-n-existent-solver:latest
singularity build 2022solver_existent.sif 2022solver_existent.def