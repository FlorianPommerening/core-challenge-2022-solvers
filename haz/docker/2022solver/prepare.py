#!/usr/bin/env python3

import sys, os, csv
import argparse

import run

def create_instance_sas(style,cfile, dfile, sasfile):
    from sas import compile
    compile.compile(style, cfile, dfile, sasfile)


def create_instance_pddl(style,cfile, dfile, domfile, probfile):
    from pddl import encode
    encode.go(style, cfile, dfile, domfile, probfile)


def main(args):

    benchmark_path = os.path.abspath(args.list)
    benchmark_path = os.path.dirname(benchmark_path)
    benchmark_path = os.path.dirname(benchmark_path)
    print(benchmark_path)
    with open(args.list, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            cfile = os.path.join(benchmark_path, row[0])
            dfile = os.path.join(benchmark_path, row[1])
            if args.benchmark not in cfile:
                continue

            if args.format == "sas":
                sasfile = os.path.basename(dfile).replace(".dat", ".sas")
                print(cfile, dfile, sasfile)
                create_instance_sas(args.style, cfile, dfile, sasfile)
            elif args.format == "pddl":
                domfile = os.path.basename(dfile).replace(".dat", ".pddl")
                probfile = "problem-" + domfile
                domfile = "domain-" + domfile
                print(cfile, dfile, domfile, probfile)
                create_instance_pddl(args.style, cfile, dfile, domfile, probfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=False)
 
    parser.add_argument("--benchmark", help="The benchmark", choices=["queen", "grid"])
    parser.add_argument("--format", help="The planning instance format", choices=["pddl", "sas"])
    parser.add_argument("--style", help="The action style", choices=["split", "single", "lifted"])
    parser.add_argument("--list", help="Benchmark list")

    args = parser.parse_args()

    if args.format == "sas" and args.style == "lifted":
        print("Illegal parameters, SAS+ cannot be lifted")
        exit(1)

    main(args)