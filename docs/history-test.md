# History test: what is compared, how, and when (PROPOSED)

Drafted 2026-10-22 by Valerie with Claude Code.  Valerie owns the history test.  Everything here is a proposal until Anastasiya agrees, except the two tolerances, which Valerie accepted on 2026-10-22 and Anastasiya has not yet confirmed.  Items marked (assumption) have no support in the data we hold.

## The question

Does the model, run with the Donana parameters, grow a population from the 2002 Andujar-Cardena count at about the rate the later counts show, and land near the 2011 count that it never saw?  Three counts are all we have (`data/history/counts.csv`), so a pass is weak evidence and the report must say so.

## The data

- 2002:  53 individuals, of which 25 adults.
- 2010:  190 individuals, of which 44 adult females.
- 2011:  214 individuals, of which 90 adults (held out).
- Observed growth:  (190 / 53) ^ (1 / 8) = 1.173 per year from 2002 to 2010;  (214 / 53) ^ (1 / 9) = 1.168 per year to 2011.

## What is compared

- **Quantity:**  total living animals of every age, counted at the same calendar month each year.  The census date is not known to us (assumption:  the end of the year; confirm it before the first run).
- **Growth,** per trial:  (N at month 96 / N at month 0) ^ (1 / 8), where month 0 is the 2002 count and month 96 the 2010 count.
- **Held-out count,** per trial:  N at month 108, the 2011 count.
- **Summary:**  the median of each quantity over all trials of one setting.

## The tolerances (set before any run, never changed after the 2011 result)

- Median growth within 0.05 of 1.17, that is 1.12 to 1.22.
- Median 2011 count within 10% of 214, that is 192.6 to 235.4.

## The starting population (assumption, except the two counts)

- 53 animals:  25 adults and 28 non-adults, from the counts.
- Adults:  whole-month ages drawn uniformly from 36 to 108 months (`breeding_age_min` to `breeding_age_max`); sex 1 : 1 (assumption).
- Non-adults:  whole-month ages drawn uniformly from 0 to 35 months; the cub sex ratio of the table (1.03 females per male).
- All draws use the run seed.  The synthetic 20-lynx start is a separate experiment and is never reused here.

## The one open decision that can break the test

The usable area of the history run sets how many female territories exist (area divided by the 10 km2 home range).  By 2010 the count holds 44 adult females, so the area must allow at least 44 territories, that is 440 km2 or more.  With less, territory capacity and not mortality sets the growth, and the calibration means nothing.  The area of the Andujar-Cardena nucleus is not in our sources.  Decide whether to look it up or to set the area from the 44-female floor and say so.

## Calibration

- Change one parameter only:  post-dispersal annual mortality (`annual_mortality_rate_all_causes`), searched from 0.10 to 0.50.  Every other parameter stays at its baseline.
- Use 2002 to 2010 only.  Choose the mortality whose median growth is closest to 1.17.
- Then run 2011 once.  Report pass or fail against the tolerance.  Do not re-calibrate after that run.
- A hand check with the published rates puts growth near 0.99 at mortality 0.37 and near 1.16 at 0.20.  This is arithmetic and not a simulation result.

## The report must say

The three-anchor limit; that Donana parameters are applied to Andujar-Cardena (a transfer assumption); the starting-population assumptions; the census-date assumption; the trial count; the median and the 10th to 90th percentile of growth and of the 2011 count; and the share of trials that went extinct.
