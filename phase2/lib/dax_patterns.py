"""Deterministic DAX expression → LookML measure pattern classifier.

Rules are regex/heuristic only (no LLM). Complex patterns become TODO stubs
with the original DAX preserved in comments for the Looker developer.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class MeasurePlan:
    strategy: str  # direct_sum | direct_average | direct_count | count_distinct | ratio | filtered | complex_todo | parameter_value
    lookml_type: str
    sql: str | None = None
    filters: list[tuple[str, str]] = field(default_factory=list)  # (field_ref_hint, value)
    notes: list[str] = field(default_factory=list)
    value_format: str | None = None


_COL_REF = r"(?:'[^']+'|[\w ]+)\[([^\]]+)\]"
_TABLE_COL = re.compile(
    r"(?:'([^']+)'|([\w ]+))\[([^\]]+)\]",
    re.IGNORECASE,
)


def _norm_expr(expr: str) -> str:
    return re.sub(r"\s+", " ", (expr or "").strip())


def extract_table_column(expr: str) -> tuple[str | None, str | None]:
    m = _TABLE_COL.search(expr or "")
    if not m:
        return None, None
    table = (m.group(1) or m.group(2) or "").strip()
    col = (m.group(3) or "").strip()
    return table or None, col or None


def classify_dax(expression: str, measure_name: str) -> MeasurePlan:
    """Map a DAX measure expression to a LookML implementation plan."""
    expr = _norm_expr(expression)
    upper = expr.upper()
    notes: list[str] = []

    # SELECTEDVALUE parameter-like
    if upper.startswith("SELECTEDVALUE("):
        return MeasurePlan(
            strategy="parameter_value",
            lookml_type="number",
            sql=None,
            notes=[
                "Power BI SELECTEDVALUE → Looker parameter or filter-only dimension.",
                f"Original DAX: {expr}",
            ],
        )

    # Simple SUM(Table[Col])
    m = re.fullmatch(rf"SUM\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return MeasurePlan(
            strategy="direct_sum",
            lookml_type="sum",
            sql=m.group(1).strip(),
            notes=["Direct SUM → type: sum"],
        )

    m = re.fullmatch(rf"AVERAGE\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return MeasurePlan(
            strategy="direct_average",
            lookml_type="average",
            sql=m.group(1).strip(),
            notes=["Direct AVERAGE → type: average"],
        )

    m = re.fullmatch(rf"COUNT\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return MeasurePlan(
            strategy="direct_count",
            lookml_type="count",
            sql=m.group(1).strip(),
            notes=["Direct COUNT → type: count (prefer count_distinct on PK if uniqueness required)"],
        )

    m = re.fullmatch(rf"DISTINCTCOUNT\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return MeasurePlan(
            strategy="count_distinct",
            lookml_type="count_distinct",
            sql=m.group(1).strip(),
            notes=["DISTINCTCOUNT → type: count_distinct"],
        )

    # Ratio of two bracket measure refs: [A]/[B] or DIVIDE([A],[B])
    m = re.fullmatch(r"\[([^\]]+)\]\s*/\s*\[([^\]]+)\]", expr)
    if m:
        return MeasurePlan(
            strategy="ratio",
            lookml_type="number",
            sql=None,
            notes=[
                f"Ratio of measures [{m.group(1)}] / [{m.group(2)}] → SAFE_DIVIDE(${{{_snake(m.group(1))}}}, ${{{_snake(m.group(2))}}})",
                "Wire after child measures exist on the same view/explore.",
            ],
            value_format="percent_2" if "%" in measure_name or "pct" in measure_name.lower() else "decimal_2",
        )

    m = re.fullmatch(r"DIVIDE\(\s*\[([^\]]+)\]\s*,\s*\[([^\]]+)\]\s*(?:,\s*[^)]+)?\)", expr, re.IGNORECASE)
    if m:
        return MeasurePlan(
            strategy="ratio",
            lookml_type="number",
            sql=None,
            notes=[
                f"DIVIDE([{m.group(1)}], [{m.group(2)}]) → SAFE_DIVIDE of LookML measures",
            ],
            value_format="percent_2" if "%" in measure_name else "decimal_2",
        )

    # SUM(a)+SUM(b)
    if re.fullmatch(
        rf"SUM\(\s*{_COL_REF}\s*\)\s*\+\s*SUM\(\s*{_COL_REF}\s*\)",
        expr,
        re.IGNORECASE,
    ):
        cols = re.findall(_COL_REF, expr, flags=re.IGNORECASE)
        return MeasurePlan(
            strategy="sum_plus_sum",
            lookml_type="number",
            sql=None,
            notes=[
                f"Sum of two columns {cols} → type: number sql: ${{{_snake(cols[0])}}} + ${{{_snake(cols[1])}}} "
                "after defining sum measures, or single sql with + of ${TABLE} cols",
            ],
        )

    # SUM(a)/SUM(b)
    m = re.fullmatch(
        rf"SUM\(\s*{_COL_REF}\s*\)\s*/\s*SUM\(\s*{_COL_REF}\s*\)",
        expr,
        re.IGNORECASE,
    )
    if m:
        return MeasurePlan(
            strategy="sum_over_sum",
            lookml_type="number",
            sql=None,
            notes=[f"SUM/SUM ratio on columns {m.group(1)} / {m.group(2)}"],
            value_format="decimal_2",
        )

    # Time intelligence / iterators → complex
    complex_tokens = (
        "DATESYTD",
        "DATESQTD",
        "DATESMTD",
        "DATEADD",
        "DATESINPERIOD",
        "SAMEPERIODLASTYEAR",
        "PARALLELPERIOD",
        "TOTALYTD",
        "SUMX",
        "AVERAGEX",
        "RANKX",
        "USERELATIONSHIP",
        "SELECTEDVALUE",
        "ALL(",
        "ALLEXCEPT",
        "FILTER(",
    )
    if any(tok in upper for tok in complex_tokens) or upper.startswith("CALCULATE"):
        notes.append("Complex / filter / time-intel DAX — implement with LookML filters, period-over-period patterns, or warehouse.")
        notes.append(f"Original DAX: {expr}")
        # Try to extract simple CALCULATE([M], Table[Col] = "X")
        simple = _try_simple_calculate(expr)
        if simple:
            return simple
        return MeasurePlan(
            strategy="complex_todo",
            lookml_type="number",
            sql=None,
            notes=notes,
        )

    return MeasurePlan(
        strategy="complex_todo",
        lookml_type="number",
        sql=None,
        notes=[f"Unclassified DAX — developer review required. Original: {expr}"],
    )


def _snake(name: str) -> str:
    from .naming import snake_case

    return snake_case(name)


def _try_simple_calculate(expr: str) -> MeasurePlan | None:
    """CALCULATE([Measure], Table[Col] = \"Value\") with one equality filter."""
    m = re.match(
        r"CALCULATE\(\s*\[([^\]]+)\]\s*,\s*(?:'([^']+)'|([\w ]+))\[([^\]]+)\]\s*=\s*\"([^\"]+)\"\s*\)",
        _norm_expr(expr),
        re.IGNORECASE,
    )
    if not m:
        return None
    base = m.group(1).strip()
    table = (m.group(2) or m.group(3) or "").strip()
    col = m.group(4).strip()
    val = m.group(5)
    return MeasurePlan(
        strategy="filtered",
        lookml_type="number",
        sql=None,
        filters=[(f"{table}.{col}", val)],
        notes=[
            f"CALCULATE([{base}], {table}[{col}] = \"{val}\") → filtered measure / filters: block on base measure",
            "Prefer explore filters or measure filters: [view.field: \"value\"]",
        ],
    )
