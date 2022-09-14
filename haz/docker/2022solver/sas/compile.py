#!/usr/bin/env python3

from Cheetah.Template import Template
from collections import defaultdict
import os
import sys


def to_var_id(node):
    return int(node) - 1


def parse_col_file(filename):
    with open(filename) as f:
        graph = defaultdict(set)
        num_nodes, num_edges = None, None
        num_parsed_edges = 0
        for line in f:
            args = line.split()
            assert args[0] == "c" or len(args) == 3
            if args[0] == "p":
                num_nodes, num_edges = int(args[1]), int(args[2])
            elif args[0] == "e":
                num_parsed_edges += 1
                v0, v1 = to_var_id(args[1]), to_var_id(args[2])
                assert 0 <= v0 <  num_nodes
                assert 0 <= v1 <  num_nodes
                graph[v0].add(v1)
                graph[v1].add(v0)
    assert num_edges == num_parsed_edges
    return graph


def parse_dat_file(filename):
    start, target = None, None
    with open(filename) as f:
        for line in f:
            args = line.split()
            if args[0] == "s":
                start = set([to_var_id(x) for x in args[1:]])
            if args[0] == "t":
                target = set([to_var_id(x) for x in args[1:]])
    return start, target


def fill_template(template_filename, out_file, **kwargs):
    template = Template(file=template_filename, searchList=[kwargs])
    with open(out_file, "w") as f:
        f.write(str(template))


def compile(style, col_filename, dat_filename, outfile):
    if style == "single":
        template_file = "sas_file_single.tmpl"
    elif style == "split":
        template_file = "sas_file_split.tmpl"
    elif style == "split_tnf":
        template_file = "sas_file_split_tnf.tmpl"
    template_file = os.path.join(os.path.dirname(__file__), template_file)
    graph = parse_col_file(col_filename)
    start, target = parse_dat_file(dat_filename)
    fill_template(template_file, outfile, **locals())


if __name__ == "__main__":
    compile(*sys.argv[1:])
