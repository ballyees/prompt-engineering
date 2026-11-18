# Root Cause Analysis: {Topic / Bug / CVE Identifier}
* **Date:** {YYYY-MM-DD} | **Scope:** {Root / Backend / Frontend / Cross-Stack} | **Severity:** {Critical / High / Medium} | **Category:** {Bug / Tail-Latency / Memory-Leak / Concurrency / Security-Vulnerability / CVE} | **Status:** {Investigating / Root Cause Proven / Fixed & Verified}
* **TL;DR Symptom / Impact:** {1–2 sentences describing the exact observed failure, exploit vector, anomaly, or tail-latency spike}
* **TL;DR Root Cause (`file:line`):** {Exact mechanism, CWE/CVE ID if applicable, broken invariant, and `{subproject}/file:line` where the defect originates}
* **TL;DR Permanent Fix:** {Concise summary of the structural fix, security hardening, and newly enforced invariant}

---
## 1. Failure Manifestation, Threat Vector & Observability Evidence
* Exact error traces, structured log signatures, metric anomalies (`p99`/`p99.9` spikes, memory ceiling breaches), or exploit preconditions required to trigger the issue.

## 2. Minimal Deterministic Reproducer (`{subproject}/memory/scratchpad/` or `{subproject}/memory/script/`)
* Exact command, input payload, concurrency/timing schedule, or adversarial condition that reproduces the failure or vulnerability 100% deterministically.

## 3. Fault Tree & Hypothesis Elimination Log
* **Hypothesis A:** {Claim} → **Test/Probe:** {Command/Script} → **Result:** `Falsified` / `Confirmed` ({Brief evidence — prevents repeating dead ends}).
* **Hypothesis B:** {Claim} → **Test/Probe:** {Command/Script} → **Result:** `Confirmed` ({Exact causal chain}).

## 4. Formal Mechanism & Broken Invariant (Abstraction, Hypothesis & Lean Proof)
* Step-by-step state transition trace showing how the system enters the illegal/vulnerable state, the exact invariant violated, and the formal/logical proof that the new constraint prevents re-entry across base cases, inductive/state transitions, and worst-case boundary conditions.

## 5. Remediation, Regression Tests & Blast-Radius Check
* Modified `{subproject}/file:line` locations, regression/security test commands added to the suite, before/after normal & worst-case benchmark results, sibling modules audited across `backend`/`frontend`, and synced RCA paths (`root/memory/rca/{topic}.md` ↔ `{subproject}/memory/rca/{topic}.md`).
