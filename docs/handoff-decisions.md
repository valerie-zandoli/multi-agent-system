# Handoff decisions (PROPOSED)

Drafted 2026-10-22 by Valerie with Claude Code.  These are Valerie's proposed answers to items 1 to 9 of Anastasiya's review of pull request 21, and the failure behavior that the tutor asked to carry into the PRD.  Nothing here is agreed until Anastasiya says yes, and nothing here is built.  Every number marked (guess) is a guess until the first real runs measure it.

## Research contract

1. **Confidence.**  The allowed labels are `low`, `medium`, and `high`, and `confidence_reason` is required (one sentence that names the evidence).  `high` means two or more distinct origins, each read in full, and no open conflict.  `medium` means one origin read in full, or two or more distinct origins with a recorded conflict.  `low` means abstract only, second-hand, provisional, or an assumption.  Valerie assigns the label, because it is an evidence judgment.  Code checks that the label is in the set and the reason is not empty.
2. **Origin.**  Origin IDs are defined in `docs/research-notes.md`.  The registry `origin` lists every upstream that a source reports; it is a menu, not a count.  The parameter table gets an `origin` column that lists only the origin IDs that support that row's value, and the validator checks that they are a subset of the origins of the sources cited in the row.  For example, `eu_spain_report2018` reports both Palomares 2001 and the 2017 census, but only `palomares2001` supports a rabbit threshold.  Code counts distinct row-level origins per parameter, not source keys.  `unknown` never counts as an independent origin.  Provisional and final figures of one census share an origin; different census years are different origins.  Code sets no minimum number of origins; a single-origin parameter can still be used, and its confidence label says how far to trust it.
3. **Contradictions.**  The parameter table gets a `contradicts` column, and every row has a value.  Entries are separated by semicolons:  `none_identified`; `not_checked`; `source:<key>~source:<key>` (two sources of this row disagree about this parameter); and `parameter:<name>` (this parameter conflicts with the evidence for another parameter, such as range size and food level).  `none_identified` and `not_checked` stand alone.  The validator checks that every named key and parameter exists.  A `not_checked` row warns in pilot runs and blocks final runs.  A recorded conflict does not block a run (both versions run, as agreed for range size), but the Evaluator report lists every open conflict.  A test holds the known conflicts from `docs/research-notes.md` (breeding age, `palomares2005` against `catsg`; range size and food) and fails if they are missing from the column.

## Clarification round

- A case is one run chain, from the first `input.json` until pass or stop.  A deliberate change to the research files starts a new run (round 0) inside the same case; the clarification budget carries over.
- Each case gets one Researcher round, shared by the Developer and the Evaluator, and it batches every open parameter.  The budget is separate from developer revisions 1 to 3.
- A request names the parameter, what is missing, whether the gap is required or optional, and who filed it.
- A required gap is a missing or `low`-confidence value for a parameter that an experiment cannot run without, or any gap the Evaluator marks blocking.  An optional gap affects a sensitivity run only; it is logged as a limitation.
- The round resolves a gap when the Researcher returns the value with source, origin, confidence, reason, and `contradicts`, and the validator accepts it.
- A required gap that remains after the round, or a new required gap after the round, stops the case and reports to both owners.  An optional gap never stops a case.

## Failure behavior (for the PRD)

- **Hand back, once.**  The Researcher holds the evidence, and a fresh Researcher run is cheap.  This is the clarification round above.
- **Escalate** to a person (Valerie and Anastasiya) with the table and the request attached when a claim stays unresolved after the round.  The run stays held.
- **Fail explicitly, with no retry,** for faults that more evidence cannot fix:  a changed parameter file or a schema mismatch (both built), a killed run, and an unresolved issue at revision round 3 (both planned).
- A "settled" claim needs a new origin that the code derives from the fetched page.  A person audits 10 settled rows before each experiment batch.  If fewer than 6 of the first 20 hand-backs return a new source that settles the claim (guess), the default switches to escalate.

## Hashes

The harness computes the content hashes from the actual input files, and the agents carry them unchanged.  A deliberate research edit starts a fresh run.  No live harness enforcement exists yet.

## Transient retries

- Allow at most 1 retry per tool call, 3 per round, and 10 per case (guess).
- These errors qualify:  a network timeout, a connection reset, HTTP 429, and HTTP 5xx from the provider.  These do not:  a schema or validation failure, model output that fails a check, a killed run, and any other 4xx.
- The trace logs each retry with its error, apart from revisions.  When a bound is reached, the case stops and reports.

## Primary-source audit

- Before each experiment batch, a person checks 10 parameter rows against the primary source.
- A script chooses the rows with a recorded seed (the batch run ID), so another person can reproduce the sample.
- A failure means the value or range does not match the primary source, or the source does not support the claim.  A primary source that cannot be reached counts as a failure, reported separately as "unavailable".
- Below 9 of 10, the batch stops; fix the rows, look for the same fault in the unsampled rows, and draw 10 fresh rows.
- One running table records batch, rows checked, correct, unavailable, and the running total.  Review the audit design if the running total falls below 90% after 30 rows (guess).
- A trace that reports zero missed contradictions proves nothing.  The planted flaws 7 and 8 in `docs/baseline-test.md` test for them.

## Labels and the held-out tolerance

Label every threshold "guess" or "measured".  Change a future threshold only in a commit that says why.  The historical tolerances (growth within 0.05 of 1.17; the 2011 count within 10%) never change after the held-out result is seen.

## Still open

Sandbox limits and the isolation mechanism, the trace location and retention, and the writer of the shared state need Anastasiya's answers (`docs/execution-sandbox.md`, `docs/trace-plan.md`, `docs/architecture.md`).
