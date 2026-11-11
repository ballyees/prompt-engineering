# Operating Workflow

1. **Precedence, scope, and token efficiency:** Follow explicit user requirements before this workflow. Work only in this workspace. Before executing work, perform strict scope definition by explicitly stating the Goal, In-Scope boundaries, and Out-of-Scope limitations. Eliminate conversational filler, status commentary, and text preambles; execute the next required development tool or terminal command immediately once aligned. Write concise, accurate, professional output; state assumptions and tradeoffs, choose the simplest sufficient solution, and request clarification when ambiguity blocks a safe decision.
   * **Token & Context Optimization (Maximize Performance):** Never dump large files, full logs, or verbose stdout into context. Use targeted line-range reads, ripgrep/AST filters, or executable scripts in `memory/script/` (and sub-project `{subproject}/memory/script/`) that emit compact, structured summaries (exit codes, JSON metrics, or `file:line` references). Offload repetitive reasoning, parsing, and batch operations to scripts rather than LLM token generation.

2. **Full Lazy-Loading Context, Memory Lifecycle & Skill Registry (Root & Sub-Projects):**
   * **Turn-1 Minimal Initialization (Preserve Token Buffer):** At session initialization (first chat turn), **do NOT** load `memory/project.md`, `memory/rules.md`, `memory/tools.md`, or parse the application codebase. Load strictly in sequence:
     1. `memory/refs.md` (and target `{subproject}/memory/refs.md` if scoped to a specific sub-project).
     2. The **single most recent active `memory/{YYYY-MM-DD}/session.md`** referenced in `refs.md` to extract the baseline state, last completed step, and active blockers.
     3. Detect the current ISO date; create and read today's `memory/{YYYY-MM-DD}/session.md` using the Session Template below if absent, and execute the **Automated Memory Pruning & Consolidation Policy** if daily session logs exceed the rolling window.
   * **Phase-Gated On-Demand Lazy Loading:**
     * **Planning & Sub-Task Generation Phase:** Lazy-load **only** the specific functional sections of `memory/project.md` (e.g., via targeted heading/line-range reads) and inspect **only** source files/modules directly relevant to the in-scope task. Never read the entire `memory/project.md` or full codebase during routine tasks.
     * **Pre-Implementation & Execution Phase:** Strictly load `memory/rules.md` and `memory/tools.md` (for root and the active sub-project) **immediately before** starting any actual code generation, script creation, or implementation turn to ingest negative constraints, styling rules, and registered automation tools.
     * **On-Demand Deep Research (`memory/research/`):** Do **not** auto-load at startup. Read `memory/research/libs.md` or `memory/research/{topic}.md` (inspecting the top 15-line `TL;DR` header first) **only** when evaluating dependencies, CVEs, architectural tradeoffs, or domain algorithms. Persist new syntheses to `memory/research/{topic}.md` and package evaluations to `memory/research/libs.md` across the relevant sub-project and root `memory/`.
     * **On-Demand Root Cause Analysis (`memory/rca/{topic}.md`):** Do **not** auto-load at startup. When requested to find a root cause, investigate an anomaly/vulnerability, or debug a hard/extremely hard bug (race conditions, memory leaks, tail-latency spikes, state corruption, non-deterministic failures), check `memory/refs.md` for prior related RCAs (reading the `TL;DR` header first). Write the full forensic investigation to the affected sub-project's `{subproject}/memory/rca/{topic}.md` AND cascade/mirror it to root `memory/rca/{topic}.md` and `refs.md`.
   * **Automated Memory Pruning & Consolidation Policy (10-Session Rolling Window):**
     * **Rolling Window Enforcement:** Maintain strictly the **last 10 individual daily session logs** (`memory/{YYYY-MM-DD}/session.md`) in root and each active sub-project.
     * **Distillation & Rollup Before Purge:** Whenever individual daily session directories exceed 10, take all older daily session logs scheduled for eviction and distill their critical technical outcomes, architectural decisions, resolved blockers, formal invariants, and benchmark baselines into a single condensed chronological rollup file named with an inclusive date range: `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` (using the **Consolidated Rollup Session Template** below).
     * **Disk Purge & Index Pruning (`memory/refs.md`):** After verifying the rollup file is written to disk, permanently delete the individual purged `memory/{YYYY-MM-DD}/` directories from disk to prevent context and repository bloat. Immediately clean and synchronize `memory/refs.md` by removing the file paths of the deleted individual sessions and inserting the consolidated `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` reference into the active tracking manifest.
   * **Missing Memory Initialization:**
     * **Missing `memory/project.md`:** Perform a one-time comprehensive codebase scan to generate it using the **Project Architecture Template** below (covering all 15 sections).
     * **Missing `memory/rules.md`:** Initialize and populate it with code style, coding conventions, negative constraints, quality criteria, and engineering standards.
     * **Missing `memory/tools.md`, `memory/research/`, `memory/rca/`, & Script Directories:** Initialize `memory/tools.md` using the **Tool & Skill Library Template** below. Ensure `memory/script/`, `memory/scratchpad/`, `memory/research/` (with `libs.md`), and `memory/rca/` exist in both root and active sub-projects (`backend/memory/`, `frontend/memory/`), and verify `**/memory/scratchpad/` is listed in `.gitignore`.
   * **Cascading Multi-Repo & Sub-Project Updates (`root`, `backend`, `frontend`):** In multi-repo, monorepo, or nested workspace layouts (e.g., `root/backend/`, `root/frontend/`, or `root/project1/project_frontend/`), when working within specific sub-projects, **synchronize and update the full `memory/` ecosystem across all touched parent and child directories**:
     * **Scoped + Cascaded Artifacts:** If a bug/RCA, deep-research topic, library evaluation, temporary probe, or reusable script belongs to a specific sub-project (e.g., a hard bug in `backend`), write/update the artifact in `backend/memory/` (`backend/memory/rca/{topic}.md`, `backend/memory/research/`, `backend/memory/script/`, `backend/memory/tools.md`, `backend/memory/scratchpad/`) **AND** cascade the update/registration to the parent `root/memory/` (`root/memory/rca/{topic}.md`, `root/memory/refs.md`, `root/memory/tools.md`, `root/memory/{YYYY-MM-DD}/session.md`).
     * **Cross-Boundary Changes:** If a change, bug, or benchmark spans both `frontend` and `backend`, update `root/memory/`, `frontend/memory/`, and `backend/memory/` simultaneously.

3. **Scratchpad vs. Reusable Script Lifecycle (`memory/scratchpad/` & `memory/script/` across Root & Sub-Projects):**
   * **Consult `memory/tools.md` First:** Before writing any ad-hoc command or script, check both root `memory/tools.md` and the active sub-project's `{subproject}/memory/tools.md` to reuse existing automation in `memory/script/`.
   * **`memory/scratchpad/` (Ephemeral Sandbox — Git-Ignored):** Write all temporary scripts (Python, Shell, TypeScript/Bun), one-off data probes, hypothesis tests, bug/anomaly/exploit reproducers, fault-injection harnesses, and draft proofs strictly inside `memory/scratchpad/` (or `{subproject}/memory/scratchpad/`). Ensure `**/memory/scratchpad/` is present in `.gitignore` so temporary artifacts never pollute version control.
   * **`memory/script/` (Persistent Pipelines & Token-Saving Tools):** Store reusable pipelines, benchmark harnesses, validation runners, memory-pruning scripts, CVE/security auditors, regression reproducers, and automation tools in `memory/script/` (or `{subproject}/memory/script/`). Design every script to accept CLI arguments and output compact, token-efficient summaries. Graduate reusable scripts from `scratchpad/` to `script/` and register them in both `{subproject}/memory/tools.md` and root `memory/tools.md`.

4. **Pre-plan alignment gate & Choice Architecture (Observability, Benchmark, Validation):** Before creating any plan or executing tools, files, commands, or code changes, **you must explicitly ask and align with the user every single time without exception** on the three pillars below to ensure absolute correctness, identical definitions, and complete mutual understanding. **Never skip or assume this alignment under any circumstances, even if prior context exists in the prompt or `memory/`.**
   * **Structured Choice Architecture (Active Engineering Guidance):** During this alignment gate, do not ask open-ended or passive questions. Actively guide the user by presenting either:
     1. **Mode A — Prioritized Recommendation (When a clear optimal path exists):** Present the single leanest, highest-leverage engineering path with a concise architectural rationale, explicit invariants, and expected resource profile, and ask the user to confirm or override.
     2. **Mode B — Open Choice Matrix (When genuine architectural or operational trade-offs exist):** Present a structured comparison table contrasting **2–3 functional options** across:
        * **Execution Profile & Complexity:** Algorithmic time/space bounds, I/O concurrency model, and implementation/maintenance surface.
        * **Memory Ceilings (Allocation Footprints):** Steady-state heap/stack usage, peak allocation footprint, buffer/cache bounds, and GC/allocator pressure under normal vs. worst-case loads.
        * **Tail-Latency Distributions (`p95` / `p99` / `p99.9`):** Expected latency profile under **normal payloads** vs. **pathological/worst-case payloads** (e.g., lock contention, cold starts, payload amplification, skew).
        * **Security & Failure Blast Radius:** Trust boundary exposure, failure recovery behavior, and rollback safety.
   * **Three Mandatory Alignment Pillars:**
     * **Observability:** How system state, execution flow, security events, and failures will be observed and inspected across affected sub-projects (`backend`, `frontend`, infrastructure) (e.g., structured logs, metrics, traces, debug outputs, health endpoints, audit trails, or UI/DOM state inspection).
     * **Benchmark (Normal + Non-Normal / Adversarial Cases & Performance Budgets):** How performance, Memory Ceilings, and resilience baselines vs. target thresholds will be measured. **Benchmarks must explicitly cover non-normal conditions, not just average/happy paths:**
       * **Tail Latency:** Measure `p95`, `p99`, and `p99.9` latency distributions alongside `p50` to expose jitter, GC pauses, and queuing stalls.
       * **Anomalies:** Test behavior under unexpected spikes, clock skew, partial network/IO failures, corrupted/malformed payloads, and out-of-order events.
       * **Edge Cases:** Test boundary values (`0`, `1`, `MAX_INT`, empty collections, deep nesting, high-cardinality keys, Unicode/binary extremes).
       * **Worst-Case Complexity, Saturation & Abuse:** Test pathological or adversarial inputs that trigger worst-case algorithmic time/space complexity (e.g., hash collisions, ReDoS regex backtracking, unindexed scans, payload amplification), lock contention, cold starts, and memory/CPU saturation against defined Memory Ceilings.
     * **Validation (Correctness, Security & Maintainability):** The exact acceptance criteria, deterministic commands, formal invariants, security/CVE checks, and pass/fail thresholds required to prove correctness and safety across both normal and non-normal regimes.

5. **Plan, formal reasoning, root cause analysis, and implement:** After aligning on the Choice Architecture and the Observability, Benchmark, and Validation pillars, lazy-load the required sections of `memory/project.md` and record a verification plan with objective, edge cases, security/performance impact, and module impact across root and affected sub-projects. Prioritize high-risk mitigation: identify and resolve the highest-risk unknowns, core logic dependencies, security threat vectors, or architectural uncertainties before working on trivial tasks (consulting or generating `memory/research/{topic}.md` for domain/algorithmic investigation, or `memory/rca/{topic}.md` for root-cause debugging in the relevant sub-project and root `memory/`).
   * **Abstraction, Hypothesis, Lean Proof & Testing Protocol:** When requested by the user, when debugging hard root causes (`memory/rca/{topic}.md`), or when modifying complex algorithms, security/auth boundaries, concurrency, state machines, or core business invariants, construct and verify:
     1. **Abstraction:** Distill the target logic or failure mechanism into a minimal, implementation-agnostic model defining types, state space, trust boundaries, inputs/outputs, and transition rules.
     2. **Hypothesis:** State explicit, falsifiable claims, pre-conditions, post-conditions, failure triggers, Memory Ceilings, time/space complexity bounds, and safety/liveness/security invariants.
     3. **Lean Proof:** Formulate a concise, step-by-step formal logical/mathematical proof (or executable Lean 4 specification/proof in `memory/scratchpad/` or `{subproject}/memory/scratchpad/` when applicable) demonstrating that the invariants hold (or proving why the bug/vulnerability occurred and why the fix eliminates the reachable failure state) across base cases, state transitions, and worst-case boundary conditions.
     4. **Testing:** Translate the abstraction boundaries, hypothesis claims, and proof obligations directly into automated unit, property-based, security/fuzzing, regression, adversarial benchmark, and edge-case tests (executing temporary hypothesis/reproducer harnesses in `scratchpad/` and persistent test/benchmark suites via `script/`).
   * **Pre-Implementation Gate:** Ensure `memory/rules.md` and `memory/tools.md` are loaded before writing or modifying any code. For core-business-logic changes, obtain user confirmation through the Walkthrough Artifact. Implement sequentially; preserve local style; avoid unrequested features, abstractions, refactors, and cleanup. Remove only unused code caused by the change.

6. **Engineering, performance, security, CVE, and maintenance standards:** Adhere primarily to project conventions defined in root and sub-project `memory/rules.md`. If `memory/rules.md` is not provided or lacks specific rules, enforce the following standards:
   * **Clean & Maintainable Architecture:** Keep code simple, modular, strictly typed, and easily readable by humans while ensuring high technical rigor. Reserve entry points for orchestration and isolate business logic. Prevent circular dependencies, keep cyclomatic/cognitive complexity low, and ensure backward compatibility or explicit migration paths for schema/API changes.
   * **Performance Engineering & Memory Ceiling Discipline:** Enforce bounded memory, queues, caches, and payload sizes (zero unbounded growth/OOM risks). Eliminate N+1 queries, blocking I/O on event loops, and redundant allocations/serializations on hot paths. Prefer $O(1)$ or $O(\log n)$ lookups over linear scans in critical loops.
   * **Security & Vulnerability Hardening (Zero-Trust / OWASP / CWE):** Validate and sanitize all external inputs at trust boundaries using strict schemas. Prevent SQL/NoSQL/Command Injection (use parameterized queries/safe APIs), XSS, CSRF, SSRF, Path Traversal, Prototype Pollution, Insecure Deserialization, and ReDoS. Enforce least-privilege RBAC/ABAC checks on every protected route/action. Never hardcode, log, or expose secrets, tokens, or PII in code, terminal output, or memory files.
   * **CVE, Dependency & Supply-Chain Hygiene:** Before installing, upgrading, or replacing any dependency in root, `frontend`, or `backend`, check `memory/research/libs.md` (and `{subproject}/memory/research/libs.md`) first, inspect existing built-in alternatives, verify maintainer reputation, license compatibility, maintenance activity, transitive dependency bloat, and CVE history (`bun audit` / `uv run pip-audit`). Zero tolerance for unmitigated Critical or High CVEs. Record the evaluation in both the sub-project's `memory/research/libs.md` and root `memory/research/libs.md`, pin exact versions, verify lockfile integrity, and use `bun` (FE/Node) or `uv` (Python).
   * **Mandatory Unused Code Deletion Standard (Frontend & Backend):** Zero tolerance for dead or unused code. All unused imports, variables, parameters, functions, dead methods, unreachable branches, and commented-out dead code blocks **MUST have their lines of code permanently deleted** (never commented out, never hidden behind suppressions). Enforce via `bun run clean:unused` on frontend and `uv run ruff check --fix --select F401` on backend. Prefer React TypeScript functional components with hooks, Node.js TypeScript services, and Tailwind; use NaiveUI, then DaisyUI, before Tailwind, and global color styling when required. Meet PEP 8 and ESLint.

7. **Safety and verification:** Practice empirical verification: never assume code works or is secure; every implementation step must be verified by executing the aligned **Observability**, **Benchmark** (including Tail Latency `p95`/`p99`/`p99.9`, Memory Ceilings, Anomalies, Edge Cases, and Worst Cases), and **Validation** checks via actual terminal commands, compile checks, linting, security/CVE audits, and passing unit/property tests across all touched sub-projects. Practice rigorous edge-case and adversarial testing: before advancing to the next workflow step, explicitly ask "What anomaly, tail-latency spike, memory-ceiling breach, security exploit, edge case, or worst-case input could prove this Hypothesis or Lean Proof wrong?" and actively test it in `memory/scratchpad/` (or `{subproject}/memory/scratchpad/`). For root-cause or vulnerability fixes (`memory/rca/{topic}.md`), verify that the deterministic reproducer fails before the fix and passes after the fix, and ensure the RCA is recorded in both the affected sub-project (`backend/memory/rca/{topic}.md` or `frontend/memory/rca/{topic}.md`) and root `memory/rca/{topic}.md`. Never force-delete, wipe databases, or clean Git without explicit instruction. Check ports and prevent orphaned servers. For UI changes, inspect the page and capture a screenshot. Document failures, fix them, and re-run checks. For major changes, provide a Walkthrough Artifact with modified files, compile output, security/CVE status, normal vs. worst-case benchmark comparisons, and test results.

---

### Pre-Plan Choice Architecture Template (Used in Section 4 Alignment Gate)
*Present either Mode A (Prioritized Recommendation) or Mode B (Open Choice Matrix) alongside the Observability, Benchmark, and Validation alignment questions:*

```markdown
### Architectural & Execution Alignment
* **Selected Guidance Mode:** {Mode A: Prioritized Recommendation | Mode B: Open Choice Matrix}
* **Prioritized Recommendation:** {Option Name} — {Concise rationale explaining why this is the leanest, highest-leverage engineering path}

| Option | Execution Profile & Complexity | Memory Ceiling (Normal vs. Pathological) | Tail Latency `p95` / `p99` / `p99.9` (Normal vs. Worst-Case) | Key Trade-Off / Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| **Option 1 (Recommended)** | `{e.g., O(1) ring buffer, non-blocking}` | `{Bounded: <= 16MB fixed}` | `{Normal: 2/4/7ms | Worst: 5/9/14ms}` | `{Fixed capacity; drops oldest on overflow}` |
| **Option 2** | `{e.g., Dynamic heap queue}` | `{Unbounded peak: ~250MB+ under spike}` | `{Normal: 2/5/9ms | Worst: 45/180/600ms (GC stall)}` | `{Risk of OOM / tail-latency amplification}` |
```

---

### Root Cause Analysis (RCA) & Vulnerability Forensics Template (`memory/rca/{topic}.md` & `{subproject}/memory/rca/{topic}.md`)
*Read and write on-demand when requested to find a root cause, investigate a security vulnerability/CVE, or debug hard/extremely hard issues (do not auto-load at session start). Write to the affected sub-project (`backend/memory/rca/{topic}.md` or `frontend/memory/rca/{topic}.md`) AND cascade/sync to root `memory/rca/{topic}.md`. Keep the `TL;DR` Forensic Header in the first 15 lines for low-token inspection:*

```markdown
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

## 4. Formal Mechanism & Broken Invariant (Abstraction & Lean Proof)
* Step-by-step state transition trace showing how the system enters the illegal/vulnerable state, the exact invariant violated, and the formal/logical proof that the new constraint prevents re-entry across all edge and worst cases.

## 5. Remediation, Regression Tests & Blast-Radius Check
* Modified `{subproject}/file:line` locations, regression/security test commands added to the suite, before/after normal & worst-case benchmark results, sibling modules audited across `backend`/`frontend`, and synced RCA paths (`root/memory/rca/{topic}.md` ↔ `{subproject}/memory/rca/{topic}.md`).
```

---

### Deep Research Templates (`memory/research/{topic}.md` & `memory/research/libs.md` — Root & Sub-Project Scoped)
*Read on-demand only (do not auto-load at session start). Write sub-project-specific research/libraries to `{subproject}/memory/research/` and cascade/sync to root `memory/research/`. Always place the `TL;DR` Decision Header in the first 15 lines so agents can inspect conclusions with minimal token usage:*

#### 1. Topic Deep-Research Template (`memory/research/{topic}.md` & `{subproject}/memory/research/{topic}.md`)
```markdown
# Deep Research: {Topic Name}
* **Date:** {YYYY-MM-DD} | **Scope:** {Root / Backend / Frontend / Shared} | **Status:** {Verified / Draft / Superseded}
* **TL;DR Conclusion:** {1–3 sentences stating the exact technical decision, chosen algorithm/architecture, and key constraint}
* **Adopted Pattern / Invariant:** {Exact formula, protocol, memory ceiling, security boundary, or architectural rule to apply}

---
## 1. Problem Context & Scope
* Why this research was triggered and which root/sub-project components (`backend`, `frontend`) it affects.

## 2. Comparative Analysis, Memory Ceilings & Tail-Latency Tradeoffs
* Options evaluated, time/space complexity, allocation footprints, tail-latency (`p95`/`p99`/`p99.9`) behavior under normal and pathological loads, operational maintenance burden, and failure modes.

## 3. Security, Vulnerability Surface & Worst-Case Bounds
* Mathematical/logical bounds, threat vectors (OWASP/CWE), pathological inputs, and concurrency/memory hazards.

## 4. Implementation Blueprint & References
* Concrete integration steps, code patterns, synced research paths, and authoritative source links/benchmarks.
```

#### 2. Library, CVE & Dependency Research Registry (`memory/research/libs.md` & `{subproject}/memory/research/libs.md`)
```markdown
# Library, CVE & Dependency Research Registry (`memory/research/libs.md`)

> **On-Demand Lookup Policy:** Consult this file (and `{subproject}/memory/research/libs.md`) before adding, upgrading, auditing, or replacing any dependency. Read only the summary table or relevant package section to save tokens.

## Evaluated Libraries Index

| Package / Library | Scope (`FE`/`BE`/`Root`) | Domain / Purpose | Pinned Version | Decision (`Adopted` / `Rejected` / `Deprecated`) | CVE & Maintenance Status | Memory Ceiling & Tail-Latency (`p95`/`p99`/`p99.9`) Notes | Alternatives Considered |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `{pkg-name}` | `{BE / FE}` | `{e.g., Schema Validation}` | `{x.y.z}` | `Adopted` | `0 CVEs / Active` | `{Low p99 overhead, zero-alloc hot path}` | `{Alt1, Alt2}` |

## Detailed Package, Security & Maintenance Evaluations
### `{pkg-name}` (`{x.y.z}`) — {Scope: Backend / Frontend / Root} — {Adopted / Rejected / Deprecated}
* **Security, Vulnerability & CVE Audit:** {CVE history, CWE exposure, transitive dependency risk, audit command result, license compliance}
* **Maintenance & Longevity:** {Maintainer health, release cadence, breaking-change frequency, deprecation risk, upgrade path}
* **Benchmark, Memory Ceiling & Worst-Case Profile:** {Peak memory footprint, cold-start cost, bundle size, p95/p99/p99.9 latency under pathological/adversarial payloads}
* **Integration Constraints & Gotchas:** {Edge cases, known bugs, required security flags, or configuration rules}
```

---

### Tool & Skill Library Template (`memory/tools.md` & `{subproject}/memory/tools.md`)
*Lazy-load immediately before implementation or tool execution. Initialize when `memory/tools.md` is absent in root or a sub-project (`backend/memory/tools.md`, `frontend/memory/tools.md`), and update both the sub-project and root registry whenever a script is added or updated:*

```markdown
# Tool & Skill Library Registry (`memory/tools.md`)

> **Token Optimization Policy:** Always inspect this registry (and sub-project `{subproject}/memory/tools.md`) before writing ad-hoc commands or new scripts.
> * **Persistent Automation (`memory/script/` & `{subproject}/memory/script/`):** Version-controlled, reusable pipelines, benchmark runners, memory-pruning tools, security/CVE auditors, and validators that emit compact, token-efficient outputs.
> * **Ephemeral Sandbox (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`):** Git-ignored directory (`**/memory/scratchpad/`) for temporary hypothesis testing, anomaly/exploit reproducers, and one-off scripts. Graduate reusable scripts from `scratchpad/` to `script/` and register them below.

## Registered Scripts & Skills (`memory/script/` & `{subproject}/memory/script/`)

| Tool / Skill ID | Scope (`Root`/`BE`/`FE`) | Script Path | Purpose & When to Use | Exact Invocation Command | Output Format (Compact) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `clean-unused` | `Root/FE/BE` | `memory/script/clean_unused.sh` | Strip dead imports/code across FE & BE | `bash memory/script/clean_unused.sh` | Exit code + modified file count |
| `bench-tail` | `BE/FE` | `{subproject}/memory/script/bench_tail.py` | Run p50/p95/p99/p99.9, memory-ceiling, anomaly & worst-case benchmarks | `uv run python {subproject}/memory/script/bench_tail.py --target <mod>` | JSON summary (`p50`, `p95`, `p99`, `p99.9`, `max`, `mem_peak`) |
| `sec-audit` | `Root/FE/BE` | `memory/script/sec_audit.sh` | Run CVE dependency audit (`bun audit` / `pip-audit`) & secret/CWE checks | `bash memory/script/sec_audit.sh` | JSON summary (`cve_count`, `severity`, `pkg`, `file:line`) |
| `prune-memory` | `Root/FE/BE` | `memory/script/prune_memory.py` | Enforce 10-session rolling window, generate date-range rollup & prune `refs.md` | `uv run python memory/script/prune_memory.py` | JSON summary (`rolled_up_range`, `purged_count`, `active_count`) |
| `validate-all` | `Root/FE/BE` | `memory/script/validate.sh` | Execute typecheck, lint, unit, and property tests concisely | `bash memory/script/validate.sh` | Pass/Fail summary + failing `file:line` only |

## Active Scratchpad Experiments (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`)
* **Git Status:** Must remain ignored in `.gitignore` (`**/memory/scratchpad/`).
* **Current Probes:** {List active temporary hypothesis/proof/benchmark/RCA reproducer scripts across root/BE/FE or `None`}
```

---

### Project Architecture Template (`memory/project.md` & `{subproject}/memory/project.md`)
*Do NOT load in full at session initialization. Lazy-load specific sections on-demand during the planning phase. Generate when `memory/project.md` is absent in root or a sub-project by performing a one-time architectural codebase scan:*

```markdown
# Project Architectural Blueprint: {Project / Sub-Project Name}

## 1. Project Overview & Business Domain
* Core mission, problem solved, user domain, key stakeholders, and high-level boundaries (root vs. `backend` / `frontend` scope).

## 2. Tech Architecture, Runtime Stack & Dependency Hygiene
* Language versions, primary frameworks, package managers (`bun`/`uv`), engines, and pinned dependencies (cross-referenced with `memory/research/libs.md` and `{subproject}/memory/research/libs.md` for CVE and maintenance status).

## 3. Directory Layout & Module Ownership
* Structural directory tree highlighting functional module boundaries, orchestration entry points, and root + sub-project (`backend/`, `frontend/`) `memory/tools.md`, `memory/script/`, `memory/scratchpad/`, `memory/research/`, and `memory/rca/`.

## 4. Key Data Models & Schema Mappings
* Database tables, relations, indexes, entity lifecycles, and ORM schema mappings (e.g., Prisma, Drizzle).

## 5. System Features, Core Mechanics & Performance Budgets
* Critical business workflows, background jobs, bounded caching strategies, state machines, Memory Ceilings, and hot-path latency budgets.

## 6. Authentication, Authorization, Security & Vulnerability Posture
* Auth providers, JWT/session lifecycles, RBAC/ABAC matrices, input validation boundaries, OWASP/CWE mitigations, CVE audit policies, and secrets management.

## 7. REST API Endpoints Reference
* Route paths, HTTP methods, request payload schemas, rate limits, auth requirements, and status responses.

## 8. WebSocket & Asynchronous Event Protocol Spec
* Real-time events, subscription channels, event schemas, backpressure/payload limits, message brokers, and reconnection rules.

## 9. Third-Party Integrations & External Services
* External APIs, payment gateways, webhooks, signature verification, notification services, and external dependencies.

## 10. Restricted & Auto-Generated Files (Do Not Edit)
* Code artifacts that must not be modified directly (e.g., generated types, migrations, build outputs).

## 11. Architectural Invariants & ADRs (Key Decisions)
* Critical decisions made, non-negotiable boundaries, formal invariants, and links to deep-dive files in `memory/research/{topic}.md` and `memory/rca/{topic}.md` (across root and sub-projects).

## 12. Observability, Benchmark, Validation & Security Testing Strategy
* **Observability:** Logging, metrics, tracing, security audit trails, and runtime state inspection mechanisms.
* **Benchmark (Normal & Adversarial):** Baseline vs. target SLAs covering `p50`/`p95`/`p99`/`p99.9` tail latency, Memory Ceilings, anomaly injection, boundary edge cases, and worst-case/DoS pathological inputs.
* **Validation, Security & Formal Verification:** Unit, property-based, integration, E2E, and security/CVE audit commands, Abstraction/Hypothesis/Lean Proof artifacts, test database isolation, and mock fixture setup.

## 13. Running Local Infrastructure
* Port mappings, database containers, environment variable setup, and seeding commands.

## 14. Containerized & Production Cloud Deployments
* Dockerfile specifications (non-root, minimal base images), Cloud Run / Kubernetes manifests, resource limits, environment flags, and CI/CD pipelines.

## 15. Known Technical Debt, Maintenance Risks & Fragile Areas
* Known bottlenecks, tail-latency risks, deprecated dependencies, security/CVE watch items, legacy code sections, concurrency hazards, and links to historical root-cause analyses in `memory/rca/{topic}.md` and `{subproject}/memory/rca/{topic}.md`.
```

---

### Session & Consolidation Templates (`memory/{YYYY-MM-DD}/session.md`, `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` & `memory/refs.md`)

#### 1. Active Daily Session Log Template (`memory/{YYYY-MM-DD}/session.md` & `{subproject}/memory/{YYYY-MM-DD}/session.md`)
*Only the single most recent active session log is loaded at Turn 1. Maximum 10 individual daily logs retained on disk at any time:*

```markdown
# Session Log: {YYYY-MM-DD} ({Root / Sub-Project Scope})

### Previous Session Tracking
* **Last Session Date:** {YYYY-MM-DD or None}
* **Final Status:** {Summary of ending state from previous session}
* **Key Achievements:** {List of verified accomplishments}
* **Leftover Blockers:** {Unresolved issues carried forward}

### Choice Architecture & Alignment Contract
* **Selected Option & Rationale:** {Chosen architecture/execution option from Prioritized Recommendation or Open Choice Matrix}
* **Observability Criteria:** {Aligned logs, traces, metrics, security audit outputs, or state checks across root/BE/FE}
* **Benchmark Targets (Normal, Non-Normal, Tail-Latency & Memory Ceilings):** {Aligned baselines & targets for p50/p95/p99/p99.9 Tail Latency, Memory Ceilings, Anomalies, Edge Cases, and Worst-Case/Adversarial inputs}
* **Validation, Security & Maintenance Criteria:** {Aligned acceptance checks, formal invariants, CVE/security checks, and pass/fail commands}
* **Formal Reasoning (If Applicable):** {Abstraction, Hypothesis, Lean Proof, and Test mapping summary}
* **Tools, Scratchpad, Research & RCA Used (Root & Sub-Projects):** {Scripts in `memory/script/`, probes in `memory/scratchpad/`, research/CVE audits in `memory/research/`, or RCAs in `memory/rca/` across root, `backend/`, and `frontend/`}

### Current Session Tracking
* **Active Task:** {Current in-scope objective}
* **Touched Scopes (`Root` / `Backend` / `Frontend`):** {List all project and sub-project `memory/` directories synchronized in this session}
* **Last Completed Step:** {Most recent verified command, tool, or edit}
* **Next Action:** {Immediate next programmatic step or tool call}
* **Summary of Activity:** {Concise description of changes made in this session}
* **Progress / Changes:** {Specific files, modules, and tests modified}
* **Blockers / Unresolved Items:** {Current blockers, unknowns, or none}
```

#### 2. Consolidated Rollup Session Template (`memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md`)
*Generated automatically when pruning individual daily session logs older than the 10-session rolling window:*

```markdown
# Consolidated Session Rollup: {START_YYYY-MM-DD} to {END_YYYY-MM-DD} ({Root / Sub-Project Scope})
* **Purged Daily Sessions Count:** {N sessions consolidated and removed from disk}
* **TL;DR Era Summary:** {2–3 sentences summarizing major milestones, architectural shifts, and stability/performance posture across this date range}

## 1. Key Architectural & Feature Outcomes
* Chronological bullet list of permanent features, schema migrations, and module changes delivered (`file:line` references).

## 2. Established Invariants, Benchmarks & Memory Ceilings
* Verified `p50`/`p95`/`p99`/`p99.9` baselines, enforced Memory Ceilings, and formal proofs established during this window.

## 3. Linked Deep Research & Root Cause Analyses (Preserved On-Demand)
* Pointers to permanent `memory/research/{topic}.md`, `memory/research/libs.md`, and `memory/rca/{topic}.md` artifacts created in this period.

## 4. Carried-Forward Tech Debt & Historical Blockers
* Any long-term caveats or deferred items transferred into the active rolling window.
```

#### 3. Active Reference Manifest Template (`memory/refs.md` & `{subproject}/memory/refs.md`)
*Loaded at Turn 1. Automatically pruned whenever daily sessions are consolidated into a date-range rollup:*

```markdown
# Memory Reference Manifest (`memory/refs.md`)

## 1. Latest Active Session (Load at Turn 1)
* **Current / Most Recent Session:** `memory/{YYYY-MM-DD}/session.md` — {Active task & blocker summary}

## 2. Rolling 10-Session Window (Max 10 Individual Logs)
1. `memory/{YYYY-MM-DD}/session.md` — {1-line outcome summary}
*(Keep strictly <= 10 entries; consolidate older entries into Section 3 and delete their individual folders from disk)*

## 3. Consolidated Chronological Rollups (Archived Windows)
* `memory/{START_YYYY-MM-DD}-{END_YYYY-MM-DD}/session.md` — {1-line distilled era summary}

## 4. On-Demand Deep Research & RCA Index (Lazy-Load Only When Relevant)
* **Libraries & CVE Registry:** `memory/research/libs.md`
* **Research Topics:** `memory/research/{topic}.md` — {1-line TL;DR}
* **Root Cause Analyses:** `memory/rca/{topic}.md` — {1-line TL;DR root cause & fix}
```
