# Project rules for coding tools

Claude Code and Codex both read these rules (`CLAUDE.md` imports this file).  Change the rules here, not in a tool-specific file.

## Project

Single-species survival modeling for the Iberian lynx and its prey, the European rabbit.  Research question:  how do food availability and habitat quality affect the likelihood that the population persists over a fixed period?

## Architecture (agreed)

Researcher, then Simulation Developer, then Evaluator.  The Evaluator returns problems to the Simulation Developer for revision.  Code manages every handoff; a separate coordinator agent is optional.

- Researcher:  supplies a sourced parameter table and assumptions.
- Simulation Developer:  builds the model and runs the experiments.
- Evaluator:  checks the implementation and the conclusions.
- The simulated lynx and rabbits live inside the model.  They are not the AI agents.

## Ownership

- Valerie (Person 1):  Researcher, Evaluator, baseline history test.
- Anastasiya (Person 2):  Simulation Developer, parameter table validator.
- Together:  the parameter table format (written first), the harness, the presentation.

Also agreed:

- The harness is pair-programmed from 16:00 to 18:00 ET, and the revision loop stops after 3 rounds and reports to both of us.
- Each of us writes the code check for the other's output.  Anastasiya writes the parameter table validator (every parameter has a source and a range).  Valerie writes the baseline history test (the model reproduces the lynx's known population history within a tolerance set before any run).

## Stretch goal

Run the black-footed ferret and prairie dog with the same model template.  It passes if the second pair needs no change to the model code, only a new sourced parameter table, and its report passes the same checks.  Run it only if the lynx build leaves time.

## Working rules

- Ask "push or wait?" before changing a shared file.
- Draft work goes on your own branch (`dev-valerie`, `dev-anastasiya`).  Changes reach `main` only through a pull request, after the tests pass and the other person reviews it.  Do not push unproven work to `main`.
- Work in separate files; review each other through pull requests.
- Write the interfaces between the agents before anyone builds.
- A prompt asks; code guarantees.  Any rule that must always hold goes in code with a test, and the design notes which of the two enforces it.
- Never commit keys, `.env`, or private data.  This repository is public.

## Setup

- Python version:  3.12.  The Mac default `python3` is 3.9, which we do not use.
- Test command:  `python -m pytest`, run inside the virtual environment.  The setup steps are in the README.
