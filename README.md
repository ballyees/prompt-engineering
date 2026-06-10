# prompt-engineering

A collection of **prompt-engineering agents** built on the [Google Agent Development Kit (ADK)](https://adk.dev). Each agent ingests a raw, low-detail user request and refines it into a robust, production-grade prompt or skill specification using a structured framework (PERSONA / GOAL / TASK / EXPECTATION / TESTING).

## Repository layout

```
agents/                     # System instructions (source of truth) for every agent
adk-prompt-engineer/        # ADK agent project — emits ADK LlmAgent declarations
refiner-user-query-v1/      # ADK agent project — refines prompts (v1)
refiner-user-query-v2/      # ADK agent project — refines prompts (v2, 600–700 word spec)
skill-prompt-engineer/      # ADK agent project — emits agentskills.io SKILL.md files
agent-cli-cmd.sh            # Reference command for scaffolding new agents
```

### `agents/` — system instruction library

The `agents/` folder holds the raw **system instructions** that define each agent's behaviour. These are the human-authored source of truth that is embedded into the `static_instruction` of the corresponding ADK agent.

| File | Agent | Output it produces |
| --- | --- | --- |
| [agents/adk-prompt-engineer.md](agents/adk-prompt-engineer.md) | ADK Prompt Engineer | A standardized Google ADK `LlmAgent` Python declaration with dynamically configured `planner`, `code_executor`, `generate_content_config`, `tools`, and `output_key`. |
| [agents/refiner-user-query-v1.md](agents/refiner-user-query-v1.md) | Refiner User Query v1 | A structured prompt with `GOAL`, `TASK`, `EXPECTATION`, and `TESTING` sections (concise). |
| [agents/refiner-user-query-v2.md](agents/refiner-user-query-v2.md) | Refiner User Query v2 | A 600–700 word, highly detailed structured prompt with the same four sections plus an "All-rounder" escape mode. |
| [agents/skill-prompt-engineer.md](agents/skill-prompt-engineer.md) | Skill Prompt Engineer | A spec-compliant `SKILL.md` file (YAML frontmatter + workflow) conforming to the `agentskills.io` specification. |

### `*/app/agent.py` — ADK agent definitions

Each top-level project folder is a self-contained ADK application generated via the `agents-cli` scaffold. The agent itself is defined in `app/agent.py`, where the system instruction from `agents/` is wired into a `google-adk` `LlmAgent` along with its model, tools, and runtime configuration.

For example, [refiner-user-query-v1/app/agent.py](refiner-user-query-v1/app/agent.py) defines:

```python
refiner_agent = LLMAgent(
    name="RefinerUserQuery",
    model="gemini-3.5-flash",
    description="...",
    static_instruction="""...""",          # mirrors agents/refiner-user-query-v1.md
    generate_content_config=...,            # thinking config + max tokens
    planner=BuiltInPlanner(...),
    tools=[google_search, url_context],
    output_key="refined_prompt",
)

root_agent = refiner_agent
app = App(root_agent=root_agent, name="app")
```

Common building blocks across the agents:

- **Model**: `gemini-3.5-flash` on Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=True`).
- **Tools**: `google_search` and `url_context` for live grounding; `adk-prompt-engineer` additionally mounts an MCP toolset (`mcpdoc`) for ADK documentation.
- **Reasoning**: `BuiltInPlanner` and `ThinkingConfig` for multi-step planning where required.
- **Output**: a domain-specific `output_key` (e.g. `refined_prompt`).

## Project structure (per agent)

Every agent project follows the standard `agents-cli` / ADK layout:

```
<agent>/
  agents-cli-manifest.yaml   # Scaffold metadata (template, region, language)
  Dockerfile                 # Container build
  GEMINI.md                  # Agent guidance file
  pyproject.toml             # Python deps (google-adk, telemetry, eval, lint)
  app/
    agent.py                 # The ADK agent definition
    fast_api_app.py          # FastAPI server entrypoint
    app_utils/               # telemetry + typing helpers
  tests/
    eval/                    # Eval config + datasets
    integration/             # Agent + server end-to-end tests
    unit/                    # Unit tests
```

## Getting started

Requirements: Python `>=3.11,<3.14`, `google-adk >=1.15`, and Google Cloud credentials (Vertex AI access).

```bash
# Pick an agent and install its dependencies
cd refiner-user-query-v1
pip install -e .

# Run the ADK dev UI / server
adk web                 # interactive UI
# or
adk run app             # CLI run
```

Authenticate against Google Cloud before running so the agents can resolve the active project:

```bash
gcloud auth application-default login
```

## Scaffolding a new agent

New agent projects are created with the Agents CLI (see [agent-cli-cmd.sh](agent-cli-cmd.sh)):

```bash
agents-cli create <agent-name> --prototype --yes
```

After scaffolding, author the system instruction in `agents/<agent-name>.md` and embed it into `<agent-name>/app/agent.py`.
