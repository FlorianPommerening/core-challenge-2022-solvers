# Planning 4 ISR

A planning approach for solving the [The Independent Set Reconfiguration (ISR) Problem](https://core-challenge.github.io/2022).

## Solver Usage

The `[sas|pddl]` choice determines if the encoding is a SAS+ or PDDL representation.

The `[single|split|lifted]` choice decides on the encoding type. `single` moves the token in a single action while `split` separates it into pick and place. `lifted` is a variant of `single` that doesn't ground the domain (only relevant for `pddl` mode).

### To encode a problem

```bash
> python3 run.py encode [pddl|sas] [single|split|lifted] <input .col> <input .dat>
```

### To solve a problem

```bash
> {planner} domain.pddl problem.pddl
```

or

```bash
> {fd-based planner} --plan-file sas_plan output.sas --search "astar(lmcut())"
```

### To decode a solution

```bash
> python3 run.py decode <plan file> <input .dat>
```

### To do all 3 steps

```bash
> ./run.py solve [pddl|sas] [single|split|lifted] <input .col> <input .dat>
```

### To run in interactive mode
This lets you interactively select a problem to solve, along with the options to do so.

```bash
> python3 run.py interactive <benchmark .csv>
```


## Requirements

Best to run it through the provided Docker image. Planutils, Cheetah, etc is pre-installed and setup to go.
