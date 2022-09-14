#!/bin/bash

cat 2022solver_existent-container.tar.gz | gzip -d | docker import - yuya-yamada-n-existent-solver:latest
singularity build solver_existent.sif solver_existent.def

cat 2022solver_shortest.tar.gz | gzip -d | docker import - yuya-yamada-n-shortest-solver:latest
singularity build solver_shortest.sif solver_shortest.def

cat 2022solver_longest.tar.gz | gzip -d | docker import - yuya-yamada-n-longest-solver:latest
singularity build solver_longest.sif solver_longest.def
