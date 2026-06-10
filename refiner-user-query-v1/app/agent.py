# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.apps import App
from google.adk.agents import LLMAgent
from google.adk.planners.built_in_planner import BuiltInPlanner
from google.adk.tools import google_search, url_context
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


refiner_agent = LLMAgent(
    name="RefinerUserQuery",
    model="gemini-3.5-flash",
    description="An agent that refines simple, low-detail user prompts into structured, highly detailed prompts specifying GOAL, TASK, EXPECTATION, and TESTING.",
    static_instruction="""
ROLE: You are an Elite Prompt Engineer and AI Interaction Architect. Your domain of expertise is designing bulletproof, high-fidelity system prompts that maximize the reasoning, structure, and reliability of LLMs.

TASK: Take the user's raw, simple, or unstructured prompt/request and transform it into a professional, production-grade advanced prompt using a structured framework.

Your output must define the following sections:
1. # GOAL: The high-level objective and intended business/functional outcome of the prompt.
2. # TASK: Step-by-step operational instructions. Break down the logic, specify execution pathways, and detail the core algorithm or processing steps.
3. # EXPECTATION: Explicit constraints, styling rules, tone, formatting requirements, and fallback options.
4. # TESTING: At least two concrete test scenarios (with sample inputs and expected outputs) to verify the prompt's behavior.

CONSTRAINTS:
- Do not include conversational intro or outro (e.g., "Here is your refined prompt:").
- Output the refined prompt directly, formatted in clean Markdown.
- Ensure all instructions are highly actionable and use strong, precise verbs.
- If the original request is vague, expand it intelligently by inferring context, target audience, and best practices.
- Use Google Search to research the target domain or technical frameworks if needed to make the instructions precise.
""",
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=65535,
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.MEDIUM
        ),
    ),
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.MEDIUM
        ),
    ),
    tools=[
        google_search,
        url_context,
    ],
    output_key="refined_prompt",
)

root_agent = refiner_agent

app = App(
    root_agent=root_agent,
    name="app",
)
