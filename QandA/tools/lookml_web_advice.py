"""Web search for LookML / DAX→Looker expression best practices.

Grounded in Google Looker docs + looker-open-source/looker-skills.
When the network is unavailable, curated fallbacks still encode accurate patterns.
"""
from __future__ import annotations

import re
from typing import Any

# Curated fallbacks aligned with official Looker docs + looker-skills
_STATIC_BEST_PRACTICES = [
    {
        "title": "LookML measure types (incl. measure-of-measures)",
        "href": "https://cloud.google.com/looker/docs/reference/param-measure-types",
        "body": (
            "Map SUM→type:sum, AVERAGE→type:average, COUNT/DISTINCTCOUNT→type:count_distinct. "
            "A measure based on other measures MUST be type: number and reference them with "
            "${measure_a} (never nest aggregates). Prefer ${dimension} inside aggregate sql "
            "(looker-skills modeling guidelines)."
        ),
    },
    {
        "title": "Safe division (NULLIF + float)",
        "href": "https://cloud.google.com/looker/docs/best-practices/how-to-troubleshoot-fields-with-division-displaying-0",
        "body": (
            "Ratios: type: number; sql: 1.0 * ${num} / NULLIF(${den}, 0) ;; "
            "(or 100.0 * for percents). Multiplying by 1.0/100.0 forces float results. "
            "BigQuery-only alternative: SAFE_DIVIDE(${num}, ${den})."
        ),
    },
    {
        "title": "filters: on aggregate measures only",
        "href": "https://cloud.google.com/looker/docs/reference/param-field-filters",
        "body": (
            "DAX CALCULATE with filters → LookML filters: [field: \"value\"] on type:sum|average|"
            "count|count_distinct. NEVER put filters: on type: number. Instead filter the base "
            "aggregates that the number measure references (e.g. filtered twins)."
        ),
    },
    {
        "title": "Dependent measures — tell the user",
        "href": "https://cloud.google.com/looker/docs/reference/param-measure-types",
        "body": (
            "If measure B references measure A (e.g. [A]-[B], DIVIDE([A],[B]), ROUND([A]/30)), "
            "say DEPENDS ON: A (and B). Implement bases first. Example: "
            "measure: seps_yoy_var { type: number sql: ${seps} - ${seps_sply} ;; }"
        ),
    },
    {
        "title": "Time intelligence",
        "href": "https://cloud.google.com/looker/docs/timeframes-for-dimension-groups",
        "body": (
            "SAMEPERIODLASTYEAR / DATEADD: use dimension_group timeframes, Looker period-over-period "
            "patterns, or warehouse prior-period columns — do not paste DAX into LookML."
        ),
    },
    {
        "title": "looker-skills: views & explores",
        "href": "https://github.com/looker-open-source/looker-skills",
        "body": (
            "Every view needs primary_key: yes (symmetric aggregates). Explores must set "
            "relationship: explicitly on joins. Granular includes; descriptions on explores/fields."
        ),
    },
    {
        "title": "sql_table_name vs derived tables",
        "href": "https://cloud.google.com/looker/docs/derived-tables",
        "body": (
            "Prefer warehouse views + sql_table_name. Use SQL derived tables only as a "
            "temporary bridge; native derived tables for Looker-native rollups."
        ),
    },
]


def is_expression_conversion_request(text: str) -> bool:
    q = (text or "").lower()
    if not q:
        return False
    convert_words = (
        "convert",
        "translate",
        "rewrite",
        "equivalent",
        "lookml expression",
        "to lookml",
        "into lookml",
        "as lookml",
        "dax to",
        "how to write",
        "suggest lookml",
        "lookml for",
        "depends on",
        "dependent measure",
    )
    has_convert = any(w in q for w in convert_words)
    looks_like_expr = bool(
        re.search(
            r"(calculate\s*\(|sumx?\s*\(|averagex?\s*\(|divide\s*\(|"
            r"distinctcount|sameperiodlastyear|dateadd|filter\s*\(|"
            r"type:\s*\w+|measure:|dimension:|\$\{)",
            q,
            re.I,
        )
    )
    return has_convert or (looks_like_expr and ("lookml" in q or "looker" in q or "dax" in q))


def _extract_expression_snippet(text: str) -> str:
    """Best-effort pull of a code-like snippet from the user question."""
    m = re.search(r"```(?:dax|lookml|sql)?\s*([\s\S]+?)```", text or "", re.I)
    if m:
        return m.group(1).strip()[:500]
    m = re.search(r"[\"']([^\"']{8,400})[\"']", text or "")
    if m:
        return m.group(1).strip()
    m = re.search(
        r"(?:convert|translate|rewrite)\s+(.+?)\s+(?:to|into)\s+lookml",
        text or "",
        re.I | re.S,
    )
    if m:
        return m.group(1).strip()[:500]
    return (text or "").strip()[:400]


def _local_pattern_hint(expr: str) -> dict[str, Any] | None:
    """Deterministic hint using Phase 2 classifier when available."""
    try:
        import sys
        from pathlib import Path

        phase2 = Path(__file__).resolve().parents[2] / "phase2"
        if str(phase2) not in sys.path:
            sys.path.insert(0, str(phase2))
        from lib.dax_patterns import classify_dax, extract_measure_refs

        refs = extract_measure_refs(expr)
        plan = classify_dax(expr, "user_measure", set(refs) if refs else None)
        return {
            "strategy": plan.strategy,
            "lookml_type": plan.lookml_type,
            "depends_on": plan.depends_on or refs,
            "sql_expression": plan.sql_expression,
            "filters": [{"field": f, "value": v} for f, v in plan.filters],
            "mapped": plan.mapped,
            "dependency_warning": plan.dependency_warning,
            "notes": plan.notes[:4],
            "recommended_sql_pattern": plan.sql_expression
            or (
                f"type: {plan.lookml_type}; sql: ${{{plan.sql}}} ;;"
                if plan.sql and plan.lookml_type in {"sum", "average", "count_distinct"}
                else None
            ),
        }
    except Exception as e:
        return {"classifier_error": str(e)}


def search_lookml_best_practices(question: str, max_results: int = 5) -> dict[str, Any]:
    """Search the web for LookML / DAX migration guidance; fall back to curated docs."""
    expr = _extract_expression_snippet(question)
    local = _local_pattern_hint(expr) if expr else None
    queries = [
        f"Looker LookML equivalent of DAX {expr[:120]}",
        f"LookML best practice measure {expr[:80]} site:cloud.google.com/looker",
        "LookML type number measure based on other measures NULLIF division",
        "LookML filters parameter aggregate measures not type number",
        "looker-open-source looker-skills lookml modeling guidelines",
    ]
    hits: list[dict[str, str]] = []
    errors: list[str] = []

    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            for query in queries:
                try:
                    for r in ddgs.text(query, max_results=3):
                        hits.append(
                            {
                                "title": (r.get("title") or "")[:160],
                                "href": r.get("href") or r.get("link") or "",
                                "body": (r.get("body") or r.get("snippet") or "")[:400],
                                "query": query,
                            }
                        )
                        if len(hits) >= max_results:
                            break
                except Exception as e:
                    errors.append(f"{query[:40]}…: {e}")
                if len(hits) >= max_results:
                    break
    except Exception as e:
        errors.append(str(e))

    used_fallback = False
    if len(hits) < 2:
        used_fallback = True
        for row in _STATIC_BEST_PRACTICES:
            hits.append({**row, "query": "curated_looker_docs"})
            if len(hits) >= max_results + 2:
                break

    dep_note = ""
    if local and local.get("depends_on"):
        dep_note = (
            f" DEPENDS ON: {', '.join(local['depends_on'])}. "
            "Say this clearly to the user before showing LookML."
        )

    return {
        "conversion_request": True,
        "extracted_expression": expr,
        "local_classifier": local,
        "web_results": hits[: max_results + 2],
        "used_curated_fallback": used_fallback,
        "search_errors": errors[:3],
        "instruction_for_model": (
            "Suggest accurate LookML using official patterns: "
            "aggregates use type sum/average/count_distinct with dimension refs; "
            "measure-of-measures use type: number + measure refs; "
            "ratios use 1.0 * num / NULLIF(den, 0); "
            "filters: only on aggregate measures. "
            "If one measure depends on another, start with 'DEPENDS ON: …'."
            f"{dep_note} "
            "Cite web/curated best practices. Label as Recommendation: "
            "separate from inventory Facts about the current PBIX."
        ),
    }
