#!/usr/bin/env python3
"""Complete Power BI semantic-model object capture → inventory/ + ACTION_MATRIX."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd
from pbixray import PBIXRay

PBIX = Path("/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix")
OUT = Path("/Users/Basavaraj_Angadi/Desktop/data eng /inventory")
M_RAW = OUT / "04_m_raw"

BUSINESS_TABLES = {
    "AgeGroup",
    "BU",
    "Date",
    "Employee",
    "Ethnicity",
    "FP",
    "Gender",
    "PayType",
    "SeparationReason",
}

COMPLEX_DAX_PATTERNS = (
    "SAMEPERIODLASTYEAR",
    "DATESYTD",
    "TOTALYTD",
    "PARALLELPERIOD",
    "DATEADD",
    "FILTER(ALL(",
    "ALLSELECTED",
    "REMOVEFILTERS",
    "PATH(",
)


def df_to_records(df) -> list:
    if df is None:
        return []
    if isinstance(df, pd.DataFrame):
        if df.empty:
            return []
        return json.loads(df.to_json(orient="records", date_format="iso"))
    return []


def safe_attr_df(pbix, name: str):
    try:
        val = getattr(pbix, name, None)
    except Exception as e:
        return None, str(e)
    if val is None:
        return None, None
    if isinstance(val, pd.DataFrame):
        return val, None
    return None, f"non-dataframe:{type(val).__name__}"


def classify_m(expression: str) -> dict:
    expr = expression or ""
    tags = []
    if "Sql.Database" in expr or "Sql.Databases" in expr:
        tags.append("sql_database")
    if "Table.FromRows" in expr or "Binary.Decompress" in expr:
        tags.append("embedded_seed")
    if "Excel.Workbook" in expr or "Csv.Document" in expr:
        tags.append("file_source")
    if "Table.NestedJoin" in expr or "Table.Join" in expr or "JoinKind" in expr:
        tags.append("join")
    if "Table.Combine" in expr or "union all" in expr.lower():
        tags.append("union_combine")
    if len(expr) > 1500 or expr.count("\n") > 25:
        tags.append("complex")
    if not tags:
        tags.append("simple_transform")
    # extract SQL if present
    sql_matches = re.findall(r'Query\s*=\s*"((?:[^"\\]|\\.)*)"', expr, re.S)
    sqls = [s.replace("#(lf)", "\n").replace('\\"', '"') for s in sql_matches]
    complexity = "high" if "complex" in tags or "sql_database" in tags else (
        "medium" if "join" in tags or "union_combine" in tags else "low"
    )
    action = "DBT_SQL" if "sql_database" in tags or "complex" in tags else (
        "DBT_SEED" if "embedded_seed" in tags else "DBT_SQL"
    )
    return {
        "tags": tags,
        "complexity": complexity,
        "suggested_action": action,
        "embedded_sql": sqls,
    }


def classify_measure(name: str, expression: str) -> str:
    expr = expression or ""
    if any(p in expr for p in COMPLEX_DAX_PATTERNS):
        return "LOOKML_TODO_COMPLEX"
    if "SAMEPERIODLASTYEAR" in expr:
        return "LOOKML_TODO_COMPLEX"
    # EmpCount max period pattern
    if "PeriodNumber" in expr and "MAX(" in expr:
        return "LOOKML_TODO_COMPLEX"
    if "ALL(" in expr and ("Gender" in expr or "Ethnicity" in expr):
        return "LOOKML_TODO_COMPLEX"
    # references to SPLY measures in expression
    if "SPLY" in expr or "SPLY" in name:
        if "SAMEPERIODLASTYEAR" in expr or name.endswith("SPLY") or " SPLY" in name:
            return "LOOKML_TODO_COMPLEX"
    return "LOOKML_MEASURE"


def is_auto_date_table(name: str) -> bool:
    return name.startswith("LocalDateTable_") or name.startswith("DateTableTemplate_")


def dump_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def extract_all():
    OUT.mkdir(parents=True, exist_ok=True)
    M_RAW.mkdir(parents=True, exist_ok=True)

    pbix = PBIXRay(str(PBIX))
    errors = []

    # ---------- 01 Schema ----------
    tables = list(pbix.tables)
    schema_df = pbix.schema
    stats_df, stats_err = safe_attr_df(pbix, "statistics")
    if stats_err and stats_df is None and stats_err.startswith("non"):
        pass

    # TM columns if available for richer types / isHidden
    tm_cols_df, _ = safe_attr_df(pbix, "tmschema_columns")
    tm_tables_df, _ = safe_attr_df(pbix, "tmschema_tables")

    columns = []
    for _, row in schema_df.iterrows():
        rec = {
            "table": row["TableName"],
            "column": row["ColumnName"],
            "pandas_dtype": row["PandasDataType"],
            "is_business_table": row["TableName"] in BUSINESS_TABLES,
            "is_auto_date_table": is_auto_date_table(row["TableName"]),
        }
        columns.append(rec)

    # merge stats
    stats_by_key = {}
    if stats_df is not None and not stats_df.empty:
        for _, row in stats_df.iterrows():
            stats_by_key[(row["TableName"], row["ColumnName"])] = {
                "cardinality": row.get("Cardinality"),
                "data_size": row.get("DataSize"),
                "dictionary": row.get("Dictionary"),
                "hash_index": row.get("HashIndex"),
            }
        for c in columns:
            st = stats_by_key.get((c["table"], c["column"]))
            if st:
                c["statistics"] = st

    # TM column enrichment
    tm_col_records = df_to_records(tm_cols_df)
    tm_table_records = df_to_records(tm_tables_df)

    schema_out = {
        "source_pbix": str(PBIX),
        "table_count": len(tables),
        "tables": tables,
        "business_tables": sorted(BUSINESS_TABLES),
        "auto_date_tables": [t for t in tables if is_auto_date_table(t)],
        "column_count": len(columns),
        "columns": columns,
        "tmschema_tables": tm_table_records,
        "tmschema_columns": tm_col_records,
        "statistics": df_to_records(stats_df),
    }
    dump_json(OUT / "01_tables_columns.json", schema_out)

    # ---------- 02 DAX ----------
    measures_df = pbix.dax_measures
    dax_cols_df = pbix.dax_columns
    dax_tables_df = pbix.dax_tables

    measures = []
    for _, row in measures_df.iterrows():
        expr = row["Expression"]
        measures.append(
            {
                "table": row["TableName"],
                "name": row["Name"],
                "expression": expr,
                "display_folder": row.get("DisplayFolder"),
                "description": row.get("Description"),
                "suggested_action": classify_measure(row["Name"], expr),
            }
        )

    calc_columns = []
    for _, row in dax_cols_df.iterrows():
        calc_columns.append(
            {
                "table": row["TableName"],
                "column": row["ColumnName"],
                "expression": row["Expression"],
                "is_auto_date_table": is_auto_date_table(row["TableName"]),
                "suggested_action": (
                    "SKIP_PBI_INTERNAL"
                    if is_auto_date_table(row["TableName"])
                    else "DBT_SQL"
                ),
            }
        )

    calc_tables = []
    for _, row in dax_tables_df.iterrows():
        calc_tables.append(
            {
                "table": row["TableName"],
                "expression": row["Expression"],
                "is_auto_date_table": is_auto_date_table(row["TableName"]),
                "suggested_action": (
                    "SKIP_PBI_INTERNAL"
                    if is_auto_date_table(row["TableName"])
                    else "DBT_SQL"
                ),
            }
        )

    dax_out = {
        "measure_count": len(measures),
        "measures": measures,
        "calculated_column_count": len(calc_columns),
        "calculated_columns": calc_columns,
        "calculated_table_count": len(calc_tables),
        "calculated_tables": calc_tables,
    }
    dump_json(OUT / "02_dax_objects.json", dax_out)

    # ---------- 03 Relationships ----------
    rels_df = pbix.relationships
    relationships = []
    for _, row in rels_df.iterrows():
        relationships.append(
            {
                "from_table": row["FromTableName"],
                "from_column": row["FromColumnName"],
                "to_table": row["ToTableName"],
                "to_column": row["ToColumnName"],
                "is_active": bool(row["IsActive"]),
                "cardinality": row["Cardinality"],
                "cross_filtering_behavior": row["CrossFilteringBehavior"],
                "from_key_count": row.get("FromKeyCount"),
                "to_key_count": row.get("ToKeyCount"),
                "rely_on_referential_integrity": row.get("RelyOnReferentialIntegrity"),
                "suggested_action": "LOOKML_JOIN",
            }
        )
    rel_out = {"relationship_count": len(relationships), "relationships": relationships}
    dump_json(OUT / "03_relationships.json", rel_out)

    # ---------- 04 Power Query M ----------
    pq_df = pbix.power_query
    mashup_df, _ = safe_attr_df(pbix, "mashup_queries")
    m_params_df, _ = safe_attr_df(pbix, "m_parameters")
    data_mashup = None
    try:
        dm = pbix.data_mashup
        if dm is not None and not isinstance(dm, pd.DataFrame):
            data_mashup = str(dm)[:5000]
        elif isinstance(dm, pd.DataFrame):
            data_mashup = df_to_records(dm)
    except Exception as e:
        errors.append(f"data_mashup: {e}")

    m_queries = []
    for _, row in pq_df.iterrows():
        table = row["TableName"]
        expr = row["Expression"]
        meta = classify_m(expr)
        safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", table)
        m_path = M_RAW / f"{safe_name}.m"
        m_path.write_text(expr if expr.endswith("\n") else expr + "\n")
        m_queries.append(
            {
                "table": table,
                "expression": expr,
                "m_file": str(m_path.relative_to(OUT)),
                **meta,
            }
        )

    pq_out = {
        "power_query_count": len(m_queries),
        "queries": m_queries,
        "mashup_queries": df_to_records(mashup_df),
        "m_parameters": df_to_records(m_params_df),
        "data_mashup_preview": data_mashup,
    }
    dump_json(OUT / "04_power_query_m.json", pq_out)

    # ---------- 05 TM extras ----------
    tm_attr_names = [
        "tmschema_partitions",
        "tmschema_datasources",
        "tmschema_hierarchies",
        "tmschema_levels",
        "tmschema_kpis",
        "tmschema_calendars",
        "tmschema_calendar_column_groups",
        "tmschema_calendar_column_refs",
        "tmschema_annotations",
        "tmschema_format_string_definitions",
        "tmschema_perspectives",
        "tmschema_perspective_tables",
        "tmschema_perspective_columns",
        "tmschema_perspective_measures",
        "tmschema_perspective_hierarchies",
        "tmschema_cultures",
        "tmschema_translations",
        "tmschema_calculation_groups",
        "tmschema_calculation_items",
        "tmschema_calculation_expressions",
        "tmschema_functions",
        "tmschema_sets",
        "tmschema_variations",
        "tmschema_attribute_hierarchies",
        "tmschema_extended_properties",
        "tmschema_detail_rows_definitions",
        "tmschema_refresh_policies",
        "tmschema_query_groups",
        "tmschema_binding_info",
        "tmschema_role_memberships",
        "tmschema_column_permissions",
        "tmschema_model",
        "tmschema_linguistic_metadata",
        "aggregations",
        "perspectives",
        "connections",
        "rls",
        "ols",
        "metadata",
    ]

    extras = {"categories": {}, "empty_categories": [], "non_empty_categories": []}
    for name in tm_attr_names:
        try:
            val = getattr(pbix, name, None)
        except Exception as e:
            extras["categories"][name] = {"error": str(e), "records": []}
            extras["empty_categories"].append(name)
            continue
        if isinstance(val, pd.DataFrame):
            recs = df_to_records(val)
            extras["categories"][name] = {"record_count": len(recs), "records": recs}
            if recs:
                extras["non_empty_categories"].append(name)
            else:
                extras["empty_categories"].append(name)
        elif isinstance(val, list):
            extras["categories"][name] = {"record_count": len(val), "records": val}
            if val:
                extras["non_empty_categories"].append(name)
            else:
                extras["empty_categories"].append(name)
        elif val is None:
            extras["categories"][name] = {"record_count": 0, "records": []}
            extras["empty_categories"].append(name)
        else:
            # scalar / other
            try:
                serialized = json.loads(json.dumps(val, default=str))
            except Exception:
                serialized = str(val)
            extras["categories"][name] = {
                "record_count": 1 if serialized not in (None, "", [], {}) else 0,
                "records": [serialized] if serialized not in (None, "", [], {}) else [],
            }
            if extras["categories"][name]["record_count"]:
                extras["non_empty_categories"].append(name)
            else:
                extras["empty_categories"].append(name)

    dump_json(OUT / "05_tmschema_extras.json", extras)

    pbix.close()
    return {
        "tables": tables,
        "schema_out": schema_out,
        "dax_out": dax_out,
        "rel_out": rel_out,
        "pq_out": pq_out,
        "extras": extras,
        "errors": errors,
    }


def merge(bundle: dict) -> None:
    tables = bundle["tables"]
    schema_out = bundle["schema_out"]
    dax_out = bundle["dax_out"]
    rel_out = bundle["rel_out"]
    pq_out = bundle["pq_out"]
    extras = bundle["extras"]

    gate_failures = []

    # Gate 1: table count
    if len(tables) != 15:
        gate_failures.append(f"table_count expected 15 got {len(tables)}")

    # Gate 2: every schema column present (already from schema dump)
    if schema_out["column_count"] < 1:
        gate_failures.append("no columns in schema")

    # Gate 3: 30 measures + calc cols/tables with expressions
    if dax_out["measure_count"] != 30:
        gate_failures.append(f"measure_count expected 30 got {dax_out['measure_count']}")
    for m in dax_out["measures"]:
        if not (m.get("expression") or "").strip():
            gate_failures.append(f"measure missing expression: {m['name']}")
    if dax_out["calculated_column_count"] < 1:
        gate_failures.append("no calculated columns")
    for c in dax_out["calculated_columns"]:
        if not (c.get("expression") or "").strip():
            gate_failures.append(f"calc column missing expression: {c['table']}.{c['column']}")
    if dax_out["calculated_table_count"] != 6:
        gate_failures.append(
            f"calculated_table_count expected 6 got {dax_out['calculated_table_count']}"
        )

    # Gate 4: 8 relationships
    if rel_out["relationship_count"] != 8:
        gate_failures.append(
            f"relationship_count expected 8 got {rel_out['relationship_count']}"
        )

    # Gate 5: 9 PQ queries + .m files
    if pq_out["power_query_count"] != 9:
        gate_failures.append(
            f"power_query_count expected 9 got {pq_out['power_query_count']}"
        )
    m_files = list(M_RAW.glob("*.m"))
    if len(m_files) != 9:
        gate_failures.append(f"m_raw file count expected 9 got {len(m_files)}")

    # Gate 6: empty categories listed
    if "empty_categories" not in extras or "categories" not in extras:
        gate_failures.append("extras missing empty_categories listing")

    # ---------- ACTION MATRIX ----------
    rows = []

    def add_row(**kwargs):
        rows.append(kwargs)

    # Tables
    for t in tables:
        if is_auto_date_table(t):
            action = "SKIP_PBI_INTERNAL"
            obj_type = "auto_date_table"
            notes = "Power BI auto date/time intelligence table"
        elif t == "Employee":
            action = "LOOKML_VIEW_FACT"
            obj_type = "table"
            notes = "Fact / snapshot grain EmplID + date"
        else:
            action = "LOOKML_VIEW_DIM"
            obj_type = "table"
            notes = "Dimension table"
        add_row(
            object_class="table",
            object_type=obj_type,
            parent="",
            name=t,
            action=action,
            expression="",
            notes=notes,
        )

    # Columns (native inventory — every schema column)
    calc_col_keys = {
        (c["table"], c["column"]) for c in dax_out["calculated_columns"]
    }
    for c in schema_out["columns"]:
        key = (c["table"], c["column"])
        if is_auto_date_table(c["table"]):
            action = "SKIP_PBI_INTERNAL"
            notes = "Column on auto date table"
        elif key in calc_col_keys:
            action = "DBT_SQL"
            notes = "Calculated column — materialize in warehouse/dbt; expose in LookML after"
        elif c["table"] == "Employee":
            action = "LOOKML_VIEW_FACT"
            notes = "Fact attribute / key"
        else:
            action = "LOOKML_VIEW_DIM"
            notes = "Dimension attribute / key"
        add_row(
            object_class="column",
            object_type="calculated_column" if key in calc_col_keys else "column",
            parent=c["table"],
            name=c["column"],
            action=action,
            expression="",
            notes=notes,
        )

    # Calc column expressions as separate actionable rows (full expression)
    for c in dax_out["calculated_columns"]:
        add_row(
            object_class="dax_calculated_column",
            object_type="calculated_column",
            parent=c["table"],
            name=c["column"],
            action=c["suggested_action"],
            expression=c["expression"],
            notes="Full DAX calculated column",
        )

    # Calc tables
    for t in dax_out["calculated_tables"]:
        add_row(
            object_class="dax_calculated_table",
            object_type="calculated_table",
            parent="",
            name=t["table"],
            action=t["suggested_action"],
            expression=t["expression"],
            notes="DAX calculated table",
        )

    # Measures
    for m in dax_out["measures"]:
        add_row(
            object_class="measure",
            object_type="dax_measure",
            parent=m["table"],
            name=m["name"],
            action=m["suggested_action"],
            expression=m["expression"],
            notes="Full DAX measure",
        )

    # Relationships
    for r in rel_out["relationships"]:
        add_row(
            object_class="relationship",
            object_type="relationship",
            parent=r["from_table"],
            name=f"{r['from_table']}.{r['from_column']}->{r['to_table']}.{r['to_column']}",
            action="LOOKML_JOIN",
            expression=f"cardinality={r['cardinality']}; cross_filter={r['cross_filtering_behavior']}; active={r['is_active']}",
            notes="Map to explore join",
        )

    # M queries
    for q in pq_out["queries"]:
        add_row(
            object_class="power_query",
            object_type="m_query",
            parent="",
            name=q["table"],
            action=q["suggested_action"],
            expression=q["expression"][:500] + ("…" if len(q["expression"]) > 500 else ""),
            notes=f"complexity={q['complexity']}; tags={','.join(q['tags'])}; file={q['m_file']}",
        )

    # Empty / present TM extras as NONE_IN_SOURCE or catalog
    for cat in extras["empty_categories"]:
        add_row(
            object_class="tmschema",
            object_type=cat,
            parent="",
            name=cat,
            action="NONE_IN_SOURCE",
            expression="",
            notes="Confirmed empty in PBIX",
        )
    for cat in extras["non_empty_categories"]:
        count = extras["categories"][cat].get("record_count", 0)
        # metadata / model / partitions / annotations are informational
        if cat in ("rls", "ols", "perspectives", "connections"):
            action = "NONE_IN_SOURCE" if count == 0 else "LOOKML_TODO_COMPLEX"
        elif cat in ("metadata", "tmschema_model", "tmschema_annotations", "tmschema_partitions", "tmschema_extended_properties"):
            action = "SKIP_PBI_INTERNAL"
            notes = f"Present ({count} records) — capture only; not LookML objects"
            add_row(
                object_class="tmschema",
                object_type=cat,
                parent="",
                name=cat,
                action=action,
                expression="",
                notes=notes,
            )
            continue
        else:
            action = "LOOKML_TODO_COMPLEX"
        add_row(
            object_class="tmschema",
            object_type=cat,
            parent="",
            name=cat,
            action=action,
            expression="",
            notes=f"Present with {count} records — review for Looker relevance",
        )

    # Write CSV
    import csv

    matrix_path = OUT / "ACTION_MATRIX.csv"
    fieldnames = [
        "object_class",
        "object_type",
        "parent",
        "name",
        "action",
        "expression",
        "notes",
    ]
    with matrix_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # Action summary counts
    from collections import Counter

    action_counts = Counter(r["action"] for r in rows)
    class_counts = Counter(r["object_class"] for r in rows)

    # ---------- OBJECT_INVENTORY.md ----------
    lines = []
    lines.append("# Power BI Object Inventory")
    lines.append("")
    lines.append(f"**Source:** `{PBIX}`")
    lines.append("")
    lines.append("Semantic-model objects only (report visuals out of scope).")
    lines.append("")
    lines.append("## Completeness gate")
    lines.append("")
    if gate_failures:
        lines.append("**FAILED**")
        for g in gate_failures:
            lines.append(f"- {g}")
    else:
        lines.append("**PASSED** — all capture gates succeeded.")
    lines.append("")
    lines.append("| Gate | Expected | Actual |")
    lines.append("|---|---|---|")
    lines.append(f"| Tables | 15 | {len(tables)} |")
    lines.append(f"| Schema columns | (all) | {schema_out['column_count']} |")
    lines.append(f"| Measures | 30 | {dax_out['measure_count']} |")
    lines.append(f"| Calculated columns | (all) | {dax_out['calculated_column_count']} |")
    lines.append(f"| Calculated tables | 6 | {dax_out['calculated_table_count']} |")
    lines.append(f"| Relationships | 8 | {rel_out['relationship_count']} |")
    lines.append(f"| Power Query queries | 9 | {pq_out['power_query_count']} |")
    lines.append(f"| `.m` files | 9 | {len(m_files)} |")
    lines.append(f"| TM empty categories listed | yes | {len(extras['empty_categories'])} |")
    lines.append("")
    lines.append("## Action summary")
    lines.append("")
    lines.append("| Action tag | Count |")
    lines.append("|---|---|")
    for k, v in sorted(action_counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("| Object class | Count |")
    lines.append("|---|---|")
    for k, v in sorted(class_counts.items()):
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Tables")
    lines.append("")
    for t in tables:
        kind = "SKIP_PBI_INTERNAL" if is_auto_date_table(t) else (
            "LOOKML_VIEW_FACT" if t == "Employee" else "LOOKML_VIEW_DIM"
        )
        cols = [c for c in schema_out["columns"] if c["table"] == t]
        lines.append(f"### `{t}` → `{kind}` ({len(cols)} columns)")
        lines.append("")
        for c in cols:
            lines.append(f"- `{c['column']}` ({c['pandas_dtype']})")
        lines.append("")

    lines.append("## Measures (full DAX)")
    lines.append("")
    for m in dax_out["measures"]:
        lines.append(f"### `{m['table']}[{m['name']}]` → `{m['suggested_action']}`")
        lines.append("")
        lines.append("```dax")
        lines.append(m["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## Calculated columns (full DAX)")
    lines.append("")
    for c in dax_out["calculated_columns"]:
        lines.append(
            f"### `{c['table']}[{c['column']}]` → `{c['suggested_action']}`"
        )
        lines.append("")
        lines.append("```dax")
        lines.append(c["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## Calculated tables (full DAX)")
    lines.append("")
    for t in dax_out["calculated_tables"]:
        lines.append(f"### `{t['table']}` → `{t['suggested_action']}`")
        lines.append("")
        lines.append("```dax")
        lines.append(t["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## Relationships")
    lines.append("")
    lines.append("| From | To | Cardinality | Active | Cross-filter | Action |")
    lines.append("|---|---|---|---|---|---|")
    for r in rel_out["relationships"]:
        lines.append(
            f"| {r['from_table']}.{r['from_column']} | {r['to_table']}.{r['to_column']} | "
            f"{r['cardinality']} | {r['is_active']} | {r['cross_filtering_behavior']} | LOOKML_JOIN |"
        )
    lines.append("")

    lines.append("## Power Query (M)")
    lines.append("")
    for q in pq_out["queries"]:
        lines.append(
            f"### `{q['table']}` → `{q['suggested_action']}` "
            f"(complexity={q['complexity']}; tags={', '.join(q['tags'])})"
        )
        lines.append("")
        lines.append(f"Raw file: `{q['m_file']}`")
        lines.append("")
        if q.get("embedded_sql"):
            lines.append("Embedded SQL:")
            lines.append("")
            lines.append("```sql")
            lines.append(q["embedded_sql"][0])
            lines.append("```")
            lines.append("")
        lines.append("<details><summary>Full M expression</summary>")
        lines.append("")
        lines.append("```powerquery")
        lines.append(q["expression"])
        lines.append("```")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    lines.append("## TM schema extras")
    lines.append("")
    lines.append("### Non-empty")
    lines.append("")
    for cat in extras["non_empty_categories"]:
        lines.append(
            f"- `{cat}` ({extras['categories'][cat].get('record_count', 0)} records)"
        )
    lines.append("")
    lines.append("### Empty (confirmed NONE_IN_SOURCE)")
    lines.append("")
    for cat in extras["empty_categories"]:
        lines.append(f"- `{cat}`")
    lines.append("")

    lines.append("## Artifact index")
    lines.append("")
    lines.append("| File | Description |")
    lines.append("|---|---|")
    lines.append("| `01_tables_columns.json` | Tables, columns, stats, TM columns |")
    lines.append("| `02_dax_objects.json` | Measures, calc columns, calc tables |")
    lines.append("| `03_relationships.json` | Relationships |")
    lines.append("| `04_power_query_m.json` | M metadata + embedded SQL |")
    lines.append("| `04_m_raw/*.m` | Verbatim M per table |")
    lines.append("| `05_tmschema_extras.json` | Partitions, hierarchies, RLS, etc. |")
    lines.append("| `ACTION_MATRIX.csv` | Every object → Looker/dbt/SKIP action |")
    lines.append("| `OBJECT_INVENTORY.md` | This document |")
    lines.append("")
    lines.append("## What to do next in Looker / dbt")
    lines.append("")
    lines.append("1. **dbt:** Implement all `DBT_SQL` / `DBT_SEED` rows (especially Employee M SQL + calc columns).")
    lines.append("2. **LookML views/joins:** Cover all `LOOKML_VIEW_*` and `LOOKML_JOIN` rows.")
    lines.append("3. **Complex measures:** Hand-implement each `LOOKML_TODO_COMPLEX` (SPLY, EmpCount period max, TO % Norm).")
    lines.append("4. **Skip:** `SKIP_PBI_INTERNAL` auto date tables unless product requires them.")
    lines.append("5. **Ignore:** `NONE_IN_SOURCE` categories (nothing to migrate).")
    lines.append("")

    inv_path = OUT / "OBJECT_INVENTORY.md"
    inv_path.write_text("\n".join(lines) + "\n")

    gate_path = OUT / "COMPLETENESS_GATE.json"
    dump_json(
        gate_path,
        {
            "passed": len(gate_failures) == 0,
            "failures": gate_failures,
            "counts": {
                "tables": len(tables),
                "columns": schema_out["column_count"],
                "measures": dax_out["measure_count"],
                "calculated_columns": dax_out["calculated_column_count"],
                "calculated_tables": dax_out["calculated_table_count"],
                "relationships": rel_out["relationship_count"],
                "power_query": pq_out["power_query_count"],
                "m_files": len(m_files),
                "action_matrix_rows": len(rows),
                "empty_tm_categories": len(extras["empty_categories"]),
                "non_empty_tm_categories": len(extras["non_empty_categories"]),
            },
        },
    )

    if gate_failures:
        print("COMPLETENESS GATE FAILED:", file=sys.stderr)
        for g in gate_failures:
            print(" -", g, file=sys.stderr)
        return 1
    print("COMPLETENESS GATE PASSED")
    print(f"Wrote {inv_path}")
    print(f"Wrote {matrix_path} ({len(rows)} rows)")
    return 0


def main():
    bundle = extract_all()
    rc = merge(bundle)
    sys.exit(rc)


if __name__ == "__main__":
    main()
