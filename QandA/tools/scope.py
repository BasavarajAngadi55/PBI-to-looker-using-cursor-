"""Greeting + in-scope detection for QandA (no LLM needed)."""
from __future__ import annotations

import re

GREETING_RE = re.compile(
    r"^\s*(hi|hello|hey|hiya|good\s*(morning|afternoon|evening)|howdy|hola)\b[\s!.?]*$",
    re.I,
)

# Strong domain terms — question must include at least one (unless greeting/help)
DOMAIN_HINTS = (
    "pbix",
    "power bi",
    "powerbi",
    "looker",
    "lookml",
    "table",
    "tables",
    "column",
    "measure",
    "dax",
    "expression",
    "convert",
    "translate",
    "rewrite",
    "equivalent",
    "relationship",
    "dashboard",
    "visual",
    "page",
    "slicer",
    "coverage",
    "validation",
    "migration",
    "inventory",
    "extract",
    "view",
    "explore",
    "connection",
    "placeholder",
    "todo",
    "gap",
    "warehouse",
    "kpi",
    "report",
    "mapping",
    "semantic",
    "model",
    "join",
    "phase 1",
    "phase 2",
    "phase 3",
    "scorecard",
    "percent",
    "completion",
    "calculate",
    "sumx",
    "averagex",
    "distinctcount",
)

HELP_RE = re.compile(
    r"^\s*(help|help me|what can you do|what do you do|options|menu)\??\s*$",
    re.I,
)

OUT_OF_SCOPE_REPLY = (
    "That question is **out of scope** for this assistant.\n\n"
    "I only help with **Power BI → Looker migration** for the **current PBIX**:\n"
    "- Extracted model (tables, measures, relationships, Power Query)\n"
    "- LookML semantic model & placeholders you must fill\n"
    "- Report pages → Looker dashboards & coverage\n"
    "- Migration scorecard (% done / left)\n\n"
    "Please ask something about this PBIX migration."
)

GREETING_REPLY = (
    "Hi — I’m your **PBIX → Looker migration accelerator**.\n\n"
    "I can help you with the **current PBIX** only:\n"
    "1. **Extract Power BI model** — tables, measures, relationships\n"
    "2. **Build Looker semantic model (LookML)** — views, TODOs, placeholders\n"
    "3. **Convert report pages → Looker dashboards** — coverage & gaps\n"
    "4. **Migration scorecard** — % done / left and what you must edit\n\n"
    "How can I help you?"
)


def is_greeting(text: str) -> bool:
    return bool(GREETING_RE.match((text or "").strip()))


def is_help(text: str) -> bool:
    return bool(HELP_RE.match((text or "").strip()))


def is_in_scope(text: str) -> bool:
    """True for greetings, help, conversion asks, or migration/PBIX/Looker topics."""
    q = (text or "").strip().lower()
    if not q:
        return False
    if is_greeting(q) or is_help(q):
        return True
    try:
        from tools.lookml_web_advice import is_expression_conversion_request

        if is_expression_conversion_request(text):
            return True
    except Exception:
        pass
    return any(h in q for h in DOMAIN_HINTS)
