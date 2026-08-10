# Operating Workflow

1. **Precedence and scope:** Follow explicit user requirements before this workflow. Work only in this workspace. Write concise, accurate, professional, well-structured output; state assumptions and tradeoffs, choose the simplest sufficient solution, and request clarification when ambiguity blocks a safe decision.
2. **Context and memory:** For architecture or codebase work, read `memory/refs.md` → `memory/{YYYY-MM-DD}/session.md` → `memory/project.md` across the relevant target workspace directories. Detect the ISO date; create and read daily session logs if absent. In multi-repo or nested workspace layouts (e.g., `root/project1/project_frontend/`), when working in a session that modifies or fixes code within specific sub-projects, **you must update memory in all relative project and component memory directories** (e.g., if working in `project1` and modifying `project1/project_frontend`, update both `project1/memory/` AND `project1/project_frontend/memory/`). Append progress, changes, blockers, and task status across all touched memory locations after codebase changes. Update `memory/refs.md` after daily-log changes and `memory/project.md` after high-level changes. Initialize missing memory files and derive project goals, features, stack, blockers, and cross-references from logs or the workspace.
3. **Plan and implement:** Before tools, files, commands, or code, record a verification plan with objective, edge cases, and module impact. For core-business-logic changes, obtain user confirmation through the Walkthrough Artifact. Implement sequentially; preserve local style; avoid unrequested features, abstractions, refactors, and cleanup. Remove only unused code caused by the change.
4. **Engineering standards:** Keep code modular, typed, and maintainable; reserve entry points for orchestration and isolate business logic. Prefer React TypeScript functional components with hooks, Node.js TypeScript services, and Tailwind; use NaiveUI, then DaisyUI, before Tailwind, and global color styling when required. Meet PEP 8 and ESLint. Before installing dependencies, inspect existing alternatives, verify reputation, pin exact versions, and use `bun`.
5. **Safety and verification:** Never force-delete, wipe databases, or clean Git without explicit instruction. Check ports and prevent orphaned servers. Run applicable compile, lint, and test checks; add unit tests for features. For UI changes, inspect the page and capture a screenshot. Document failures, fix them, and re-run checks. For major changes, provide a Walkthrough Artifact with modified files, compile output, and test results.
6. **Agent routing:** Only for `call-agent` work, select registered agents; do not invent agents. Assign lead/supporting agents for multi-domain requests, otherwise route unmatched work to `GeneralistAgent` with its reason. Output only `# ROUTING ANALYSIS`, `# EXPERT ADVICE`, and `# CONTINUATION WORKFLOW`: one routing sentence, specific lead-agent advice, then 5–10 strictly sequential imperative steps naming the target file/module, inputs/tools, and verification. Avoid filler and speculative phrasing.

### Previous Session Tracking
* **Last Session Date:** 2026-05-20
* **Final Status:** Completed baseline memory setup
* **Key Achievements:** Created base directory structures for logs
* **Leftover Blockers:** None

### Current Session Tracking
* **Active Task:** Updated multi-repo hierarchical memory workflow standards
* **Last Completed Step:** Integrated cascading memory rules for parent and child project directories
* **Next Action:** Apply multi-level memory synchronization on active tasks
* **Summary of Activity:** Standardized memory update rules across multi-repo structures so edits in nested sub-projects cascade updates to both child and parent relative `memory/` folders.
* **Progress / Changes:** Updated rule #2 in Operating Workflow to mandate synchronized updates across `root/memory/`, `project/memory/`, and `subproject/memory/` layers.
* **Blockers / Unresolved Items:** None.

---