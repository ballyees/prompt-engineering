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
