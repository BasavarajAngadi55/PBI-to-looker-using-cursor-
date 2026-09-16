"""Deterministic context pack — Python specialists enrich facts (no LLM tools)."""
from __future__ import annotations

import json
import re

from tools.lookml_web_advice import is_expression_conversion_request, search_lookml_best_practices
from tools.phase1_tools import (
    get_current_pbix,
    get_object_counts,
    list_measures,
    list_power_query,
    list_relationships,
    list_tables,
    search_columns,
)
from tools.phase2_tools import (
    get_phase2_summary,
    get_user_input_placeholders,
    list_lookml_views,
    list_mapped_objects,
)
from tools.phase3_tools import (
    get_dashboard_coverage,
    get_phase3_summary,
    get_validation_summary,
    list_lookml_dashboards,
    list_report_pages,
    search_visuals,
)


def _wants(q: str, *words: str) -> bool:
    ql = q.lower()
    return any(w in ql for w in words)


def build_grounding_context(question: str = "") -> str:
    """Always-on facts + specialist enrichment based on the question."""
    q = question or ""
    specialists_used: list[str] = []

    payload: dict = {
        "current_pbix": get_current_pbix(),
        "object_counts": get_object_counts(),
        "phase2_summary": get_phase2_summary(),
        "phase3_summary": get_phase3_summary(),
        "dashboard_coverage": get_dashboard_coverage(),
        "validation_summary": get_validation_summary(),
    }

    # Specialist 1 — inventory
    if _wants(q, "table", "column", "measure", "dax", "relationship", "power query", "m query", "inventory", "model", "count", "what is", "hi", "hello"):
        specialists_used.append("inventory")
        payload["tables"] = list_tables(business_only=True)
        if _wants(q, "measure", "dax", "kpi", "expression", "convert"):
            payload["measures"] = list_measures(search="", limit=25)
        if _wants(q, "column"):
            m = re.search(r"column[s]?\s+(\w+)", q.lower())
            payload["columns"] = search_columns(m.group(1) if m else "", limit=20)
        if _wants(q, "relationship", "join"):
            payload["relationships"] = list_relationships()
        if _wants(q, "power query", "m query", "m file"):
            payload["power_query"] = list_power_query()

    # Specialist 2 — LookML
    if _wants(q, "lookml", "looker", "view", "todo", "placeholder", "connection", "sql_table", "mapping", "phase 2", "semantic", "convert", "expression"):
        specialists_used.append("lookml")
        payload["lookml_views"] = list_lookml_views()
        payload["mapped_objects_todo"] = list_mapped_objects(status="todo", limit=25)
        payload["user_placeholders"] = get_user_input_placeholders()

    # Specialist 3 — dashboards / validation
    if _wants(q, "dashboard", "page", "visual", "coverage", "gap", "slicer", "validation", "percent", "%", "complete", "phase 3"):
        specialists_used.append("dashboards")
        payload["report_pages"] = list_report_pages()
        payload["lookml_dashboards"] = list_lookml_dashboards()
        if _wants(q, "gap", "partial", "missing"):
            payload["gap_visuals"] = search_visuals(status="gap", limit=20)
            payload["partial_visuals"] = search_visuals(status="partial", limit=20)

    # Expression conversion — web + curated Looker best practices
    if is_expression_conversion_request(q):
        specialists_used.append("lookml_web_advice")
        payload["lookml_expression_advice"] = search_lookml_best_practices(q)

    if not specialists_used:
        specialists_used = ["overview"]
        payload["tables"] = list_tables(business_only=True)

    payload["specialists_used"] = specialists_used
    payload["question"] = q

    raw = json.dumps(payload, ensure_ascii=False, default=str)
    if len(raw) > 18000:
        raw = raw[:18000] + "...[truncated]"

    return (
        "GROUNDING_CONTEXT:\n"
        "- inventory_* fields = facts from the CURRENT PBIX extract (authoritative).\n"
        "- lookml_expression_advice = web/curated Looker best practices for expression conversion "
        "(use under Recommendation: — do not invent inventory facts from this).\n"
        f"{raw}\n\n"
        "USER_QUESTION:\n"
        f"{q}"
    )
