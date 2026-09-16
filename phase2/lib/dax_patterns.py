"""Deterministic DAX expression → LookML measure pattern classifier.

Grounded in:
- Google Looker docs (measure types, filters, division/NULLIF, measure-of-measures)
- looker-open-source/looker-skills (lookml-view, lookml-explore, modeling-guidelines)

Rules are regex/heuristic only (no LLM). Complex patterns become TODO stubs
with the original DAX preserved. Dependent measures are always surfaced so
developers know implementation order.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .naming import lookml_field_name, snake_case


@dataclass
class MeasurePlan:
    """Plan for one Power BI measure → LookML measure."""

    strategy: str
    lookml_type: str
    # Column name for aggregate sql (sum/avg/count_distinct), when applicable
    sql: str | None = None
    # LookML sql expression using ${field} refs (for type: number)
    sql_expression: str | None = None
    filters: list[tuple[str, str]] = field(default_factory=list)  # (lookml_field, filter_expr)
    notes: list[str] = field(default_factory=list)
    value_format: str | None = None
    # Power BI measure names this measure depends on (implementation order)
    depends_on: list[str] = field(default_factory=list)
    # True when LookML is complete enough to compile (placeholders may remain for SQL table)
    mapped: bool = False
    # Human warning for the developer guide / field description
    dependency_warning: str | None = None


# Column ref: Table[Col], 'Table'[Col], or bare [Col]
_COL_REF = r"(?:(?:'[^']+'|[\w ]+)\[|\[)([^\]]+)\]"
_TABLE_COL = re.compile(
    r"(?:'([^']+)'|([\w ]+))\[([^\]]+)\]",
    re.IGNORECASE,
)
_BARE_BRACKET = re.compile(r"\[([^\]]+)\]")
_BARE_MEASURE = re.compile(r"(?<![\w'])\[([^\]]+)\]")

# Time-intel / iterators that cannot be auto-mapped to accurate LookML
_COMPLEX_TOKENS = (
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
    "ALLEXCEPT",
    "ALLSELECTED",
    "KEEPFILTERS",
)


def _norm_expr(expr: str) -> str:
    return re.sub(r"\s+", " ", (expr or "").strip())


def _snake(name: str) -> str:
    return snake_case(name)


def _lookml_ref(name: str) -> str:
    return lookml_field_name(name)


def extract_table_column(expr: str) -> tuple[str | None, str | None]:
    m = _TABLE_COL.search(expr or "")
    if not m:
        return None, None
    table = (m.group(1) or m.group(2) or "").strip()
    col = (m.group(3) or "").strip()
    return table or None, col or None


def extract_measure_refs(expression: str, known_measures: set[str] | None = None) -> list[str]:
    """Return Power BI measure names referenced as [Name], excluding column refs Table[Col]."""
    expr = expression or ""
    # Strip Table[Col] / 'Table'[Col] so we don't treat qualified columns as measures
    stripped = _TABLE_COL.sub(" ", expr)
    # Also strip aggregate wrappers' bare columns when we only want measure-to-measure deps:
    # keep bare [Name] tokens; caller filters via known_measures.
    refs: list[str] = []
    seen: set[str] = set()
    for m in _BARE_BRACKET.finditer(stripped):
        name = m.group(1).strip()
        if not name or name in seen:
            continue
        if known_measures is not None and name not in known_measures:
            continue
        seen.add(name)
        refs.append(name)
    return refs


def _ratio_sql(num_lookml: str, den_lookml: str, *, as_percent: bool = False) -> str:
    """Official Looker division pattern: float cast + NULLIF (dialect-portable).

    Refs:
    - https://cloud.google.com/looker/docs/best-practices/how-to-troubleshoot-fields-with-division-displaying-0
    - https://cloud.google.com/looker/docs/reference/param-field-sql (NULLIF)
    BigQuery-only alternative: SAFE_DIVIDE(${a}, ${b})
    """
    scale = "100.0 *" if as_percent else "1.0 *"
    return f"{scale} ${{{num_lookml}}} / NULLIF(${{{den_lookml}}}, 0)"


def _is_percent_name(measure_name: str) -> bool:
    n = (measure_name or "").lower()
    return any(tok in n for tok in ("% ", "%", "pct", "percent", "ratio", "rate"))


def _has_complex_time_intel(upper: str) -> bool:
    return any(tok in upper for tok in _COMPLEX_TOKENS)


def classify_dax(
    expression: str,
    measure_name: str,
    known_measures: set[str] | None = None,
) -> MeasurePlan:
    """Map a DAX measure expression to a LookML implementation plan."""
    expr = _norm_expr(expression)
    upper = expr.upper()
    known = known_measures or set()
    # Always treat sibling measures as known for dependency extraction when provided
    deps = [d for d in extract_measure_refs(expr, known if known else None) if d != measure_name]

    def with_deps(plan: MeasurePlan) -> MeasurePlan:
        # Merge regex deps with any already set
        merged: list[str] = []
        for d in list(plan.depends_on) + deps:
            if d and d not in merged and d != measure_name:
                merged.append(d)
        plan.depends_on = merged
        if plan.depends_on:
            dep_list = ", ".join(plan.depends_on)
            plan.dependency_warning = (
                f"DEPENDS ON: {dep_list}. Implement those LookML measures first. "
                f"This measure must be type: number and reference them via ${{measure}} "
                f"(Looker: measures based on other measures)."
            )
            if plan.dependency_warning not in plan.notes:
                plan.notes.append(plan.dependency_warning)
        return plan

    # SELECTEDVALUE parameter-like
    if upper.startswith("SELECTEDVALUE("):
        return with_deps(
            MeasurePlan(
                strategy="parameter_value",
                lookml_type="number",
                notes=[
                    "Power BI SELECTEDVALUE → Looker parameter or filter-only dimension.",
                    f"Original DAX: {expr}",
                    "Ref: https://cloud.google.com/looker/docs/reference/param-field-parameter",
                ],
            )
        )

    # --- Simple aggregates -------------------------------------------------
    m = re.fullmatch(rf"SUM\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return with_deps(
            MeasurePlan(
                strategy="direct_sum",
                lookml_type="sum",
                sql=m.group(1).strip(),
                notes=[
                    "Direct SUM → type: sum; sql uses ${dimension} (looker-skills).",
                    "Ref: https://cloud.google.com/looker/docs/reference/param-measure-types",
                ],
                mapped=True,
            )
        )

    m = re.fullmatch(rf"AVERAGE\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return with_deps(
            MeasurePlan(
                strategy="direct_average",
                lookml_type="average",
                sql=m.group(1).strip(),
                notes=["Direct AVERAGE → type: average"],
                mapped=True,
            )
        )

    # ROUND(AVERAGE([Col]), n)
    m = re.fullmatch(
        rf"ROUND\(\s*AVERAGE\(\s*{_COL_REF}\s*\)\s*,\s*(\d+)\s*\)",
        expr,
        re.IGNORECASE,
    )
    if m:
        decimals = int(m.group(2))
        fmt = "decimal_0" if decimals == 0 else "decimal_2"
        return with_deps(
            MeasurePlan(
                strategy="direct_average",
                lookml_type="average",
                sql=m.group(1).strip(),
                value_format=fmt,
                notes=[
                    f"ROUND(AVERAGE(...), {decimals}) → type: average + value_format_name: {fmt}",
                    "Prefer value_format over wrapping ROUND in measure sql for aggregates.",
                ],
                mapped=True,
            )
        )

    m = re.fullmatch(rf"COUNT\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return with_deps(
            MeasurePlan(
                strategy="count_distinct",
                lookml_type="count_distinct",
                sql=m.group(1).strip(),
                notes=[
                    "DAX COUNT on a key → type: count_distinct (safer under joins / symmetric aggregates).",
                ],
                mapped=True,
            )
        )

    m = re.fullmatch(rf"COUNTA\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return with_deps(
            MeasurePlan(
                strategy="direct_count",
                lookml_type="count",
                sql=m.group(1).strip(),
                notes=["COUNTA → type: count (non-null rows); use count_distinct on PK if uniqueness required."],
                mapped=True,
            )
        )

    m = re.fullmatch(rf"DISTINCTCOUNT\(\s*{_COL_REF}\s*\)", expr, re.IGNORECASE)
    if m:
        return with_deps(
            MeasurePlan(
                strategy="count_distinct",
                lookml_type="count_distinct",
                sql=m.group(1).strip(),
                notes=["DISTINCTCOUNT → type: count_distinct"],
                mapped=True,
            )
        )

    # --- Measure arithmetic / transforms (type: number) --------------------
    # DIVIDE([A],[B]) or [A]/[B]
    m = re.fullmatch(r"DIVIDE\(\s*\[([^\]]+)\]\s*,\s*\[([^\]]+)\]\s*(?:,\s*[^)]+)?\)", expr, re.IGNORECASE)
    if not m:
        m = re.fullmatch(r"\[([^\]]+)\]\s*/\s*\[([^\]]+)\]", expr)
    if m:
        a, b = m.group(1).strip(), m.group(2).strip()
        as_pct = _is_percent_name(measure_name)
        return with_deps(
            MeasurePlan(
                strategy="measure_ratio",
                lookml_type="number",
                sql_expression=_ratio_sql(_lookml_ref(a), _lookml_ref(b), as_percent=as_pct),
                depends_on=[a, b],
                value_format="percent_2" if as_pct else "decimal_2",
                notes=[
                    f"DIVIDE/ratio of measures [{a}] / [{b}] → type: number with 1.0 * ${{a}} / NULLIF(${{b}}, 0).",
                    "Do NOT put filters: on type: number — filter the base aggregate measures instead.",
                    "Refs: measure types (type: number), division best practice (NULLIF + float).",
                ],
                mapped=True,
            )
        )

    # [A]-[B] / [A]+[B] / [A]*[B]
    m = re.fullmatch(r"\[([^\]]+)\]\s*([+\-*])\s*\[([^\]]+)\]", expr)
    if m:
        a, op, b = m.group(1).strip(), m.group(2), m.group(3).strip()
        return with_deps(
            MeasurePlan(
                strategy="measure_math",
                lookml_type="number",
                sql_expression=f"${{{_lookml_ref(a)}}} {op} ${{{_lookml_ref(b)}}}",
                depends_on=[a, b],
                notes=[
                    f"Measure arithmetic [{a}] {op} [{b}] → type: number referencing ${{measures}}.",
                    "Ref: https://cloud.google.com/looker/docs/reference/param-measure-types#number",
                ],
                mapped=True,
            )
        )

    # ROUND([Measure]/N, d) optional trailing -K / +K
    m = re.fullmatch(
        r"ROUND\(\s*\[([^\]]+)\]\s*/\s*([\d.]+)\s*,\s*(\d+)\s*\)\s*([+\-]\s*[\d.]+)?",
        expr,
        re.IGNORECASE,
    )
    if m:
        base = m.group(1).strip()
        divisor = m.group(2)
        decimals = m.group(3)
        tail = (m.group(4) or "").replace(" ", "")
        div_sql = divisor if "." in divisor else f"{divisor}.0"
        sql = f"ROUND(${{{_lookml_ref(base)}}} / {div_sql}, {decimals})"
        if tail:
            sql = f"{sql} {tail[0]} {tail[1:]}"
        return with_deps(
            MeasurePlan(
                strategy="measure_transform",
                lookml_type="number",
                sql_expression=sql,
                depends_on=[base],
                value_format="decimal_1" if decimals == "1" else "decimal_2",
                notes=[
                    f"Transform of [{base}] → type: number. DEPENDS ON [{base}].",
                ],
                mapped=True,
            )
        )

    # SUM(a)+SUM(b) as two sum measures composed
    if re.fullmatch(
        rf"SUM\(\s*{_COL_REF}\s*\)\s*\+\s*SUM\(\s*{_COL_REF}\s*\)",
        expr,
        re.IGNORECASE,
    ):
        cols = re.findall(_COL_REF, expr, flags=re.IGNORECASE)
        c1, c2 = cols[0], cols[1]
        # Prefer defining two sum measures then type:number — emit inline sums via dimensions
        return with_deps(
            MeasurePlan(
                strategy="sum_plus_sum",
                lookml_type="number",
                sql_expression=None,  # generator expands via helper sum measures or TABLE sum
                sql=f"{c1}|{c2}",
                notes=[
                    f"SUM({c1})+SUM({c2}) → create two type:sum measures then type:number, "
                    "or single sql with SUM of both (prefer two measures for reuse).",
                    "filters: cannot be applied to type: number.",
                ],
                mapped=True,
            )
        )

    # SUM(a)/SUM(b)
    m = re.fullmatch(
        rf"SUM\(\s*{_COL_REF}\s*\)\s*/\s*SUM\(\s*{_COL_REF}\s*\)",
        expr,
        re.IGNORECASE,
    )
    if m:
        c1, c2 = m.group(1).strip(), m.group(2).strip()
        # Generator should emit helper sums or use nested aggregate carefully —
        # Best practice: two sum measures + type number ratio.
        return with_deps(
            MeasurePlan(
                strategy="sum_over_sum",
                lookml_type="number",
                sql=f"{c1}|{c2}",
                value_format="percent_2" if _is_percent_name(measure_name) else "decimal_2",
                notes=[
                    f"SUM/SUM on [{c1}]/[{c2}] → two type:sum measures + type:number with NULLIF.",
                    "Do not put filters on the ratio measure.",
                ],
                mapped=True,
            )
        )

    # --- Filtered aggregates (CALCULATE + FILTER ISBLANK / equality) -------
    simple_filt = _try_filtered_aggregate(expr)
    if simple_filt:
        return with_deps(simple_filt)

    simple_calc = _try_simple_calculate(expr, known)
    if simple_calc:
        return with_deps(simple_calc)

    # Time intelligence or remaining CALCULATE/FILTER → TODO but keep deps
    if _has_complex_time_intel(upper) or "CALCULATE(" in upper or "FILTER(" in upper or "ALL(" in upper:
        notes = [
            "Complex / filter / time-intel DAX — implement with LookML period patterns, "
            "filtered aggregate measures, or warehouse metrics.",
            "Do not claim KPI parity until side-by-side validation.",
            f"Original DAX: {expr}",
            "Refs: https://cloud.google.com/looker/docs/reference/param-field-filters",
            "https://cloud.google.com/looker/docs/reference/param-measure-types",
        ]
        return with_deps(
            MeasurePlan(
                strategy="complex_todo",
                lookml_type="number",
                notes=notes,
                mapped=False,
            )
        )

    # Bare measure pass-through: [Other Measure]
    m = re.fullmatch(r"\[([^\]]+)\]", expr)
    if m:
        base = m.group(1).strip()
        return with_deps(
            MeasurePlan(
                strategy="measure_alias",
                lookml_type="number",
                sql_expression=f"${{{_lookml_ref(base)}}}",
                depends_on=[base],
                notes=[f"Alias of [{base}] → type: number sql: ${{{_lookml_ref(base)}}}"],
                mapped=True,
            )
        )

    return with_deps(
        MeasurePlan(
            strategy="complex_todo",
            lookml_type="number",
            notes=[f"Unclassified DAX — developer review required. Original: {expr}"],
            mapped=False,
        )
    )


def _try_filtered_aggregate(expr: str) -> MeasurePlan | None:
    """CALCULATE(COUNT|SUM|AVERAGE([Col]), FILTER(Table, ISBLANK / NOT ISBLANK / = \"x\"))."""
    e = _norm_expr(expr)

    # COUNT/SUM/AVERAGE with ISBLANK / NOT(ISBLANK(...)) / NOT ISBLANK(...)
    m = re.match(
        rf"CALCULATE\(\s*(COUNT|SUM|AVERAGE|DISTINCTCOUNT)\(\s*{_COL_REF}\s*\)\s*,\s*"
        rf"FILTER\(\s*(?:'([^']+)'|([\w ]+))\s*,\s*"
        rf"(?:(NOT)\s*\(\s*ISBLANK\(\s*{_COL_REF}\s*\)\s*\)|(NOT)\s+ISBLANK\(\s*{_COL_REF}\s*\)|ISBLANK\(\s*{_COL_REF}\s*\))"
        rf"\s*\)\s*\)",
        e,
        re.IGNORECASE,
    )
    if m:
        agg = m.group(1).upper()
        col = m.group(2).strip()
        # Groups: 3/4 table, then either (5=NOT, 6=col) or (7=NOT, 8=col) or (9=col)
        is_not = bool(m.group(5) or m.group(7))
        filt_col = (m.group(6) or m.group(8) or m.group(9) or "").strip()
        lookml_filt = _lookml_ref(filt_col)
        filt_expr = "-NULL" if is_not else "NULL"
        type_map = {
            "COUNT": ("filtered_aggregate", "count_distinct"),
            "DISTINCTCOUNT": ("filtered_aggregate", "count_distinct"),
            "SUM": ("filtered_aggregate", "sum"),
            "AVERAGE": ("filtered_aggregate", "average"),
        }
        strategy, ltype = type_map[agg]
        return MeasurePlan(
            strategy=strategy,
            lookml_type=ltype,
            sql=col,
            filters=[(lookml_filt, filt_expr)],
            notes=[
                f"CALCULATE({agg}([{col}]), FILTER(..., {'NOT ' if is_not else ''}ISBLANK([{filt_col}]))) "
                f"→ type: {ltype} with filters: [{lookml_filt}: \"{filt_expr}\"].",
                "filters: only valid on aggregate measure types (not type: number).",
                "Ref: https://cloud.google.com/looker/docs/reference/param-field-filters",
            ],
            mapped=True,
        )

    # Equality filter: CALCULATE(AGG([Col]), Table[Col] = "Value")
    m = re.match(
        rf"CALCULATE\(\s*(COUNT|SUM|AVERAGE|DISTINCTCOUNT)\(\s*{_COL_REF}\s*\)\s*,\s*"
        rf"(?:'([^']+)'|([\w ]+))\[([^\]]+)\]\s*=\s*\"([^\"]+)\"\s*\)",
        e,
        re.IGNORECASE,
    )
    if m:
        agg = m.group(1).upper()
        col = m.group(2).strip()
        filt_col = m.group(5).strip()
        val = m.group(6)
        type_map = {
            "COUNT": ("filtered_aggregate", "count_distinct"),
            "DISTINCTCOUNT": ("filtered_aggregate", "count_distinct"),
            "SUM": ("filtered_aggregate", "sum"),
            "AVERAGE": ("filtered_aggregate", "average"),
        }
        strategy, ltype = type_map[agg]
        return MeasurePlan(
            strategy=strategy,
            lookml_type=ltype,
            sql=col,
            filters=[(_lookml_ref(filt_col), val)],
            notes=[
                f"CALCULATE({agg}([{col}]), [{filt_col}]=\"{val}\") → filters on aggregate measure.",
                "Ref: https://cloud.google.com/looker/docs/reference/param-field-filters",
            ],
            mapped=True,
        )

    return None


def _try_simple_calculate(expr: str, known_measures: set[str]) -> MeasurePlan | None:
    """CALCULATE([Measure], Table[Col] = \"Value\") or CALCULATE([Measure], FILTER(..., ISBLANK))."""
    e = _norm_expr(expr)

    # CALCULATE([M], Table[Col] = "Value")
    m = re.match(
        r"CALCULATE\(\s*\[([^\]]+)\]\s*,\s*(?:'([^']+)'|([\w ]+))\[([^\]]+)\]\s*=\s*\"([^\"]+)\"\s*\)",
        e,
        re.IGNORECASE,
    )
    if m:
        base = m.group(1).strip()
        table = (m.group(2) or m.group(3) or "").strip()
        col = m.group(4).strip()
        val = m.group(5)
        return MeasurePlan(
            strategy="filtered_measure",
            lookml_type="number",
            depends_on=[base],
            filters=[(_lookml_ref(col), val)],
            notes=[
                f"CALCULATE([{base}], {table}[{col}] = \"{val}\").",
                "Looker: filters: cannot be used on type: number. "
                f"Apply filters to the aggregate measures that compose [{base}], "
                "or create a filtered twin of the base aggregate.",
                f"DEPENDS ON: {base}",
                "Ref: https://cloud.google.com/looker/docs/reference/param-field-filters",
            ],
            mapped=False,
        )

    # CALCULATE([M], FILTER(Table, NOT(ISBLANK(...)) / ISBLANK(...)))
    m = re.match(
        r"CALCULATE\(\s*\[([^\]]+)\]\s*,\s*"
        rf"FILTER\(\s*(?:'([^']+)'|([\w ]+))\s*,\s*"
        rf"(?:(NOT)\s*\(\s*ISBLANK\(\s*{_COL_REF}\s*\)\s*\)|(NOT)\s+ISBLANK\(\s*{_COL_REF}\s*\)|ISBLANK\(\s*{_COL_REF}\s*\))"
        rf"\s*\)\s*\)",
        e,
        re.IGNORECASE,
    )
    if m:
        base = m.group(1).strip()
        is_not = bool(m.group(4) or m.group(6))
        filt_col = (m.group(5) or m.group(7) or m.group(8) or "").strip()
        filt_expr = "-NULL" if is_not else "NULL"
        return MeasurePlan(
            strategy="filtered_measure",
            lookml_type="number",
            depends_on=[base],
            filters=[(_lookml_ref(filt_col), filt_expr)],
            notes=[
                f"CALCULATE([{base}], FILTER(..., {'NOT ' if is_not else ''}ISBLANK([{filt_col}]))).",
                "Looker best practice: do not filter a type: number measure. "
                f"Create a filtered aggregate that replaces [{base}] under this filter "
                f"(filters: [{_lookml_ref(filt_col)}: \"{filt_expr}\"]), then reference it.",
                f"DEPENDS ON: {base} — implement [{base}] first or replace with filtered aggregate.",
                "Ref: https://cloud.google.com/looker/docs/reference/param-field-filters",
            ],
            mapped=False,
        )

    return None


def topological_measure_order(measures: list[dict], known: set[str] | None = None) -> list[dict]:
    """Order measures so dependencies come before dependents (stable Kahn sort)."""
    names = [(m.get("measure_name") or m.get("name") or "") for m in measures]
    known_set = known or {n for n in names if n}
    plans = {
        (m.get("measure_name") or m.get("name") or ""): classify_dax(
            m.get("expression") or "",
            m.get("measure_name") or m.get("name") or "",
            known_set,
        )
        for m in measures
    }
    name_to_m = {(m.get("measure_name") or m.get("name") or ""): m for m in measures}
    indeg: dict[str, int] = {n: 0 for n in name_to_m}
    edges: dict[str, list[str]] = {n: [] for n in name_to_m}
    for n, plan in plans.items():
        for d in plan.depends_on:
            if d in name_to_m and d != n:
                edges[d].append(n)
                indeg[n] += 1
    queue = [n for n, d in indeg.items() if d == 0]
    # Preserve original relative order for zero-indegree
    order_index = {n: i for i, n in enumerate(names)}
    queue.sort(key=lambda x: order_index.get(x, 0))
    out: list[str] = []
    while queue:
        n = queue.pop(0)
        out.append(n)
        for nxt in edges[n]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
                queue.sort(key=lambda x: order_index.get(x, 0))
    # Cycles / leftovers
    for n in names:
        if n not in out:
            out.append(n)
    return [name_to_m[n] for n in out if n in name_to_m]
