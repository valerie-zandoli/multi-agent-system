# Draft agent handoffs — version 1.0

For Valerie and Anastasiya to review before simulation integration. JSON Schemas
in `schemas/` define the shapes; matching examples live in `examples/handoffs/`.
These examples are hand-authored fixtures, not generated scientific results.

## Flow

Researcher supplies the existing eight-column parameter CSV and source registry.
Run the parameter validator first. The harness then supplies `input.json` to the
simulation developer. A run produces `results.json`; the evaluator returns
`evaluation.json`. This PR defines contracts only, not AI calls or the harness.

## Input

The initial synthetic population is 10 females and 10 males, all 36 months old,
with five of each sex per patch. The two patch areas, age, habitat scores, food
level, and allocation in the example are illustrative assumptions, not measured
starting conditions. Habitat quality is a dimensionless 0–1 shelter/suitability
score; its biological effect still needs agreement. Rabbits remain a density
input, not simulated individuals. No disease shock is included.

`start_month` is the calendar month at elapsed month 0. `duration_months` counts
transitions after initialization. Paths are repository-relative. The proposed
experiment duration is 120 months, but the example uses one month for inspection.
Record the random seed and full configuration in results. Reproduction rules,
food/habitat effects, and any parameter overrides need agreement before runs.

The proposed persistence rule is a living breeding-capable male and female in
at least one shared patch at the endpoint. Determine breeding eligibility from
the parameter specification; this is an endpoint measure, not long-term viability.
Valerie must review this definition before experiments.

## Results

`history` contains month 0 through `duration_months`, inclusive. Month 0 has zero
births, deaths, and movements. Later event counts cover the preceding monthly
transition. Movement counts animals changing patch at least once that month.
`final_animals` includes every animal created, including dead animals; age and
patch for dead animals are their last state at death. IDs stay unique for a run.
`population`, `females`, and `males` count living animals. Births and deaths must
balance each transition; moves do not change total population.

`data_kind: sample` identifies fixtures; real model runs use `simulation`.
The harness must verify matching run IDs/seeds/configurations, contiguous months,
unique animal and patch IDs, valid patch references, final counts, and persistence
against final animal states. JSON Schema alone does not establish these semantic
relationships. They must become runtime checks when the simulation is built.

## Evaluation and bounded revisions

`pass` means all reported checks passed and no issues remain. `revise` means
issues need developer changes; each issue includes a code, message, and requested
change. `stop` is required if unresolved issues remain at revision round 3.
Round 0 is the initial attempt; rounds 1–3 are revisions. On stop, the harness
must report to both teammates. Those behavioral rules require harness tests;
the schemas constrain round numbers, field shapes, and the link between the status
and its evidence (a `pass` lists no issue and no failed check; a `revise` lists at
least one issue).

This version is for synthetic experiments. `historical_validation: not_assessed`
prevents an example format check from implying a historical fit. Historical
comparison requires a separate agreed initialization, observation definition,
calibration/validation split, and tolerance. Do not reuse the 20-lynx fixture as
historical initialization.

## Content hashes

The inputs name the research files by path, and the Researcher can still edit them. A path alone does not say which version of a file a run used, so a run could be evaluated against a table it never read (a stale-data read).

`input.json` therefore records `parameters_sha256` and `sources_sha256`, the content hashes of the two CSV files it names. A content hash is a short fingerprint of a file's contents. `results.json` carries the same values inside `config`, and `evaluation.json` carries them at the top level. Hashes ignore the CRLF/LF difference so every checkout agrees. The sample fixtures use all-zero placeholders; a real run computes them with `validators/handoff_hashes.py`.

The harness must run two checks, which are code and not a prompt:

- `check_handoff_hashes(input, results, evaluation)` before it accepts results and again before it accepts an evaluation. Any difference rejects the handoff.
- `check_files_current(input, root)` at the start of every revision round. A changed file rejects the round.

If the Researcher changes a CSV on purpose, that is not a revision of the old run. The harness starts a new run from a fresh `input.json` with new hashes and a new run ID.

A hash proves two agents read the same file, not that the file is correct. Checking the table against its sources stays a separate job.

## Check contracts locally

```bash
pip install -r requirements-dev.txt
python -m pytest tests/test_handoffs.py
```

`jsonschema` is a development dependency, so the required `tests` check runs
these tests. A missing `jsonschema` makes them fail; it never skips them.
The Handoff contracts CI workflow still installs `requirements-handoffs.txt`
(the same pin) and runs the full test suite.
