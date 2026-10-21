# Project Resurrection
Cycle 3 multi-agent system, Pursuit L2

Single-species survival modeling for the Iberian lynx and its prey, the European rabbit.  Three agents (Researcher, Simulation Developer, Evaluator) estimate how food availability and habitat quality affect whether the population persists.  The project rules for coding tools are in `AGENTS.md`.

## Setup

Use Python 3.12.  The Mac default `python3` is 3.9, which we do not use.  `python3.12 --version` shows whether 3.12 is installed.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

Until the first tests are added, `python -m pytest` reports that no tests ran.  Never commit keys or `.env`; this repository is public.
