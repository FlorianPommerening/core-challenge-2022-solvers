
import os, pprint, sys

from pddl.templates import DOMAIN, PROBLEM, SINGLE_ACTION, DUAL_ACTION_PICK, DUAL_ACTION_PLACE, LIFTED_DOMAIN, LIFTED_PROBLEM

USAGE = "\n\tpython3 encode.py [single|split] <input .col> <input .dat>\n"


def parse(cfile, dfile):

    with open(dfile, 'r') as f:
        data = f.read().splitlines()

    with open(cfile, 'r') as f:
        col = f.read().splitlines()

    while 'c' == data[0][0]:
        data.pop(0)

    while 'c' == col[0][0]:
        col.pop(0)

    (p, n, e) = col[0].split()
    assert p == "p"
    num_nodes = int(n)
    num_edges = int(e)
    col.pop(0)

    edges = {i: set() for i in range(1, num_nodes+1)}

    for line in col:
        (e, a, b) = line.split()
        assert e == "e"
        edges[int(a)].add(int(b))
        edges[int(b)].add(int(a))

    assert "s " == data[0][0:2]
    assert "t " == data[1][0:2]

    init = [int(x) for x in data[0][2:].split()]
    goal = [int(x) for x in data[1][2:].split()]

    assert len(init) == len(goal)

    return (edges, init, goal, num_nodes, num_edges)

def gen_single_action(loc1, loc2, edges):
    act = SINGLE_ACTION.replace('[LOC1]', loc1)
    act = act.replace('[LOC2]', loc2)

    # We don't include the source location in the destination neighbourhood
    relevant_locs = set(edges[int(loc2[1:])]) - set([int(loc1[1:])])
    is_cond = ' '.join([f'(free l{i})' for i in relevant_locs])
    act = act.replace('[IS-COND]', is_cond)
    return act

def gen_dual_actions(loc, edges):
    act1 = DUAL_ACTION_PICK.replace('[LOC]', loc)

    act2 = DUAL_ACTION_PLACE.replace('[LOC]', loc)
    is_cond = ' '.join([f'(free l{i})' for i in edges[int(loc[1:])]])
    act2 = act2.replace('[IS-COND]', is_cond)

    return [act1, act2]

def go(style, cfile, dfile, domfile, probfile):
    (edges, init, goal, num_nodes, num_edges) = parse(cfile, dfile)

    locations = [f'l{i}' for i in range(1, num_nodes+1)]

    ###########
    # Problem #
    ###########

    # Not required if we ground the actions in advance
    if style == 'lifted':
        f_edges = []
        for e1 in edges:
            for e2 in edges[e1]:
                f_edges.append(f'(edge l{e1} l{e2})')
        problem = LIFTED_PROBLEM.replace('[EDGES]', '\n        '.join(f_edges))
        problem = problem.replace('[LOCATIONS]', ' '.join(locations))
    else:
        problem = PROBLEM.replace('[EDGES]', '')

    f_tokened = []
    for i in range(len(init)):
        f_tokened.append(f'(tokened l{init[i]})')
    problem = problem.replace('[TOKENED]', '\n        '.join(f_tokened))

    f_free = []
    for loc in locations:
        if int(loc[1:]) not in init:
            f_free.append(f'(free {loc})')
    problem = problem.replace('[FREE_LOCATIONS]', '\n        '.join(f_free))

    f_goal = []
    for i in goal:
        f_goal.append(f'(tokened l{i})')
    problem = problem.replace('[GOAL]', '\n            '.join(f_goal))


    if style == 'split':
        problem = problem.replace('[PHASE]', '(handfree)')
    elif style == 'single':
        problem = problem.replace('[PHASE]', '')


    ##########
    # Domain #
    ##########

    domain = DOMAIN.replace('[LOCATIONS]', ' '.join(locations))

    if style == 'split':
        domain = domain.replace('[PHASE-PRED]', '; Actions split in two\n        (holding)\n        (handfree)')
        actions = []
        for loc in locations:
            actions.extend(gen_dual_actions(loc, edges))
        domain = domain.replace('[ACTIONS]', '\n        '.join(actions))
    elif style == 'single':
        domain = domain.replace('[PHASE-PRED]', '')
        actions = []
        for l1 in locations:
            for l2 in locations:
                if l1 != l2:
                    actions.append(gen_single_action(l1, l2, edges))
        domain = domain.replace('[ACTIONS]', '\n        '.join(actions))
    else:
        # Nothing to do for the lifted domain
        domain = LIFTED_DOMAIN

    with open(domfile, 'w') as f:
        f.write(domain)
    with open(probfile, 'w') as f:
        f.write(problem)

if __name__ == "__main__":

    if len(sys.argv) != 4 or sys.argv[1] not in ['single', 'split']:
        print(USAGE)
        exit(1)

    go(sys.argv[2], sys.argv[3], sys.argv[1] == 'split')


