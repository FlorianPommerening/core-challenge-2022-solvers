#!/usr/bin/env python3

import sys, os, subprocess, time, tempfile

CUR_DIR = os.getcwd()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = tempfile.TemporaryDirectory()
#RESULTS_DIR = TMP_DIR.name
RESULTS_DIR = CUR_DIR
print(f"Results dir: {RESULTS_DIR}")

USAGE = """
\tUsage: ./run.py [encode|decode|validate|solve|interactive]

\tencode:
\t  python3 run.py encode [pddl|sas] [single|split|lifted] <input .col> <input .dat>
\t    - encode a problem in either PDDL or SAS format
\t    - [pddl|sas]: type of encoding format
\t    - [single|split|lifted]: type of encoding technique
\t    - <input .col>: input .col file from the benchmarks
\t    - <input .dat>: input .dat file from the benchmarks

\tdecode:
\t  python3 run.py decode [pddl-single|pddl-split|pddl-lifted|sas-single|sas-split] <plan file> <input .dat>
\t    - decode a plan into the contest format
\t    - [pddl-single|pddl-split|pddl-lifted|sas-single|sas-split]: type of encoding format
\t    - <plan file>: the generated plan
\t    - <input .dat>: input .dat file from the benchmarks

\tvalidate:
\t  python3 run.py validate <sol file> <input .col> <input .dat>
\t    - validate a solution
\t    - <sol file>: the solution (translated from plan)
\t    - <input .col>: input .col file from the benchmarks
\t    - <input .dat>: input .dat file from the benchmarks

\tsolve:
\t  python3 run.py solve [pddl|sas] [single|split|lifted] <input .col> <input .dat>
\t    - encode a problem in either PDDL or SAS format
\t    - Same parameters as encode

\tsubmission:
\t  python3 run.py submission [pddl|sas] [single|split|lifted] <input .col> <input .dat>
\t    - same as solve, but prints the solution and not the debugging information

\tinteractive:
\t  python3 run.py interactive <benchmark .csv>
\t    - run an interactive session to choose problem and solving technique
\t    - <benchmark .csv>: the benchmark .csv file

"""

SILENCE = False
STATUS = True

# Ugly, I know...
VALIDATOR = os.path.join(os.path.dirname(__file__),
                    '..',
                    '..',
                    'external',
                    'isr-validator',
                    'main.py')

def prep_instance(dfile, wipe=False):
    instance = os.path.basename(dfile).split('.')[0]
    if wipe:
        os.system(f'rm -rf {RESULTS_DIR}/{instance}')
    if os.path.exists(os.path.join(RESULTS_DIR, instance)):
        print("\n\tError: instance directory already exists\n")
        exit(1)
    else:
        os.mkdir(os.path.join(RESULTS_DIR, instance))
    return instance

def do_encode(format, style, cfile, dfile, instance = '..', sasfile = 'output.sas'):
    if SILENCE and STATUS:
        print("\nEncoding...", end='')
        t = time.time()

    if format == 'pddl':
        from pddl import encode
        domfile = os.path.join(RESULTS_DIR, instance, 'domain.pddl')
        probfile = os.path.join(RESULTS_DIR, instance, 'problem.pddl')
        encode.go(style, cfile, dfile, domfile, probfile)

    else:
        from sas import compile
        sasfile = os.path.join(RESULTS_DIR, instance, sasfile)
        compile.compile(style, cfile, dfile, sasfile)

    if SILENCE and STATUS:
        print(f"{time.time() - t:.2f}s")

def do_plan(format, instance = '..', sasfile = 'output.sas', planfile = 'sas_plan', cfile = 'in.col', dfile = 'in.dat'):
    if SILENCE and STATUS:
        print("\nPlanning...", end='')
        t = time.time()

    logfile = open(os.path.join(RESULTS_DIR, instance, 'plan.log'), "w")
    errfile = open(os.path.join(RESULTS_DIR, instance, 'plan.err'), "w")
    if format == 'pddl':
        domfile = os.path.join(RESULTS_DIR, instance, 'domain.pddl')
        probfile = os.path.join(RESULTS_DIR, instance, 'problem.pddl')
        planfile = os.path.join(RESULTS_DIR, instance, planfile)
        result = subprocess.run([os.path.join(SCRIPT_DIR, 'plan-pddl.sh'), domfile, probfile, planfile],
                                stdout=logfile, stderr=errfile, universal_newlines=True)
    else:
        planfile = os.path.join(RESULTS_DIR, instance, planfile)
        sasfile = os.path.join(RESULTS_DIR, instance, sasfile)
        result = subprocess.run([os.path.join(SCRIPT_DIR, 'plan-sas.sh'), planfile, sasfile, cfile, dfile],
                                stdout=logfile, stderr=errfile, universal_newlines=True)

    logfile.close()
    errfile.close()
    #if SILENCE:
    #    if STATUS:
    #        errfile = os.path.join(RESULTS_DIR, instance, 'plan.err')
    #        logfile = os.path.join(RESULTS_DIR, instance, 'plan.log')
    #        with open(logfile, 'w') as f:
    #            f.write(result.stdout)
    #        with open(errfile, 'w') as f:
    #            f.write(result.stderr)
    #        print(f"{time.time() - t:.2f}s")
    #    else:
    #        print('\n'.join(filter(lambda x: x[:2] == 'c ', result.stdout.split('\n'))))
    #else:
    #    print(result.stdout)
    #    print(result.stderr)
    return result.returncode

def do_decode(mode, datafile, instance = '..', planfile = 'sas_plan', solfile = 'SOL', rescode=None):
    if SILENCE and STATUS:
        print("\nDecoding...", end='')
        t = time.time()
    from utils import decode
    solfile = os.path.join(RESULTS_DIR, instance, solfile)
    planfile = os.path.join(RESULTS_DIR, instance, planfile)
    with open(solfile, 'w') as f:
        if rescode == 10:
            f.write('a NO')
        elif not os.path.isfile(planfile):
            f.write('c UNKNOWN')
        else:
            f.write(decode.go(mode, planfile, datafile))
    if SILENCE and STATUS:
        print(f"{time.time() - t:.2f}s")

def do_validate(cfile, dfile, instance = '..', solfile = 'SOL'):
    if SILENCE and STATUS:
        print("\nValidating...\n\n\t", end='')
    solfile = os.path.join(RESULTS_DIR, instance, solfile)
    if not STATUS:
        suffix = ' > /dev/null 2>&1'
    else:
        suffix = ''
    os.system(f'python3 {VALIDATOR} {cfile} {dfile} {solfile}{suffix}')

def do_solve(format, style, cfile, dfile, instance):
    do_encode(format, style, cfile, dfile, instance)
    res = do_plan(format, instance, cfile=cfile, dfile=dfile)
    do_decode(f'{format}-{style}', dfile, instance, rescode=res)
    do_validate(cfile, dfile, instance)


def interactive(instance_csv):
    instances = {}
    with open(instance_csv, 'r') as f:
        for line in f.readlines():
            cfile, dfile = line.strip().split(',')
            domain = cfile.split('/')[1]
            if domain not in instances:
                instances[domain] = {}
            graph = cfile.split('/')[-1]
            if graph not in instances[domain]:
                instances[domain][graph] = []
            instances[domain][graph].append((cfile, dfile))
    domains = sorted(instances.keys())

    print("\n\tWhich domain?")
    for i, domain in enumerate(domains):
        print(f'\t {i+1}: {domain} ({len(instances[domain])})')
    choice = None
    while choice not in map(str, range(1, len(domains)+1)):
        choice = input('\n\t? ')
    domain = domains[int(choice)-1]
    graphs = sorted(instances[domain].keys())

    print("\n\n\tWhich graph file?")
    for i, gfile in enumerate(graphs):
        print(f'\t {i+1}: {gfile} ({len(instances[domain][gfile])})')
    choice = None
    while choice not in map(str, range(1, len(instances[domain])+1)):
        choice = input('\n\t? ')
    gfile = graphs[int(choice)-1]

    print("\n\n\tWhich problem file?")
    for i, (cfile, dfile) in enumerate(instances[domain][gfile]):
        print(f'\t {i+1}: {dfile.split("/")[-1]}')
    choice = None
    while choice not in map(str, range(1, len(instances[domain][gfile])+1)):
        choice = input('\n\t? ')
    instance = instances[domain][gfile][int(choice)-1]

    print("\n\t   Graph:", instance[0])
    print("\tInstance:", instance[1])

    print("\n\t   Which format?")
    print("\t 1: PDDL")
    print("\t 2: SAS")
    choice = None
    while choice not in ['1','2']:
        choice = input('\n\t? ')
    format = 'pddl' if choice == '1' else 'sas'

    print("\n\t   Which style?")
    print("\t 1: Single")
    print("\t 2: Split")
    if format == 'pddl':
        print("\t 3: Lifted")
    choice = None
    while choice not in ['1','2','3']:
        choice = input('\n\t? ')
        if format == 'sas' and choice == '3':
            print("\n\t   Lifted is not supported for SAS")
            choice = None
    style = 'single' if choice == '1' else 'split' if choice == '2' else 'lifted'

    iname = prep_instance(instance[1])
    benchdir = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'external',
                            'benchmarks')
    cfile = os.path.join(benchdir, instance[0])
    dfile = os.path.join(benchdir, instance[1])

    print(f"\n To rerun:\n\npython3 run.py solve {format} {style} {cfile} {dfile}")

    global SILENCE
    SILENCE = True

    do_solve(format, style, cfile, dfile, iname)


if __name__ == "__main__":

    if len(sys.argv) < 2 or sys.argv[1] not in ['encode', 'decode', 'validate', 'solve', 'interactive', 'submission']:
        sys.exit(USAGE)

    def check_args():
        if len(sys.argv) != 6:
            sys.exit(USAGE)
        if sys.argv[2] not in ['pddl', 'sas']:
            sys.exit(USAGE)
        if sys.argv[3] not in ['single', 'split', 'split_tnf', 'lifted']:
            sys.exit(USAGE)
        if sys.argv[2] == 'sas' and sys.argv[3] == 'lifted':
                print("\n\tLifted encoding not supported for SAS")
                sys.exit(USAGE)

    if sys.argv[1] == 'encode':
        check_args()
        do_encode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    elif sys.argv[1] == 'decode':
        if len(sys.argv) != 5:
            sys.exit(USAGE)
        do_decode(sys.argv[2], sys.argv[4], planfile=sys.argv[3])

    elif sys.argv[1] == 'validate':
        if len(sys.argv) != 5:
            sys.exit(USAGE)
        do_validate(sys.argv[3], sys.argv[4], solfile=sys.argv[2])

    elif sys.argv[1] in ['solve', 'submission']:

        check_args()

        SILENCE = True
        if sys.argv[1] == 'submission':
            STATUS = False

        #instance = prep_instance(sys.argv[5], wipe=(sys.argv[1] == 'submission'))
        instance = ""

        do_solve(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], instance)

        if sys.argv[1] == 'submission':
            solfile = os.path.join(RESULTS_DIR, instance, 'SOL')
            with open(solfile, 'r') as f:
                print(f.read().strip())

    elif sys.argv[1] == 'interactive':
        if len(sys.argv) != 3:
            sys.exit(USAGE)
        interactive(sys.argv[2])

    if STATUS:
        print()
