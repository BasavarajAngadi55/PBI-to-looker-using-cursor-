#!/usr/bin/env python3
"""Phase 2 — generate LOOKML_MAPPING_ASSESSMENT.md only (no LookML/SQL)."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = Path(__file__).resolve().parent
OUT = ROOT / "LOOKML_MAPPING_ASSESSMENT.md"

a1 = json.loads((INV / "01_tables_columns.json").read_text())
a2 = json.loads((INV / "03_relationships.json").read_text())
a3 = json.loads((INV / "02_dax_objects.json").read_text())
a4 = json.loads((INV / "04_power_query_m.json").read_text())
a5 = json.loads((INV / "05_tmschema_extras.json").read_text())
gate = json.loads((INV / "COMPLETENESS_GATE.json").read_text())

COMPLEX_RE = re.compile(
    r"CALCULATE|FILTER|ALL(?:EXCEPT)?|REMOVEFILTERS|SAMEPERIODLASTYEAR|DATEADD|"
    r"TOTALYTD|DATESYTD|RANKX|SUMX|AVERAGEX|USERELATIONSHIP|SELECTEDVALUE|VALUES|"
    r"PARALLELPERIOD|ALLEXCEPT",
    re.I,
)

# TM DataType enum-ish map (common Tabular)
TM_TYPE = {
    1: "string",
    2: "int64",
    3: "float64",
    4: "boolean",
    5: "decimal",
    6: "date",
    7: "currency",
    8: "datetime",
    9: "binary",
}


def esc(s):
    if s is None:
        return ""
    return str(s).replace("|", "\\|").replace("\n", "<br>")


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for r in rows:
        cells = [esc(c) for c in r]
        while len(cells) < len(headers):
            cells.append("")
        lines.append("| " + " | ".join(cells[: len(headers)]) + " |")
    return "\n".join(lines)


def is_internal(name: str) -> bool:
    n = name or ""
    return n.startswith("LocalDateTable_") or n.startswith("DateTableTemplate_")


def lookml_dtype(pandas_or_tm) -> str:
    if isinstance(pandas_or_tm, int):
        pandas_or_tm = TM_TYPE.get(pandas_or_tm, str(pandas_or_tm))
    s = str(pandas_or_tm or "").lower()
    if any(x in s for x in ("date", "datetime", "timestamp")):
        if "time" in s and "date" in s:
            return "date_time"
        return "date"
    if any(x in s for x in ("int", "float", "double", "decimal", "number", "currency")):
        return "number"
    if "bool" in s:
        return "yesno"
    return "string"


def map_cardinality(c):
    c = (c or "").upper().replace(" ", "")
    if c in ("M:1", "MANY_TO_ONE", "MANYTOONE"):
        return "many_to_one"
    if c in ("1:M", "ONE_TO_MANY", "ONETOMANY"):
        return "one_to_many"
    if c in ("1:1", "ONE_TO_ONE", "ONETOONE"):
        return "one_to_one"
    if c in ("M:M", "*:*", "MANY_TO_MANY"):
        return "many_to_many"
    return c or "Not available in source extraction"


def measure_suggestion(name, expr, complexity):
    e = (expr or "").upper()
    e_nospace = e.replace(" ", "")
    if "SAMEPERIODLASTYEAR" in e:
        return (
            "COMPLEX",
            "Uses SAMEPERIODLASTYEAR and requires date-filter context validation.",
            "Review LookML time-based / PoP implementation and validate against Power BI KPI results.",
            "Blocks YoY and SPLY-dependent KPIs until implemented.",
        )
    if "ALL(GENDER" in e_nospace or "ALL(ETHNICITY" in e_nospace:
        return (
            "COMPLEX",
            "Uses ALL() to ignore Gender/Ethnicity filter context (TO % Norm pattern).",
            "Implement via filtered measure / explore that ignores those dimensions; parity-test vs Power BI.",
            "Blocks TO % Norm and TO % Var.",
        )
    if "PERIODNUMBER" in e and "MAX" in e:
        return (
            "COMPLEX",
            "EmpCount uses FILTER(ALL(PeriodNumber), PeriodNumber = MAX(...)) latest-period pattern.",
            "Use always_filter / liquid / SQL max-period filter; do not treat as plain COUNT.",
            "Affects EmpCount, EmpCount SPLY, and Actives if Actives wraps EmpCount.",
        )
    if name == "AVG Tenure Months":
        return (
            "PARTIAL",
            "Derived from another measure with ROUND arithmetic.",
            "Implement as type:number referencing base average measure; confirm rounding parity.",
            "Tenure months KPI.",
        )
    if any(x in name for x in ("YoY Var", "YoY %", "Sep%ofSMLY", "BadHire%ofActiveSPLY", "TO % Var")):
        return (
            "PARTIAL",
            "Arithmetic on parent measures that include blocked SPLY/Norm parents.",
            "Keep formula ready; light up only after parent SPLY/Norm measures work.",
            "Dependent KPI until parents resolve.",
        )
    if "DIVIDE" in e:
        return (
            "DIRECT",
            "Ratio of existing measures; maps to SAFE_DIVIDE pattern in LookML.",
            "Implement as type:number with SAFE_DIVIDE; format as percent.",
            "Ratio KPI.",
        )
    if "SUM(" in e or name.startswith("Sum of") or name == "New Hires":
        return (
            "DIRECT",
            "Additive sum over a column/flag.",
            "Implement as type:sum on the corresponding dimension/flag.",
            "Core volume KPI.",
        )
    if "AVERAGE" in e or name.startswith("AVG"):
        return (
            "DIRECT",
            "Average aggregation.",
            "Implement as type:average (apply ROUND in SQL/LookML if needed).",
            "Average KPI.",
        )
    if "COUNT" in e or name.startswith("Count of") or name == "EmpCount":
        status = "PARTIAL" if "FILTER" in e else "DIRECT"
        return (
            status,
            "Count / distinct-count style measure."
            + (" Extra FILTER context present." if "FILTER" in e else ""),
            "Prefer count_distinct on EmplID where business grain requires uniqueness; validate filters.",
            "Headcount-style KPI.",
        )
    if "CALCULATE" in e and "ISBLANK" in e_nospace:
        return (
            "PARTIAL",
            "CALCULATE with TermDate blank/not blank filter — maps to filtered measure.",
            "Implement with filters on yesno TermDate dimension; confirm Actives vs EmpCount nesting.",
            "Actives/Seps KPIs.",
        )
    if complexity == "COMPLEX":
        return (
            "COMPLEX",
            "Complex DAX patterns detected.",
            "Design LookML carefully; parity-test before claiming equivalence.",
            "Complex KPI.",
        )
    if complexity == "MODERATE":
        return (
            "PARTIAL",
            "Moderate DAX — possible with filters or derived measures.",
            "Implement with filtered measures / derived number measures; validate.",
            "Moderate KPI.",
        )
    return (
        "DIRECT",
        "Straightforward aggregation pattern.",
        "Map to standard LookML measure type in next phase.",
        "Standard KPI.",
    )


def suggested_measure_type(name, expr):
    e = (expr or "").upper()
    n = name or ""
    if "SAMEPERIODLASTYEAR" in e or ("ALL(" in e and "NORM" in n.upper()):
        return "number"
    if "DIVIDE" in e or "YoY" in n or "%" in n or "TO %" in n:
        return "number"
    if "AVERAGE" in e or n.startswith("AVG"):
        return "average"
    if "SUM(" in e or n.startswith("Sum of") or n == "New Hires":
        return "sum"
    if "COUNT" in e or n.startswith("Count of") or "EmpCount" in n:
        return "count_distinct"
    if "CALCULATE" in e and ("SEPS" in n.upper() or "ACTIVES" in n.upper()):
        return "count_distinct"
    return "number"


def count_status(rows, idx):
    return Counter(r[idx] for r in rows)


def bucket(counter):
    direct = counter.get("DIRECT", 0)
    partial = counter.get("PARTIAL", 0)
    complex_ = counter.get("COMPLEX", 0)
    wh = counter.get("WAREHOUSE_REQUIRED", 0)
    skip = counter.get("SKIP_INTERNAL", 0) + counter.get("NONE_IN_SOURCE", 0)
    blocked = counter.get("BLOCKED", 0)
    return direct, partial, complex_, wh, skip, blocked


def sumrow(total, counter):
    d, p, c, w, s, b = bucket(counter)
    return [total, d, p, c, w, s, b]


def main():
    sec1_rows = []
    for t in a1["tables"]:
        name = t["table_name"]
        internal = t.get("is_internal") or is_internal(name)
        business = "Internal" if internal else ("Business" if t.get("is_business") else "Other")
        if internal:
            view_type, status = "Internal/Skip", "SKIP_INTERNAL"
            comments = "Power BI auto date/time intelligence table; captured for completeness."
            suggestion = "Do not create a business LookML view; use the business Date view + dimension_group for time."
        elif name == "Employee":
            view_type, status = "Fact", "DIRECT"
            comments = "Primary fact: monthly employee snapshot grain (EmplID x date)."
            suggestion = "Create lookml view employee; point sql_table_name at warehouse hr.employee after M load."
        elif name == "Date":
            view_type, status = "Date", "DIRECT"
            comments = "Business calendar / period dimension used by time intelligence and EmpCount."
            suggestion = "Create date view with calendar dimension_group; expose PeriodNumber for EmpCount logic."
        elif name in ("AgeGroup", "BU", "Ethnicity", "FP", "Gender", "PayType", "SeparationReason"):
            view_type, status = "Dimension", "DIRECT"
            comments = f"Dimension table joining to Employee for {name} attributes."
            suggestion = "Create dim view; seeds vs SQL per M tags in Section 7."
        else:
            view_type, status = "Dimension", "PARTIAL"
            comments = "Table present in extraction."
            suggestion = "Confirm role in next phase."
        sec1_rows.append(
            [name, t.get("table_type"), business, "view", view_type, status, comments, suggestion]
        )

    sec2_rows = []
    for c in a1["columns"]:
        tname = c["table_name"]
        cn = c["column_name"]
        raw_type = c.get("data_type")
        if isinstance(raw_type, int):
            type_disp = f"{raw_type} ({TM_TYPE.get(raw_type, 'unknown')})"
        else:
            type_disp = raw_type or c.get("pandas_dtype") or "Not available in source extraction"
        if is_internal(tname):
            status = "SKIP_INTERNAL"
            comments = "Column on internal auto date table."
            suggestion = "Skip direct migration; covered under auto date section."
        elif c.get("is_calculated_column"):
            status = "PARTIAL"
            comments = "Calculated column — see Section 4 for DAX mapping."
            suggestion = "Prefer warehouse materialization or LookML dimension SQL; do not invent logic."
        else:
            status = "DIRECT"
            comments = "Source/business column maps to LookML dimension."
            suggestion = "Map name/type; preserve labels; honor hidden/key if present."
        lk_type = lookml_dtype(c.get("pandas_dtype") or c.get("data_type"))
        if cn.lower() in ("date", "hiredate", "termdate", "monthstartdate", "monthenddate") or "date" in cn.lower():
            if lk_type == "string":
                lk_type = "date"
        sec2_rows.append(
            [
                tname,
                cn,
                type_disp,
                "Yes" if c.get("is_calculated_column") else "No",
                "dimension",
                lk_type,
                status,
                comments,
                suggestion,
            ]
        )

    sec3_rows = []
    complex_objects = []
    for m in a3["measures"]:
        status, comments, suggestion, kpi = measure_suggestion(
            m["measure_name"], m["expression"], m.get("complexity")
        )
        sec3_rows.append(
            [
                m["table"],
                m["measure_name"],
                m["expression"],
                "measure",
                suggested_measure_type(m["measure_name"], m["expression"]),
                status,
                m.get("complexity"),
                comments,
                suggestion,
                kpi,
            ]
        )
        if status == "COMPLEX" or m["measure_name"] in (
            "New Hires SPLY",
            "Actives SPLY",
            "Seps SPLY",
            "Bad Hires SPLY",
            "EmpCount SPLY",
            "TO % Norm",
            "EmpCount",
        ):
            complex_objects.append(
                (
                    "measure",
                    m["table"],
                    m["measure_name"],
                    status if status != "DIRECT" else "COMPLEX",
                    comments,
                    "Date / filter context / parent measures",
                    suggestion,
                    kpi,
                    "HIGH",
                )
            )

    sec4_rows = []
    for c in a3["calculated_columns"]:
        expr = c.get("expression") or ""
        complexity = c.get("complexity") or "SIMPLE"
        tname = c["table"]
        cname = c["column_name"]
        if is_internal(tname):
            obj, status = "no direct equivalent", "SKIP_INTERNAL"
            comments = "Calculated column on auto date table."
            suggestion = "Skip; use business Date model."
            dep = "Auto date table"
        elif cname == "MonthIncrementNumber":
            obj, status = "warehouse calculation", "WAREHOUSE_REQUIRED"
            comments = "Uses model-wide MIN(Year) pattern — awkward as pure LookML."
            suggestion = "Materialize in warehouse Date table."
            dep = "Date.m / Date table"
        elif cname == "Region" and tname == "BU":
            obj, status = "dimension", "DIRECT"
            comments = "MID/SUBSTR of RegionSeq — simple string derivation."
            suggestion = "LookML SUBSTR or warehouse column Region."
            dep = "BU.m"
        elif "RELATED" in expr.upper() or "LOOKUPVALUE" in expr.upper():
            obj, status = "warehouse calculation", "WAREHOUSE_REQUIRED"
            comments = "Cross-table DAX; better as warehouse SQL join/calc."
            suggestion = "Implement in warehouse SQL before LookML dimension."
            dep = "Related dim tables + M load"
        elif COMPLEX_RE.search(expr) and any(x in expr.upper() for x in ("CALCULATE", "FILTER", "ALL(")):
            obj, status = "warehouse calculation", "COMPLEX"
            comments = "Filter-context sensitive calculated column."
            suggestion = "Prefer warehouse materialization; avoid filter-context DAX in LookML."
            dep = "Warehouse + source columns"
        else:
            obj = "dimension"
            status = "PARTIAL" if complexity != "SIMPLE" else "DIRECT"
            comments = "Row-level calculated column; can be LookML dimension SQL or warehouse column."
            suggestion = "Prefer warehouse column for large Employee; LookML CASE acceptable for prototypes."
            dep = f"{tname} table / M query"
        sec4_rows.append([tname, cname, expr, obj, status, complexity, comments, suggestion, dep])
        if status in ("COMPLEX", "WAREHOUSE_REQUIRED"):
            complex_objects.append(
                (
                    "calculated_column",
                    tname,
                    cname,
                    status,
                    comments,
                    dep,
                    suggestion,
                    "Feeds measures that reference this column",
                    "HIGH" if tname == "Employee" else "MEDIUM",
                )
            )

    sec5_rows = []
    for t in a3["calculated_tables"]:
        name = t["table_name"]
        if is_internal(name):
            rec, status = "no direct equivalent", "SKIP_INTERNAL"
            comments = "Power BI auto-generated date table (Calendar DAX)."
            suggestion = "Skip LookML view; rely on business Date + Looker timeframes."
            dep = "Power BI time intelligence"
        else:
            rec, status = "warehouse table", "WAREHOUSE_REQUIRED"
            comments = "Calculated table outside auto-date pattern."
            suggestion = "Materialize via warehouse SQL or PDT in a later phase."
            dep = "DAX expression"
        sec5_rows.append([name, t["expression"], rec, status, comments, suggestion, dep])

    sec6_rows = []
    for r in a2["relationships"]:
        lk_rel = map_cardinality(r.get("cardinality"))
        cross = r.get("cross_filter") or ""
        active = r.get("active")
        status = "DIRECT"
        comments = "M:1 single-direction relationship — standard Looker left_outer many_to_one from fact."
        suggestion = "Declare join on explore employee; sql_on fact.dim_key = dim.pk."
        if str(cross).lower() in ("both", "bidirectional"):
            status = "PARTIAL"
            comments = "Bidirectional cross-filter has no 1:1 Looker join equivalent."
            suggestion = "Model primary many_to_one; use careful explore design if needed."
        if not active:
            status = "PARTIAL"
            comments = "Inactive relationship — USERELATIONSHIP may activate in DAX."
            suggestion = "Do not join by default; document for measures that need alternate paths."
        if lk_rel == "many_to_many":
            status = "COMPLEX"
            comments = "Many-to-many — needs bridge or fanout control."
            suggestion = "Introduce bridge table or carefully scoped joins."
        sec6_rows.append(
            [
                r["from_table"],
                r["from_column"],
                r["to_table"],
                r["to_column"],
                r.get("cardinality"),
                cross,
                active,
                "left_outer join on explore",
                lk_rel,
                status,
                comments,
                suggestion,
            ]
        )

    sec7_rows = []
    for q in a4["queries"]:
        name = q["query_name"]
        tags = q.get("tags") or []
        src = q.get("source_type")
        ttype = ", ".join(tags)
        refs = ", ".join(q.get("referenced_queries") or []) or "None"
        if q.get("is_embedded_static"):
            dest, status = "Warehouse Seed", "WAREHOUSE_REQUIRED"
            comments = "Embedded/static M (Table.FromRows / decompress) — not SQL Server."
            suggestion = "Load as seed/CSV/INSERT in warehouse; then LookML view."
            impact = f"Dim {name} labels/joins"
        elif name == "Employee":
            dest, status = "Warehouse SQL", "WAREHOUSE_REQUIRED"
            comments = "Complex SQL + UNION actives/seps + transforms; largest ETL dependency."
            suggestion = "Port M SQL to warehouse view/table before any HR KPI LookML is runnable."
            impact = "ALL Employee measures / KPIs"
            complex_objects.append(
                (
                    "power_query",
                    "Employee",
                    "Employee.m",
                    "WAREHOUSE_REQUIRED",
                    comments,
                    "inventory/04_m_raw/Employee.m",
                    suggestion,
                    impact,
                    "HIGH",
                )
            )
        elif src == "sql_database" or q.get("has_sql"):
            dest, status = "Warehouse SQL", "WAREHOUSE_REQUIRED"
            comments = "M reads SQL Database; must be reproduced or replaced by warehouse extract."
            suggestion = f"Create warehouse object from inventory/04_m_raw/{name}.m SQL."
            impact = f"Table {name} and joining measures"
        else:
            dest, status = "Review Required", "PARTIAL"
            comments = "Review M source classification."
            suggestion = "Inspect .m file and choose seed vs SQL."
            impact = name
        sec7_rows.append([name, src, ttype, refs, dest, status, comments, suggestion, impact])

    sec8_rows = []
    for h in a5.get("hierarchies") or []:
        levels = " > ".join(
            f"{lv.get('level_name')}({lv.get('column_name')})" for lv in (h.get("levels") or [])
        )
        tname = h.get("table")
        if is_internal(tname or ""):
            approach, status = "no direct equivalent", "SKIP_INTERNAL"
            comments = "Hierarchy on auto date table."
            suggestion = "Use Looker timeframes on business date instead."
        else:
            approach, status = "drill_fields / related dimensions", "PARTIAL"
            comments = "Business hierarchy can be approximated with drill_fields ordered dimensions."
            suggestion = "Define drill_fields on Date (Year > Quarter > Month) matching YQM levels."
        sec8_rows.append(
            [tname, h.get("hierarchy_name"), levels, approach, status, comments, suggestion]
        )

    if a5.get("rls"):
        sec9_table = md_table(
            [
                "Role",
                "Table",
                "Power BI Filter",
                "Recommended Looker Security Object",
                "Mapping Status",
                "Comments",
                "Suggestion",
            ],
            [
                [
                    r.get("role"),
                    r.get("table"),
                    r.get("filter"),
                    "access_grant / sql_always_where",
                    "PARTIAL",
                    "RLS role present",
                    "Map to Looker user attributes",
                ]
                for r in a5["rls"]
            ],
        )
    else:
        sec9_table = md_table(
            ["RLS", "Status", "Comments"],
            [["None", "NONE_IN_SOURCE", "No Power BI RLS roles were identified."]],
        )

    sec10_rows = []
    for p in a5.get("partitions") or []:
        tname = p.get("TableName")
        pname = p.get("Name")
        mode = p.get("Mode")
        src = (p.get("QueryDefinition") or "")[:120] or "Not available in source extraction"
        if is_internal(tname or ""):
            treat, status = "Irrelevant to LookML (internal)", "SKIP_INTERNAL"
            comments = "Partition on auto date / internal table."
            suggestion = "Ignore for LookML; warehouse uses business tables only."
        else:
            treat, status = "Warehouse design consideration", "PARTIAL"
            comments = "Import/partition metadata from Tabular; LookML does not model partitions 1:1."
            suggestion = "Ensure warehouse table refresh covers this source; no LookML partition object."
        sec10_rows.append([tname, pname, src, mode, treat, status, comments, suggestion])

    sec11_rows = []
    if not a5.get("sort_by_columns"):
        sec11_rows.append(
            [
                "—",
                "—",
                "—",
                "NONE_IN_SOURCE",
                "NONE_IN_SOURCE",
                "No Sort By Column metadata extracted.",
                "If needed later, use order_by_field in LookML.",
            ]
        )
    else:
        for s in a5["sort_by_columns"]:
            sec11_rows.append(
                [
                    s.get("table"),
                    s.get("column"),
                    s.get("sort_by"),
                    "order_by_field",
                    "DIRECT",
                    "Sort-by metadata present.",
                    "Set order_by_field on the display dimension.",
                ]
            )

    sec12_rows = []
    for f in a5.get("format_strings") or []:
        sec12_rows.append(
            [
                f.get("table"),
                f.get("column"),
                f.get("format_string"),
                "value_format / value_format_name",
                "PARTIAL",
                "Power BI format string captured on column.",
                "Map to LookML value_format_name where standard; else custom value_format.",
            ]
        )
    if not a5.get("display_folders"):
        sec12_rows.append(
            [
                "—",
                "display_folders",
                "NONE_IN_SOURCE",
                "group_label / view labels",
                "NONE_IN_SOURCE",
                "No display folder entries in extraction.",
                "Optional group_label in next phase.",
            ]
        )
    sec12_rows.append(
        [
            "Employee / BU / Date",
            "measures",
            "Not available in source extraction (format_string null on dax_measures)",
            "value_format_name on measures",
            "BLOCKED",
            "Measure format strings not present in Phase 1 DAX extract.",
            "Infer percent/decimal from measure names in implementation phase; confirm in Power BI UI if needed.",
        ]
    )

    sec13_rows = []
    for ad in a5.get("auto_date_tables") or []:
        cols = ", ".join(c.get("column_name") for c in (ad.get("columns") or []))
        hier = ", ".join(h.get("hierarchy_name") for h in (ad.get("hierarchies") or [])) or "None listed"
        sec13_rows.append(
            [
                ad.get("table_name"),
                cols,
                hier,
                "SKIP_INTERNAL",
                "SKIP_INTERNAL",
                "Power BI auto date table with Calendar(...) DAX; not a business calendar.",
                "Replace auto-date behavior with business Date view + Looker timeframes / PoP.",
            ]
        )

    sec14_rows = []
    if not a5.get("perspectives"):
        sec14_rows.append(
            [
                "perspectives",
                "perspectives",
                "NONE_IN_SOURCE",
                "No LookML equivalent (Explore curation)",
                "NONE_IN_SOURCE",
                "No perspectives in PBIX.",
                "Optionally hide explores/fields manually.",
            ]
        )
    if not a5.get("rls"):
        sec14_rows.append(
            [
                "rls",
                "security",
                "NONE_IN_SOURCE",
                "access_grant / sql_always_where",
                "NONE_IN_SOURCE",
                "No RLS roles.",
                "No security mapping required from PBIX.",
            ]
        )
    if not a5.get("ols"):
        sec14_rows.append(
            [
                "ols",
                "security",
                "NONE_IN_SOURCE",
                "field-level access_grant",
                "NONE_IN_SOURCE",
                "No OLS.",
                "N/A",
            ]
        )
    sec14_rows.append(
        [
            "model annotations",
            "annotations",
            f"{len(a5.get('annotations') or [])} annotation records in 05_tmschema_extras.json",
            "Not available in source extraction as LookML 1:1",
            "PARTIAL",
            "Large annotation set captured in Phase 1 JSON; mostly Power BI internal tags.",
            "Review annotations JSON only if a specific business tag is needed; do not auto-migrate all.",
        ]
    )
    for meta in a5.get("metadata") or []:
        sec14_rows.append(
            [
                meta.get("Name"),
                "metadata",
                meta.get("Value"),
                "No direct equivalent",
                "PARTIAL",
                "PBIX metadata key/value.",
                "Informational only for Looker.",
            ]
        )
    if a5.get("model"):
        m0 = a5["model"][0] if isinstance(a5["model"], list) and a5["model"] else a5["model"]
        sec14_rows.append(
            [
                "tmschema_model",
                "model",
                f"Name={m0.get('Name')}; Culture={m0.get('Culture')}; DefaultMode={m0.get('DefaultMode')}",
                "model connection / project settings",
                "PARTIAL",
                "Tabular model header metadata.",
                "Set Looker connection separately; culture may affect formats.",
            ]
        )
    if a5.get("variations"):
        sec14_rows.append(
            [
                "variations",
                "variations",
                f"{len(a5['variations'])} records",
                "No direct equivalent",
                "PARTIAL",
                "Field variations captured in TM extras.",
                "Usually skip unless UI field variations matter.",
            ]
        )
    else:
        sec14_rows.append(
            [
                "variations",
                "variations",
                "NONE_IN_SOURCE",
                "N/A",
                "NONE_IN_SOURCE",
                "No variations listed.",
                "N/A",
            ]
        )

    seen = set()
    sec15_rows = []
    for row in complex_objects:
        key = (row[0], row[1], row[2])
        if key in seen:
            continue
        seen.add(key)
        sec15_rows.append(list(row))

    c1 = count_status(sec1_rows, 5)
    c2 = count_status(sec2_rows, 6)
    c3 = count_status(sec3_rows, 5)
    c4 = count_status(sec4_rows, 4)
    c5 = count_status(sec5_rows, 3)
    c6 = count_status(sec6_rows, 9)
    c7 = count_status(sec7_rows, 5)
    c8 = count_status(sec8_rows, 4)

    sum_rows = [
        ["Tables"] + sumrow(len(sec1_rows), c1),
        ["Columns"] + sumrow(len(sec2_rows), c2),
        ["Measures"] + sumrow(len(sec3_rows), c3),
        ["Calculated Columns"] + sumrow(len(sec4_rows), c4),
        ["Calculated Tables"] + sumrow(len(sec5_rows), c5),
        ["Relationships"] + sumrow(len(sec6_rows), c6),
        ["Power Query"] + sumrow(len(sec7_rows), c7),
        ["Hierarchies"] + sumrow(len(sec8_rows), c8),
        ["RLS", 0, 0, 0, 0, 0, 1, 0],
    ]

    lines = []
    lines.append("# LOOKML Mapping Assessment — Phase 2")
    lines.append("")
    lines.append("**Phase:** 2 — Power BI → LookML mapping assessment only")
    lines.append(f"**Source inventory gate:** `{gate.get('status')}`")
    lines.append(
        "**Rule:** Analysis and mapping only. No LookML, warehouse SQL, PDTs, or report migration in this phase."
    )
    lines.append("")
    lines.append(
        "Inputs used: `inventory/01_tables_columns.json`, `02_dax_objects.json`, `03_relationships.json`, "
        "`04_power_query_m.json`, `05_tmschema_extras.json`, `04_m_raw/*.m`, `OBJECT_INVENTORY.md`, "
        "`ACTION_MATRIX.csv`, `COMPLETENESS_GATE.json`."
    )
    lines.append("")

    def add_sec(title, headers, rows):
        lines.append(f"## {title}")
        lines.append("")
        lines.append(md_table(headers, rows))
        lines.append("")

    add_sec(
        "Section 1 — Tables → LookML Views",
        [
            "Power BI Table",
            "Table Type",
            "Business/Internal",
            "Recommended LookML Object",
            "Suggested View Type",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec1_rows,
    )
    add_sec(
        "Section 2 — Columns → LookML Dimensions",
        [
            "Power BI Table",
            "Power BI Column",
            "Data Type",
            "Calculated?",
            "Recommended LookML Object",
            "LookML Type",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec2_rows,
    )
    add_sec(
        "Section 3 — Measures → LookML Measures",
        [
            "Table",
            "Measure",
            "Original DAX",
            "Recommended LookML Object",
            "Suggested Measure Type",
            "Mapping Status",
            "Complexity",
            "Comments",
            "Suggestion",
            "KPI Impact",
        ],
        sec3_rows,
    )
    add_sec(
        "Section 4 — Calculated Columns → LookML Dimensions / Other",
        [
            "Table",
            "Calculated Column",
            "Original DAX",
            "Recommended LookML Object",
            "Mapping Status",
            "Complexity",
            "Comments",
            "Suggestion",
            "Dependency",
        ],
        sec4_rows,
    )
    add_sec(
        "Section 5 — Calculated Tables",
        [
            "Power BI Table",
            "Original DAX",
            "Recommended LookML Representation",
            "Mapping Status",
            "Comments",
            "Suggestion",
            "Dependency",
        ],
        sec5_rows,
    )
    add_sec(
        "Section 6 — Relationships → LookML Joins",
        [
            "From Table",
            "From Column",
            "To Table",
            "To Column",
            "Power BI Cardinality",
            "Cross Filter",
            "Active",
            "Recommended LookML Join",
            "LookML Relationship",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec6_rows,
    )
    add_sec(
        "Section 7 — Power Query / M → Looker Data Layer",
        [
            "Power Query",
            "Source",
            "Transformation Type",
            "Referenced Queries",
            "Recommended Destination",
            "Mapping Status",
            "Comments",
            "Suggestion",
            "Impacted Tables/KPIs",
        ],
        sec7_rows,
    )
    add_sec(
        "Section 8 — Hierarchies",
        [
            "Table",
            "Hierarchy",
            "Levels",
            "Recommended LookML Approach",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec8_rows,
    )

    lines.append("## Section 9 — RLS / Security")
    lines.append("")
    lines.append(sec9_table)
    lines.append("")

    add_sec(
        "Section 10 — Partitions",
        [
            "Table",
            "Partition",
            "Source",
            "Mode",
            "Recommended LookML / Warehouse Treatment",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec10_rows,
    )
    add_sec(
        "Section 11 — Sort-By Columns",
        [
            "Table",
            "Column",
            "Sort By Column",
            "Recommended LookML Approach",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec11_rows,
    )
    add_sec(
        "Section 12 — Formatting / Display Metadata",
        [
            "Table",
            "Object",
            "Power BI Format",
            "Recommended LookML Formatting",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec12_rows,
    )
    add_sec(
        "Section 13 — Auto Date Tables",
        [
            "Internal Table",
            "Columns",
            "Hierarchy",
            "Recommended LookML Treatment",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec13_rows,
    )
    add_sec(
        "Section 14 — Annotations / Other Tabular Metadata",
        [
            "Object",
            "Metadata Type",
            "Power BI Value",
            "LookML Equivalent",
            "Mapping Status",
            "Comments",
            "Suggestion",
        ],
        sec14_rows,
    )
    add_sec(
        "Section 15 — Complex / Unmapped Objects",
        [
            "Object Type",
            "Table",
            "Object",
            "Mapping Status",
            "Why Direct Mapping Is Difficult",
            "Dependency",
            "Recommended Approach",
            "KPI Impact",
            "Priority",
        ],
        sec15_rows,
    )
    add_sec(
        "Section 16 — Overall Object Mapping Summary",
        [
            "Power BI Object Type",
            "Total",
            "Direct Mapping",
            "Partial",
            "Complex",
            "Warehouse Required",
            "Skip Internal",
            "Blocked",
        ],
        sum_rows,
    )

    lines.append(
        f"_Totals derived from Phase 1 extraction (gate `{gate.get('status')}`): "
        f"tables={gate['counts']['tables']}, columns={gate['counts']['columns']}, "
        f"measures={gate['counts']['measures']}, calculated_columns={gate['counts']['calculated_columns']}, "
        f"calculated_tables={gate['counts']['calculated_tables']}, relationships={gate['counts']['relationships']}, "
        f"power_query={gate['counts']['power_query']}, hierarchies={gate['counts']['hierarchies']}, "
        f"partitions={gate['counts']['partitions']}, rls_roles={gate['counts']['rls_roles']}._"
    )
    lines.append("")
    lines.append("## Mapping Status Definitions (reference)")
    lines.append("")
    lines.append("| Status | Meaning |")
    lines.append("| --- | --- |")
    lines.append("| DIRECT | Clear one-to-one conceptual mapping |")
    lines.append("| PARTIAL | Representable in LookML with extra design/validation |")
    lines.append("| COMPLEX | Not safe as a simple LookML object |")
    lines.append("| WAREHOUSE_REQUIRED | Prefer warehouse before LookML |")
    lines.append("| SKIP_INTERNAL | Captured PBI internal; normally not migrated |")
    lines.append("| BLOCKED | Required information missing from extraction |")
    lines.append("| NONE_IN_SOURCE / NO_DIRECT_EQUIVALENT | Empty category or no LookML equivalent |")
    lines.append("")
    lines.append("# Next Phase")
    lines.append("")
    lines.append("This document is the **design/mapping layer only**.")
    lines.append("")
    lines.append("The next phase will use this assessment to generate:")
    lines.append("")
    lines.append("1. Warehouse SQL where required")
    lines.append("2. LookML views")
    lines.append("3. LookML measures")
    lines.append("4. LookML joins")
    lines.append("5. LookML model/explore")
    lines.append("6. Security implementation")
    lines.append("7. KPI parity testing")
    lines.append("")
    lines.append("Those tasks are **not** performed in Phase 2.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")

    assert len(sec1_rows) == gate["counts"]["tables"]
    assert len(sec2_rows) == gate["counts"]["columns"]
    assert len(sec3_rows) == gate["counts"]["measures"]
    assert len(sec4_rows) == gate["counts"]["calculated_columns"]
    assert len(sec5_rows) == gate["counts"]["calculated_tables"]
    assert len(sec6_rows) == gate["counts"]["relationships"]
    assert len(sec7_rows) == gate["counts"]["power_query"]
    assert len(sec8_rows) == gate["counts"]["hierarchies"]
    assert len(sec10_rows) == gate["counts"]["partitions"]
    assert len(sec13_rows) == gate["counts"]["auto_date_tables"]
    print("VALIDATION OK")


if __name__ == "__main__":
    main()
