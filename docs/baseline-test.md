# Baseline test: do three roles beat one agent? (DRAFT)

Drafted 2026-10-22 by Valerie (Evaluator owner) with Claude Code.  LaNice's lesson on multi-agent systems says to stay with one agent until it clearly breaks.  This test checks whether our split earns its cost.

## Planted flaws

Six runs, each a copy of an otherwise valid run with one flaw:

1. births and deaths do not balance in one month;
2. a parameter outside its published range;
3. an unknown source key;
4. the trapping share added on top of the all-cause mortality (a double count);
5. the 2011 count used inside the calibration (history leakage);
6. persistence computed from the wrong endpoint.

## Arms

- A:  one agent does research, simulation, and evaluation in one session.
- B:  one agent, then a second pass in a fresh session that changes nothing.
- C:  the three roles through the harness.

## Procedure

- The same six cases, the same model, and the same prompt budget for every arm; each arm runs each case 5 times.
- Record flaws caught, false alarms, tokens, and minutes.
- Score with arm labels hidden (a script, or a person who does not know the arm).
- Arms A and B can run with hand-prepared files before the harness exists; arm C waits for the harness.

## Bar (written before any run)

Arm C must catch at least 1 more planted flaw per run than arm B on average, with no more false alarms.

## If the bar is missed

Report the counts plainly, including any case where one agent matched or beat the team.  The split is then justified only by independent review and separate permissions, and the PRD says so.

## Limits

Six cases times five runs is a small sample.  Report counts, not significance claims.
