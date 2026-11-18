# Memory Reference Manifest (`memory/refs.md`)

## 1. Latest Active Session (Load at Turn 1)
* **Current / Most Recent Session:** `memory/{YYYY-MM-DD}/session.md` — {Active task & blocker summary}

## 2. Recent Individual Sessions
1. `memory/{YYYY-MM-DD}/session.md` — {1-line outcome summary}
*(Keep all entries unless the user requests pruning; then consolidate older entries into Section 3 and delete their individual folders within the requested scope.)*

## 3. Consolidated Chronological Rollups (Archived Windows)
* `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` — {1-line distilled era summary}

## 4. On-Demand Deep Research & RCA Index (Lazy-Load Only When Relevant)
* **Libraries & CVE Registry:** `memory/research/libs.md`
* **Research Topics:** `memory/research/{topic}.md` — {1-line TL;DR}
* **Root Cause Analyses:** `memory/rca/{topic}.md` — {1-line TL;DR root cause & fix}
