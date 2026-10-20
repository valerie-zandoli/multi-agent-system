# Research notes for the Iberian lynx parameter table (DRAFT)

Drafted 2026-10-20 on branch `dev-valerie` by Valerie with Claude Code.  Nothing here is on `main` until Anastasiya reviews it by pull request.

## How to read the table

- `data/parameters/iberian_lynx_baseline.csv` uses Anastasiya's eight columns.  The file format and the `source` keys are a proposal for the validator; she decides.
- Every `source` value is a key in `data/parameters/sources.csv`, which records how each source was read (full text, abstract only, or second-hand).
- In `evidence_or_assumption`, "Published" means the value or range appears in the source.  "Chosen by us" means we picked a sensitivity range; no source gives one.  "SECOND-HAND" means we have not opened the primary paper.  "ASSUMPTION" means the model needs the number and no source gives it.
- Intervals marked Wilson were computed by us from a published percentage and its n.

## Proposed study population and period (decision needed from both of us)

- **Parameters:** Donana, Coto del Rey, 1992 to 2001 (palomares2005).  It is the only source with full reproduction and cub survival.
- **History test:** Andujar-Cardena, 2002 to 2011, adult counts 25 then 90 (catsg).  That is growth of about 1.15 per year (computed by us: 90/25 over 9 years).  Donana is a poor history test because of the 2007 feline leukaemia outbreak and later genetic reinforcement.
- **Mismatch to resolve:** parameters come from one population and the test from another.  Releases and management also helped Andujar-Cardena grow: about 300 rabbit-habitat agreements covering about 250,000 ha across Spain and Portugal (eu_spain_report2018), and connectivity work from 2008 and 2009.  So the model should be expected to match the trend only roughly.
- **Still needed before runs:** a yearly census series (we have only two adult counts for Andujar-Cardena), the error measure and tolerance, and a split between calibration years and validation years.

## How food and habitat should enter the model (what the evidence supports)

- In Coto del Rey, rabbit density ranged from 4 to 55 per hectare and had no significant link with breeding females, cubs born, or cub survival (palomares2005; n=8 years, so low power).  One cub starved in the year with the lowest density.
- The EU report gives thresholds of about 1 rabbit per hectare in autumn and 4.6 in spring for territorial breeding lynx (second-hand).
- Home ranges are smaller where rabbits are abundant, and female ranges are exclusive (catsg).  Breeding females need a territory.
- **Proposal:** food and habitat act on the number of female territories a patch can hold (patch area divided by female home range, with home range shrinking as rabbits increase), not directly on litter size or cub survival.  Below the spring threshold, territorial breeding fails.
- **Consequence:** the medium (4.6) and high (55) food levels may give similar persistence.  If they do, that matches the evidence and is not a bug.
- **Habitat quality independent of rabbits:** females gave birth in hollow trees wider than 0.9 m (palomares2005 methods), so natal den count is one measurable habitat factor.  Connectivity: catsg says lynx have difficulty crossing open areas wider than 5 km.

## Assumptions the model must make

- The exact shape of territory size versus rabbit density (no published function was read).
- The share of cub deaths that depend on food (palomares2005 found none in range).
- Initial age and sex structure for the starting population.
- Which source of mortality to include; avoid double counting with `annual_mortality_rate_all_causes`.

## Gaps and conflicts to resolve

- No age-specific adult or juvenile survival yet.  The one all-cause rate (0.37, 1983 to 1989) comes from an abstract and is likely too high for a protected subpopulation.
- Sierra Morena demography is missing.  Candidates to read: Rodriguez and Delibes 2004 (non-natural mortality, Biological Conservation 118: 151-161) and Simon et al. 2012 (Conservation Biology 26: 731-736), both listed in the EU report.
- Gaona, Ferreras, and Delibes 1998 (Ecological Monographs 68: 349-370) is a viability model for Donana.  palomares2005 says its most sensitive parameters after the first were reproductive rate, cub mortality, and juvenile mortality.  Read it for parameter structure.
- Primary paper for the rabbit thresholds (palomares2001) has not been read.
- Breeding age conflict: 3 years in palomares2005 versus "can breed at two years" in catsg.
- palomares2005 reports lifetime output as 11 to 19 cubs in the abstract but at least 14, 8, and 19 in the text.
- The disease, genetics, and maps are deferred by agreement.
- Survival of released lynx was 56 to 83% (WWF conference conclusions 2019); this is not in the table because the model has no releases.
