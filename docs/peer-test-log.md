# Peer-test log

One entry per outside tester.  A tester reads `docs/architecture.md` and `docs/agent-handoffs.md` cold and answers three questions:  which handoff has unclear contents, which role has no owner, and which shared state has no named writer.

## 2026-10-22:  Abheeshu Dhungana (Slack group chat)

**What he sent.**  An overall assessment instead of the three answers.  Strong points:  contract-first design, a solid test suite, the 3-round cap, and clean git hygiene.  In progress:  contracts versus runtime, and biological complexity.  A second message said the app will help humans understand predator-prey ratios and that AI could compare animal numbers as a group.

**What we take from it.**
- He read the project as an AI tool that compares predator and prey numbers.  It is a simulation with AI roles around it, so the documents did not say clearly what the agents are.  Fixed:  "In plain words" in `docs/architecture.md` now separates the three AI roles, the harness, the simulated animals, and the coding assistants.
- He saw "contracts, not runtime".  That is true, and the documents did not say it up front.  Fixed:  the same section lists what is built and what is planned.
- He named no unclear handoff, ownerless role, or unwritten shared state.  The three questions are now answered in the documents themselves:  "The three handoffs", "Who owns what", and "The shared state and who writes it".
- One figure did not match:  he counted "60+ unit tests"; the suite has 47 in the required check.  We do not act on it.

**Still open.**  Wil Sheppard has not replied (due Friday 2026-10-23 at 18:00 ET).  The return review of their design is owed once they send a link.
