# Tool & Skill Library Registry (`memory/tools.md`)

> **Token Optimization Policy:** Always inspect this registry (and sub-project `{subproject}/memory/tools.md`) before writing ad-hoc commands or new scripts.
> * **Persistent Automation (`memory/script/` & `{subproject}/memory/script/`):** Version-controlled, reusable pipelines, benchmark runners, memory-pruning tools, template sync utilities, security/CVE auditors, and validators that emit compact, token-efficient outputs.
> * **Ephemeral Sandbox (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`):** Git-ignored directory (`**/memory/scratchpad/`) for temporary hypothesis testing, anomaly/exploit reproducers, and one-off scripts. Graduate reusable scripts from `scratchpad/` to `script/` and register them below.

## Registered Scripts & Skills (`memory/script/` & `{subproject}/memory/script/`)

| Tool / Skill ID | Scope (`Root`/`BE`/`FE`) | Script Path | Purpose & When to Use | Exact Invocation Command | Output Format (Compact) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sync-templates` | `Root` | `memory/script/sync_templates.sh` | Fetch missing or user-requested updated templates into `memory/templates/*.md` | `bash memory/script/sync_templates.sh [template-name\|--all]` | JSON summary (`updated`, `skipped`, `status`) |
| `clean-unused` | `Root/FE/BE` | `memory/script/clean_unused.sh` | Strip dead imports/code across FE & BE | `bash memory/script/clean_unused.sh` | Exit code + modified file count |
| `bench-tail` | `BE/FE` | `{subproject}/memory/script/bench_tail.py` | Run p50/p95/p99/p99.9, memory-ceiling, anomaly & worst-case benchmarks | `uv run python {subproject}/memory/script/bench_tail.py --target <mod>` | JSON summary (`p50`, `p95`, `p99`, `p99.9`, `max`, `mem_peak`) |
| `sec-audit` | `Root/FE/BE` | `memory/script/sec_audit.sh` | Run CVE dependency audit (`bun audit` / `pip-audit`) & secret/CWE checks | `bash memory/script/sec_audit.sh` | JSON summary (`cve_count`, `severity`, `pkg`, `file:line`) |
| `prune-memory` | `Root/FE/BE` | `memory/script/prune_memory.py` | On explicit user request, enforce 10-session rolling window, generate date-range rollup & prune `refs.md` | `uv run python memory/script/prune_memory.py` | JSON summary (`rolled_up_range`, `purged_count`, `active_count`) |
| `validate-all` | `Root/FE/BE` | `memory/script/validate.sh` | Execute typecheck, lint, unit, and property tests concisely | `bash memory/script/validate.sh` | Pass/Fail summary + failing `file:line` only |

## Active Scratchpad Experiments (`memory/scratchpad/` & `{subproject}/memory/scratchpad/`)
* **Git Status:** Must remain ignored in `.gitignore` (`**/memory/scratchpad/`).
* **Current Probes:** {List active temporary hypothesis/proof/benchmark/RCA reproducer scripts across root/BE/FE or `None`}
