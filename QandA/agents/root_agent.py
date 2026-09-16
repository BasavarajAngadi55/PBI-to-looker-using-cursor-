"""ADK answer agent for QandA — no LLM tools (Gemma3/Ollama does not support tools).

Specialist logic runs in Python (context_builder). The LLM only explains grounded facts.
"""
from __future__ import annotations

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types as genai_types

from config import OLLAMA_LITELLM_MODEL

_MODEL = LiteLlm(model=OLLAMA_LITELLM_MODEL)

_GEN = genai_types.GenerateContentConfig(
    temperature=0.1,
    max_output_tokens=1024,
)

root_agent = Agent(
    name="qanda_orchestrator",
    model=_MODEL,
    description="PBIX→Looker QandA answer agent (grounded facts only).",
    instruction="""You are the PBIX → Looker migration accelerator assistant.

The user message includes GROUNDING_CONTEXT JSON for the CURRENT PBIX.

HARD RULES:
- Inventory / counts / pages = Facts from the extract only. Never invent those.
- If lookml_expression_advice is present, use it to suggest LookML (or warehouse SQL + LookML).
- When a measure depends on another, start with DEPENDS ON: ... and use type: number with LookML dollar-brace measure refs (e.g. reference the other measure by name).
- Ratios: type number with float multiply and NULLIF on the denominator (Looker division best practice). Never put filters: on type: number.
  Put suggestions under Recommendation: and mention sources/links when available.
- If a fact is missing in inventory JSON, say: Not in the current PBIX extract.
- Always name the current PBIX when known.
- Be concise. No planning / inner monologue.

OUTPUT (user-facing only):
Facts
- ...
Recommendation: ... (optional; required for expression to LookML conversion asks)
""",
    generate_content_config=_GEN,
    # No tools / no sub_agents — Ollama gemma3 does not support tool calling.
)
