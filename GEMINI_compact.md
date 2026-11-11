# Operating Workflow

1. **Precedence, scope, and token efficiency:** Prioritize explicit user requirements over this workflow. Operate strictly within this workspace. Before execution, explicitly state Goal, In-Scope boundaries, and Out-of-Scope limitations. Omit conversational filler, status commentary, and preambles; execute the next required tool or command immediately once aligned. Deliver concise, accurate output; state assumptions and tradeoffs, select the simplest sufficient solution, and request clarification if ambiguity blocks safe decisions.
   * **Token & Context Optimization (Maximize Performance):** Never dump large files, full logs, or verbose stdout into context. Use targeted line-range reads, ripgrep/AST filters, or scripts in `memory/script/` (and `{subproject}/memory/script/`) emitting compact summaries (exit codes, JSON metrics, `file:line` refs). Offload repetitive reasoning, parsing, and batch operations to scripts.

2. **Full Lazy-Loading Context, Memory Lifecycle & Skill Registry (Root & Sub-Projects):**
   * **Turn-1 Minimal Initialization (Preserve Token Buffer):** At Turn 1, **do NOT** load `memory/project.md`, `memory/rules.md`, `memory/tools.md`, or scan the codebase. Load strictly in sequence:
     1. `memory/refs.md` (plus `{subproject}/memory/refs.md` if sub-project scoped).
     2. The **single most recent active `memory/{YYYY-MM-DD}/session.md`** in `refs.md` for baseline state, last step, and active blockers.
     3. Detect current ISO date; create/read today's `memory/{YYYY-MM-DD}/session.md` via the Session Template if absent, and run the **Automated Memory Pruning & Consolidation Policy** if daily logs exceed the rolling window.
   * **Phase-Gated On-Demand Lazy Loading:**
     * **Planning & Sub-Task Generation Phase:** Lazy-load **only** relevant sections of `memory/project.md` (via heading/line-range reads) and inspect **only** in-scope source files. Never read all of `memory/project.md` or the full codebase during routine tasks.
     * **Pre-Implementation & Execution Phase:** Load `memory/rules.md` and `memory/tools.md` (root and active sub-project) **immediately before** code generation, script creation, or implementation to ingest constraints, style rules, and registered tools.
     * **On-Demand Deep Research (`memory/research/`):** Do **not** auto-load at startup. Read `memory/research/libs.md` or `memory/research/{topic}.md` (top 15-line `TL;DR` header first) **only** when evaluating dependencies, CVEs, architecture, or algorithms. Persist new syntheses to `memory/research/{topic}.md` and package evaluations to `memory/research/libs.md` across active sub-project and root `memory/`.
     * **On-Demand Root Cause Analysis (`memory/rca/{topic}.md`):** Do **not** auto-load at startup. When investigating root causes, anomalies, vulnerabilities, or hard bugs (race conditions, memory leaks, tail-latency spikes, state corruption, non-determinism), check `memory/refs.md` for prior RCAs (`TL;DR` header first). Write full forensics to `{subproject}/memory/rca/{topic}.md` AND cascade/mirror to root `memory/rca/{topic}.md` and `refs.md`.
   * **Automated Memory Pruning & Consolidation Policy (10-Session Rolling Window):**
     * **Rolling Window Enforcement:** Retain strictly the **last 10 individual daily session logs** (`memory/{YYYY-MM-DD}/session.md`) in root and each active sub-project.
     * **Distillation & Rollup Before Purge:** When daily session directories exceed 10, distill all older logs scheduled for eviction (outcomes, architectural decisions, resolved blockers, invariants, benchmark baselines) into a chronological rollup file: `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` (using the **Consolidated Rollup Session Template**).
     * **Disk Purge & Index Pruning (`memory/refs.md`):** After verifying the rollup file on disk, permanently delete purged `memory/{YYYY-MM-DD}/` directories. Immediately update `memory/refs.md` by removing deleted session paths and adding the `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` reference.
   * **Missing Memory Initialization:**
     * **Missing `memory/project.md`:** Scan codebase once to generate it via the **Project Architecture Template** (all 15 sections).
     * **Missing `memory/rules.md`:** Initialize with code style, conventions, negative constraints, quality criteria, and engineering standards.
     * **Missing `memory/tools.md`, `memory/research/`, `memory/rca/`, & Script Directories:** Initialize `memory/tools.md` via the **Tool & Skill Library Template**. Ensure `script/`, `scratchpad/`, `research/` (with `libs.md`), and `rca/` exist inside `memory/` for both root and active sub-projects (`backend/memory/`, `frontend/memory/`), and verify `**/memory/scratchpad/` is in `.gitignore`.
   * **Cascading Multi-Repo & Sub-Project Updates (`root`, `backend`, `frontend`):** In multi-repo, monorepo, or nested layouts, **synchronize the full `memory/` ecosystem across all touched parent and child directories**:
     * **Scoped + Cascaded Artifacts:** Write sub-project-specific RCAs, research, library evaluations, probes, or scripts to `{subproject}/memory/` (`rca/{topic}.md`, `research/`, `script/`, `tools.md`, `scratchpad/`) **AND** cascade/register them in `root/memory/` (`rca/{topic}.md`, `refs.md`, `tools.md`, `{YYYY-MM-DD}/session.md`).
     * **Cross-Boundary Changes:** When changes, bugs, or benchmarks span `frontend` and `backend`, update `root/memory/`, `frontend/memory/`, and `backend/memory/` simultaneously.

3. **Scratchpad vs. Reusable Script Lifecycle (`memory/scratchpad/` & `memory/script/` across Root & Sub-Projects):**
   * **Consult `memory/tools.md` First:** Before writing ad-hoc commands or scripts, check root and `{subproject}/memory/tools.md` to reuse existing automation in `memory/script/`.
   * **`memory/scratchpad/` (Ephemeral Sandbox — Git-Ignored):** Place all temporary scripts (Python, Shell, TS/Bun), one-off probes, hypothesis tests, reproducers, fault-injection harnesses, and draft proofs strictly inside `memory/scratchpad/` (or `{subproject}/memory/scratchpad/`). Keep `**/memory/scratchpad/` in `.gitignore`.
   * **`memory/script/` (Persistent Pipelines & Token-Saving Tools):** Store reusable pipelines, benchmark harnesses, validators, memory-pruners, CVE/security auditors, regression reproducers, and automation in `memory/script/` (or `{subproject}/memory/script/`). Accept CLI arguments and emit compact, token-efficient summaries. Graduate reusable scripts from `scratchpad/` to `script/` and register in both `{subproject}/memory/tools.md` and root `memory/tools.md`.

4. **Pre-plan alignment gate & Choice Architecture (Observability, Benchmark, Validation):** Before planning or executing tools, files, commands, or code changes, **explicitly ask and align with the user every time without exception** on the Choice Architecture and three pillars below. **Never skip or assume alignment, even if prior context exists in prompts or `memory/`.**
   * **Structured Choice Architecture (Active Engineering Guidance):** Do not ask open-ended questions. Guide the user by presenting either:
     1. **Mode A — Prioritized Recommendation (When a clear optimal path exists):** Present the single leanest, highest-leverage path with concise rationale, explicit invariants, and resource profile; ask user to confirm or override.
     2. **Mode B — Open Choice Matrix (When genuine architectural or operational trade-offs exist):** Present a comparison table contrasting **2–3 functional options** across:
        * **Execution Profile & Complexity:** Time/space bounds, I/O concurrency model, implementation/maintenance surface.
        * **Memory Ceilings (Allocation Footprints):** Steady-state heap/stack, peak footprint, buffer/cache bounds, GC/allocator pressure (normal vs. worst-case).
        * **Tail-Latency Distributions (`p95` / `p99` / `p99.9`):** Latency under **normal** vs. **pathological/worst-case payloads** (lock contention, cold starts, payload amplification, skew).
        * **Security & Failure Blast Radius:** Trust boundary exposure, failure recovery, rollback safety.
   * **Three Mandatory Alignment Pillars:**
     * **Observability:** How state, flow, security events, and failures are inspected across affected scopes (`backend`, `frontend`, infra) via structured logs, metrics, traces, debug outputs, health endpoints, audit trails, or UI/DOM inspection.
     * **Benchmark (Normal + Non-Normal / Adversarial Cases & Performance Budgets):** How performance, Memory Ceilings, and resilience baselines vs. targets are measured, **explicitly covering non-normal conditions:**
       * **Tail Latency:** Measure `p50`, `p95`, `p99`, and `p99.9` to expose jitter, GC pauses, and queuing stalls.
       * **Anomalies:** Test spikes, clock skew, partial network/IO failures, corrupted/malformed payloads, and out-of-order events.
       * **Edge Cases:** Test boundaries (`0`, `1`, `MAX_INT`, empty collections, deep nesting, high-cardinality keys, Unicode/binary extremes).
       * **Worst-Case Complexity, Saturation & Abuse:** Test pathological/adversarial inputs triggering worst-case time/space complexity (hash collisions, ReDoS, unindexed scans, payload amplification), lock contention, cold starts, and memory/CPU saturation against Memory Ceilings.
     * **Validation (Correctness, Security & Maintainability):** Exact acceptance criteria, deterministic commands, formal invariants, security/CVE checks, and pass/fail thresholds across normal and non-normal regimes.

5. **Plan, formal reasoning, root cause analysis, and implement:** After alignment, lazy-load required sections of `memory/project.md` and record a verification plan (objective, edge cases, security/performance impact, module impact across root and sub-projects). Mitigate highest-risk unknowns, core logic dependencies, threat vectors, or architectural uncertainties first (consulting/updating `memory/research/{topic}.md` or `memory/rca/{topic}.md` in sub-project and root `memory/`).
   * **Abstraction, Hypothesis, Lean Proof & Testing Protocol:** When requested, debugging hard RCAs (`memory/rca/{topic}.md`), or modifying complex algorithms, security/auth boundaries, concurrency, state machines, or core invariants, construct and verify:
     1. **Abstraction:** Distill target logic/failure into a minimal, implementation-agnostic model (types, state space, trust boundaries, I/O, transition rules).
     2. **Hypothesis:** State falsifiable claims, pre/post-conditions, failure triggers, Memory Ceilings, complexity bounds, and safety/liveness/security invariants.
     3. **Lean Proof:** Formulate a step-by-step formal/mathematical proof (or executable Lean 4 proof in `memory/scratchpad/` or `{subproject}/memory/scratchpad/`) proving invariants hold (or why the defect occurred and the fix eliminates reachable failure states) across base, transition, and worst-case conditions.
     4. **Testing:** Map abstraction boundaries, hypotheses, and proof obligations directly to automated unit, property-based, security/fuzzing, regression, adversarial benchmark, and edge-case tests (temporary probes in `scratchpad/`, persistent suites in `script/`).
   * **Pre-Implementation Gate:** Load `memory/rules.md` and `memory/tools.md` before modifying code. For core business logic changes, confirm with the user via the Walkthrough Artifact. Implement sequentially; preserve local style; avoid unrequested features, abstractions, or refactors. Delete only unused code caused by the change.

6. **Engineering, performance, security, CVE, and maintenance standards:** Follow root and sub-project `memory/rules.md` first. Where unspecified, enforce:
   * **Clean & Maintainable Architecture:** Write simple, modular, strictly typed, readable code. Keep entry points to orchestration; isolate business logic. Prevent circular dependencies, minimize cyclomatic/cognitive complexity, and maintain backward compatibility or explicit schema/API migrations.
   * **Performance Engineering & Memory Ceiling Discipline:** Enforce bounded memory, queues, caches, and payloads (zero unbounded growth/OOM risk). Eliminate N+1 queries, event-loop blocking I/O, and redundant hot-path allocations/serializations. Prefer $O(1)$ or $O(\log n)$ lookups over linear scans in critical loops.
   * **Security & Vulnerability Hardening (Zero-Trust / OWASP / CWE):** Validate/sanitize all external inputs at trust boundaries with strict schemas. Prevent SQL/NoSQL/Command Injection (parameterized queries/safe APIs), XSS, CSRF, SSRF, Path Traversal, Prototype Pollution, Insecure Deserialization, and ReDoS. Enforce least-privilege RBAC/ABAC on protected routes/actions. Never hardcode, log, or expose secrets, tokens, or PII.
   * **CVE, Dependency & Supply-Chain Hygiene:** Before adding, upgrading, or replacing dependencies in root, `frontend`, or `backend`, check `memory/research/libs.md` (and `{subproject}/memory/research/libs.md`), evaluate built-in alternatives, and verify maintainer reputation, license, activity, transitive bloat, and CVEs (`bun audit` / `uv run pip-audit`). Zero tolerance for unmitigated Critical/High CVEs. Record evaluations in sub-project and root `memory/research/libs.md`, pin exact versions, verify lockfiles, and use `bun` (FE/Node) or `uv` (Python).
   * **Mandatory Unused Code Deletion Standard (Frontend & Backend):** Zero tolerance for dead/unused code. **Permanently delete** all unused imports, variables, parameters, functions, dead methods, unreachable branches, and commented-out code (never comment out or suppress). Run `bun run clean:unused` (FE) and `uv run ruff check --fix --select F401` (BE). Prefer React TS functional components with hooks, Node.js TS services, and UI styling in priority order: NaiveUI > DaisyUI > Tailwind, with global color styling when required. Comply with PEP 8 and ESLint.

7. **Safety and verification:** Verify empirically: run aligned **Observability**, **Benchmark** (`p95`/`p99`/`p99.9` tail latency, Memory Ceilings, anomalies, edge/worst cases), and **Validation** checks via terminal commands, compile/lint checks, security/CVE audits, and unit/property tests across touched sub-projects. Before advancing, ask: *"What anomaly, tail-latency spike, memory-ceiling breach, exploit, edge case, or worst-case input could falsify this Hypothesis or Lean Proof?"* and test it in `memory/scratchpad/` (or `{subproject}/memory/scratchpad/`). For RCA/vulnerability fixes (`memory/rca/{topic}.md`), verify the deterministic reproducer fails pre-fix and passes post-fix, syncing the RCA across `{subproject}/memory/rca/{topic}.md` and root `memory/rca/{topic}.md`. Never force-delete, wipe DBs, or clean Git without explicit instruction. Check ports and prevent orphaned servers. For UI changes, inspect the page and capture a screenshot. Document and fix failures, then re-verify. For major changes, provide a Walkthrough Artifact (modified files, compile output, security/CVE status, normal vs. worst-case benchmarks, test results).

---

### Pre-Plan Choice Architecture Template (Used in Section 4 Alignment Gate)
*Present Mode A (Prioritized Recommendation) or Mode B (Open Choice Matrix) alongside Observability, Benchmark, and Validation alignment questions:*

```markdown
### Architectural & Execution Alignment
* **Selected Guidance Mode:** {Mode A: Prioritized Recommendation | Mode B: Open Choice Matrix}
* **Prioritized Recommendation:** {Option Name} — {Concise rationale for leanest, highest-leverage path}

| Option | Execution Profile & Complexity | Memory Ceiling (Normal vs. Pathological) | Tail Latency `p95` / `p99` / `p99.9` (Normal vs. Worst-Case) | Key Trade-Off / Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| **Option 1 (Recommended)** | `{e.g., O(1) ring buffer, non-blocking}` | `{Bounded: <= 16MB fixed}` | `{Normal: 2/4/7ms | Worst: 5/9/14ms}` | `{Fixed capacity; drops oldest on overflow}` |
| **Option 2** | `{e.g., Dynamic heap queue}` | `{Unbounded peak: ~250MB+ under spike}` | `{Normal: 2/5/9ms | Worst: 45/180/600ms (GC stall)}` | `{Risk of OOM / tail-latency amplification}` |
```

---

### Root Cause Analysis (RCA) & Vulnerability Forensics Template (`memory/rca/{topic}.md` & `{subproject}/memory/rca/{topic}.md`)
*On-demand only (do not auto-load at startup). Write to affected `{subproject}/memory/rca/{topic}.md` AND sync to root `memory/rca/{topic}.md`. Keep `TL;DR` header within top 15 lines:*

```markdown
# Root Cause Analysis: {Topic / Bug / CVE Identifier}
* **Date:** {YYYY-MM-DD} | **Scope:** {Root / Backend / Frontend / Cross-Stack} | **Severity:** {Critical / High / Medium} | **Category:** {Bug / Tail-Latency / Memory-Leak / Concurrency / Security-Vulnerability / CVE} | **Status:** {Investigating / Root Cause Proven / Fixed & Verified}
* **TL;DR Symptom / Impact:** {1–2 sentences on observed failure, exploit vector, anomaly, or latency spike}
* **TL;DR Root Cause (`file:line`):** {Exact mechanism, CWE/CVE ID, broken invariant, and `{subproject}/file:line` origin}
* **TL;DR Permanent Fix:** {Concise summary of structural fix, hardening, and enforced invariant}

---
## 1. Failure Manifestation, Threat Vector & Observability Evidence
* Error traces, log signatures, metric anomalies (`p99`/`p99.9` spikes, memory ceiling breaches), or exploit preconditions.

## 2. Minimal Deterministic Reproducer (`{subproject}/memory/scratchpad/` or `{subproject}/memory/script/`)
* Exact command, payload, timing schedule, or adversarial condition reproducing the issue 100% deterministically.

## 3. Fault Tree & Hypothesis Elimination Log
* **Hypothesis A:** {Claim} → **Test/Probe:** {Command/Script} → **Result:** `Falsified` / `Confirmed` ({Evidence}).
* **Hypothesis B:** {Claim} → **Test/Probe:** {Command/Script} → **Result:** `Confirmed` ({Exact causal chain}).

## 4. Formal Mechanism & Broken Invariant (Abstraction & Lean Proof)
* State transition trace to illegal/vulnerable state, violated invariant, and formal proof that the new constraint prevents re-entry across edge/worst cases.

## 5. Remediation, Regression Tests & Blast-Radius Check
* Modified `{subproject}/file:line` paths, regression/security test commands added, before/after normal & worst-case benchmarks, audited sibling modules, and synced RCA paths (`root/memory/rca/{topic}.md` ↔ `{subproject}/memory/rca/{topic}.md`).
```

---

### Deep Research Templates (`memory/research/{topic}.md` & `memory/research/libs.md` — Root & Sub-Project Scoped)
*On-demand only (do not auto-load at startup). Write sub-project research/libraries to `{subproject}/memory/research/` and sync to root `memory/research/`. Keep `TL;DR` header within top 15 lines:*

#### 1. Topic Deep-Research Template (`memory/research/{topic}.md` & `{subproject}/memory/research/{topic}.md`)
```markdown
# Deep Research: {Topic Name}
* **Date:** {YYYY-MM-DD} | **Scope:** {Root / Backend / Frontend / Shared} | **Status:** {Verified / Draft / Superseded}
* **TL;DR Conclusion:** {1–3 sentences stating technical decision, chosen algorithm/architecture, and key constraint}
* **Adopted Pattern / Invariant:** {Exact formula, protocol, memory ceiling, security boundary, or rule to apply}

---
## 1. Problem Context & Scope
* Trigger context and affected root/sub-project components (`backend`, `frontend`).

## 2. Comparative Analysis, Memory Ceilings & Tail-Latency Tradeoffs
* Evaluated options, time/space complexity, allocation footprints, `p95`/`p99`/`p99.9` behavior (normal vs. pathological), maintenance burden, and failure modes.

## 3. Security, Vulnerability Surface & Worst-Case Bounds
* Formal bounds, threat vectors (OWASP/CWE), pathological inputs, and concurrency/memory hazards.

## 4. Implementation Blueprint & References
* Integration steps, code patterns, synced research paths, and source links/benchmarks.
```

#### 2. Library, CVE & Dependency Research Registry (`memory/research/libs.md` & `{subproject}/memory/research/libs.md`)
```markdown
# Library, CVE & Dependency Research Registry (`memory/research/libs.md`)

> **On-Demand Lookup Policy:** Consult this file (and `{subproject}/memory/research/libs.md`) before adding, upgrading, auditing, or replacing dependencies. Read only the summary table or target package section to save tokens.

## Evaluated Libraries Index

| Package / Library | Scope (`FE`/`BE`/`Root`) | Domain / Purpose | Pinned Version | Decision (`Adopted` / `Rejected` / `Deprecated`) | CVE & Maintenance Status | Memory Ceiling & Tail-Latency (`p95`/`p99`/`p99.9`) Notes | Alternatives Considered |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `{pkg-name}` | `{BE / FE}` | `{e.g., Schema Validation}` | `{x.y.z}` | `Adopted` | `0 CVEs / Active` | `{Low p99 overhead, zero-alloc hot path}` | `{Alt1, Alt2}` |

## Detailed Package, Security & Maintenance Evaluations
### `{pkg-name}` (`{x.y.z}`) — {Scope: Backend / Frontend / Root} — {Adopted / Rejected / Deprecated}
* **Security, Vulnerability & CVE Audit:** {CVE history, CWE exposure, transitive risk, audit result, license}
* **Maintenance & Longevity:** {Maintainer health, release cadence, breaking-change frequency, deprecation risk, upgrade path}
* **Benchmark, Memory Ceiling & Worst-Case Profile:** {Peak memory, cold-start cost, bundle size, p95/p99/p99.9 latency under pathological payloads}
* **Integration Constraints & Gotchas:** {Edge cases, known bugs, required security flags, config rules}
```

---

### Tool & Skill Library Template (`memory/tools.md` & `{subproject}/memory/tools.md`)
*Lazy-load immediately before implementation or tool execution. Initialize if absent in root or sub-project, and sync both registries when scripts are added/updated:*

```markdown
# Tool & Skill Library Registry (`memory/tools.md`)

> **Token Optimization Policy:** Inspect this registry (and `{subproject}/memory/tools.md`) before writing ad-hoc commands or new scripts.
> * **Persistent Automation (`memory/script/` & `{subproject}/memory/script/`):** Version-controlled, reusable pipelines, benchmark runners, memory pruners, security/CVE auditors, and validators emitting compact outputs.
> * **Ephemeral Sandbox (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`):** Git-ignored (`**/memory/scratchpad/`) for temporary hypothesis tests, reproducers, and one-off scripts. Graduate reusable scripts to `script/` and register below.

## Registered Scripts & Skills (`memory/script/` & `{subproject}/memory/script/`)

| Tool / Skill ID | Scope (`Root`/`BE`/`FE`) | Script Path | Purpose & When to Use | Exact Invocation Command | Output Format (Compact) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `clean-unused` | `Root/FE/BE` | `memory/script/clean_unused.sh` | Strip dead imports/code across FE & BE | `bash memory/script/clean_unused.sh` | Exit code + modified file count |
| `bench-tail` | `BE/FE` | `{subproject}/memory/script/bench_tail.py` | Run p50/p95/p99/p99.9, memory-ceiling, anomaly & worst-case benchmarks | `uv run python {subproject}/memory/script/bench_tail.py --target <mod>` | JSON summary (`p50`, `p95`, `p99`, `p99.9`, `max`, `mem_peak`) |
| `sec-audit` | `Root/FE/BE` | `memory/script/sec_audit.sh` | Run CVE audit (`bun audit` / `pip-audit`) & secret/CWE checks | `bash memory/script/sec_audit.sh` | JSON summary (`cve_count`, `severity`, `pkg`, `file:line`) |
| `prune-memory` | `Root/FE/BE` | `memory/script/prune_memory.py` | Enforce 10-session window, generate rollup & prune `refs.md` | `uv run python memory/script/prune_memory.py` | JSON summary (`rolled_up_range`, `purged_count`, `active_count`) |
| `validate-all` | `Root/FE/BE` | `memory/script/validate.sh` | Execute typecheck, lint, unit, and property tests concisely | `bash memory/script/validate.sh` | Pass/Fail summary + failing `file:line` only |

## Active Scratchpad Experiments (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`)
* **Git Status:** Must remain ignored in `.gitignore` (`**/memory/scratchpad/`).
* **Current Probes:** {Active temporary hypothesis/proof/benchmark/RCA scripts across root/BE/FE or `None`}
```

---

### Project Architecture Template (`memory/project.md` & `{subproject}/memory/project.md`)
*Do NOT load in full at Turn 1. Lazy-load specific sections during planning. Generate via a one-time codebase scan if absent:*

```markdown
# Project Architectural Blueprint: {Project / Sub-Project Name}

## 1. Project Overview & Business Domain
* Core mission, problem solved, user domain, stakeholders, and root vs. `backend`/`frontend` boundaries.

## 2. Tech Architecture, Runtime Stack & Dependency Hygiene
* Language versions, frameworks, package managers (`bun`/`uv`), engines, and pinned dependencies (cross-referenced with `libs.md` for CVE/maintenance status).

## 3. Directory Layout & Module Ownership
* Directory tree showing module boundaries, entry points, and root + sub-project `memory/` (`tools.md`, `script/`, `scratchpad/`, `research/`, `rca/`).

## 4. Key Data Models & Schema Mappings
* Database tables, relations, indexes, entity lifecycles, and ORM mappings (Prisma, Drizzle, etc.).

## 5. System Features, Core Mechanics & Performance Budgets
* Core workflows, background jobs, bounded caches, state machines, Memory Ceilings, and hot-path latency budgets.

## 6. Authentication, Authorization, Security & Vulnerability Posture
* Auth providers, JWT/session lifecycles, RBAC/ABAC matrices, input validation boundaries, OWASP/CWE mitigations, CVE audit policies, and secrets management.

## 7. REST API Endpoints Reference
* Routes, HTTP methods, request/response schemas, rate limits, and auth requirements.

## 8. WebSocket & Asynchronous Event Protocol Spec
* Real-time events, channels, schemas, backpressure/payload limits, brokers, and reconnection rules.

## 9. Third-Party Integrations & External Services
* External APIs, payment gateways, webhooks, signature verification, and notifications.

## 10. Restricted & Auto-Generated Files (Do Not Edit)
* Do-not-edit artifacts (generated types, migrations, build outputs).

## 11. Architectural Invariants & ADRs (Key Decisions)
* Key decisions, non-negotiable boundaries, formal invariants, and links to `memory/research/{topic}.md` and `memory/rca/{topic}.md`.

## 12. Observability, Benchmark, Validation & Security Testing Strategy
* **Observability:** Logs, metrics, traces, security audit trails, and state inspection.
* **Benchmark (Normal & Adversarial):** Baseline vs. target SLAs for `p50`/`p95`/`p99`/`p99.9` tail latency, Memory Ceilings, anomalies, edge cases, and worst-case/DoS inputs.
* **Validation, Security & Formal Verification:** Unit, property, integration, E2E, and security/CVE audit commands, Abstraction/Hypothesis/Lean Proof artifacts, DB isolation, and fixtures.

## 13. Running Local Infrastructure
* Ports, DB containers, env setup, and seed commands.

## 14. Containerized & Production Cloud Deployments
* Dockerfiles (non-root, minimal images), Cloud Run/K8s manifests, resource limits, env flags, and CI/CD pipelines.

## 15. Known Technical Debt, Maintenance Risks & Fragile Areas
* Bottlenecks, tail-latency risks, deprecated packages, security/CVE watch items, legacy code, concurrency hazards, and links to `memory/rca/{topic}.md`.
```

---

### Session & Consolidation Templates (`memory/{YYYY-MM-DD}/session.md`, `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` & `memory/refs.md`)

#### 1. Active Daily Session Log Template (`memory/{YYYY-MM-DD}/session.md` & `{subproject}/memory/{YYYY-MM-DD}/session.md`)
*Load only the single most recent session log at Turn 1. Retain max 10 individual daily logs on disk:*

```markdown
# Session Log: {YYYY-MM-DD} ({Root / Sub-Project Scope})

### Previous Session Tracking
* **Last Session Date:** {YYYY-MM-DD or None}
* **Final Status:** {Previous ending state summary}
* **Key Achievements:** {Verified accomplishments}
* **Leftover Blockers:** {Carried-forward issues}

### Choice Architecture & Alignment Contract
* **Selected Option & Rationale:** {Chosen option from Mode A or Mode B}
* **Observability Criteria:** {Aligned logs, traces, metrics, audit outputs, or state checks across root/BE/FE}
* **Benchmark Targets (Normal, Non-Normal, Tail-Latency & Memory Ceilings):** {Baselines & targets for p50/p95/p99/p99.9 latency, Memory Ceilings, anomalies, edge cases, and worst-case inputs}
* **Validation, Security & Maintenance Criteria:** {Acceptance checks, formal invariants, CVE/security checks, and pass/fail commands}
* **Formal Reasoning (If Applicable):** {Abstraction, Hypothesis, Lean Proof, and Test mapping summary}
* **Tools, Scratchpad, Research & RCA Used (Root & Sub-Projects):** {Scripts in `script/`, probes in `scratchpad/`, audits in `research/`, or RCAs in `rca/` across root/BE/FE}

### Current Session Tracking
* **Active Task:** {In-scope objective}
* **Touched Scopes (`Root` / `Backend` / `Frontend`):** {Synchronized `memory/` directories}
* **Last Completed Step:** {Most recent verified command, tool, or edit}
* **Next Action:** {Immediate next programmatic step or tool call}
* **Summary of Activity:** {Concise session changelog}
* **Progress / Changes:** {Modified files, modules, and tests}
* **Blockers / Unresolved Items:** {Active blockers or `None`}
```

#### 2. Consolidated Rollup Session Template (`memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md`)
*Auto-generated when pruning daily session logs beyond the 10-session rolling window:*

```markdown
# Consolidated Session Rollup: {START_YYYY-MM-DD} to {END_YYYY-MM-DD} ({Root / Sub-Project Scope})
* **Purged Daily Sessions Count:** {N sessions consolidated and deleted}
* **TL;DR Era Summary:** {2–3 sentences on milestones, architectural shifts, and stability/performance posture}

## 1. Key Architectural & Feature Outcomes
* Chronological list of permanent features, migrations, and module changes (`file:line` refs).

## 2. Established Invariants, Benchmarks & Memory Ceilings
* Verified `p50`/`p95`/`p99`/`p99.9` baselines, Memory Ceilings, and formal proofs established.

## 3. Linked Deep Research & Root Cause Analyses (Preserved On-Demand)
* Pointers to permanent `memory/research/{topic}.md`, `memory/research/libs.md`, and `memory/rca/{topic}.md` artifacts.

## 4. Carried-Forward Tech Debt & Historical Blockers
* Long-term caveats or deferred items transferred to the active window.
```

#### 3. Active Reference Manifest Template (`memory/refs.md` & `{subproject}/memory/refs.md`)
*Loaded at Turn 1. Auto-pruned when daily sessions roll up:*

```markdown
# Memory Reference Manifest (`memory/refs.md`)

## 1. Latest Active Session (Load at Turn 1)
* **Current / Most Recent Session:** `memory/{YYYY-MM-DD}/session.md` — {Active task & blocker summary}

## 2. Rolling 10-Session Window (Max 10 Individual Logs)
1. `memory/{YYYY-MM-DD}/session.md` — {1-line outcome summary}
*(Keep strictly <= 10 entries; consolidate older entries into Section 3 and delete their folders from disk)*

## 3. Consolidated Chronological Rollups (Archived Windows)
* `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` — {1-line distilled era summary}

## 4. On-Demand Deep Research & RCA Index (Lazy-Load Only When Relevant)
* **Libraries & CVE Registry:** `memory/research/libs.md`
* **Research Topics:** `memory/research/{topic}.md` — {1-line TL;DR}
* **Root Cause Analyses:** `memory/rca/{topic}.md` — {1-line TL;DR root cause & fix}
```
