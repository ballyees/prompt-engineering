# Project Architectural Blueprint: {Project / Sub-Project Name}

## 1. Project Overview & Business Domain
* Core mission, problem solved, user domain, key stakeholders, and high-level boundaries (root vs. `backend` / `frontend` scope).

## 2. Tech Architecture, Runtime Stack & Dependency Hygiene
* Language versions, primary frameworks, package managers (`bun`/`uv`), engines, and pinned dependencies (cross-referenced with `memory/research/libs.md` and `{subproject}/memory/research/libs.md` for CVE and maintenance status).

## 3. Directory Layout & Module Ownership
* Structural directory tree highlighting functional module boundaries, orchestration entry points, root `memory/templates/`, and root + sub-project (`backend/`, `frontend/`) `memory/tools.md`, `memory/script/`, `memory/scratchpad/`, `memory/research/`, and `memory/rca/`.

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
