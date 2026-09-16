#!/usr/bin/env python3
"""
Phase 1 Orchestrator — deterministic Power BI semantic inventory extract.

Six specialist stages (Python + pbixray; no LLM):
  1 Tabular Schema
  2 Relationships
  3 DAX
  4 Power Query M
  5 TM Extras
  6 Merger

Extract-only phase: full semantic inventory + object counts.
No validation gates, warehouse SQL, LookML, data loading, sample data, or LLM.
Optional later: NL Q&A agent on top of inventory (not part of this extract).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from pbixray import PBIXRay

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
M_RAW = OUT / "04_m_raw"
# Active PBIX only — never hardcode a sample model; set in run_extraction via CLI/UI/uploads.
PBIX_PATH: Path | None = None

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from workspace import reset_dynamic_outputs, set_current_pbix

COMPLEX_PATTERNS = [
    "CALCULATE",
    "FILTER",
    "ALL",
    "ALLEXCEPT",
    "REMOVEFILTERS",
    "SAMEPERIODLASTYEAR",
    "DATEADD",
    "TOTALYTD",
    "DATESYTD",
    "PARALLELPERIOD",
    "MAX",
    "MIN",
    "VALUES",
    "SELECTEDVALUE",
    "SUMX",
    "AVERAGEX",
    "RANKX",
    "SWITCH",
    "USERELATIONSHIP",
    "RELATED",
    "LOOKUPVALUE",
]

HEAVY_COMPLEX = {
    "SAMEPERIODLASTYEAR",
    "DATESYTD",
    "TOTALYTD",
    "PARALLELPERIOD",
    "DATEADD",
    "USERELATIONSHIP",
    "ALLEXCEPT",
    "REMOVEFILTERS",
    "RANKX",
    "SUMX",
    "AVERAGEX",
}


def clean(v):
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    if hasattr(v, "item"):
        try:
            return v.item()
        except Exception:
            pass
    return v


def df_records(df) -> list:
    if df is None:
        return []
    if not isinstance(df, pd.DataFrame) or df.empty:
        return []
    records = json.loads(df.to_json(orient="records", date_format="iso"))
    return records


def safe_df(pbix, name: str):
    try:
        val = getattr(pbix, name, None)
    except Exception as e:
        return None, str(e)
    if val is None:
        return None, None
    if isinstance(val, pd.DataFrame):
        return val, None
    return None, f"non-dataframe:{type(val).__name__}"


def is_internal_table(name: str) -> bool:
    n = name or ""
    return n.startswith("LocalDateTable_") or n.startswith("DateTableTemplate_")


def classify_complexity(expr: str) -> str:
    e = expr or ""
    upper = e.upper()
    hits = [p for p in COMPLEX_PATTERNS if p.upper() in upper]
    if any(p in upper for p in HEAVY_COMPLEX) or upper.count("CALCULATE") >= 2:
        return "COMPLEX"
    if hits:
        return "MODERATE"
    if len(e) > 200 or e.count("\n") > 5:
        return "MODERATE"
    return "SIMPLE"


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_pbix_path(pbix_path: Path | None) -> Path:
    """
    Resolve the single active PBIX for this run.
    Priority: explicit arg → CURRENT_PBIX.json → sole file in phase1/uploads/.
    Never falls back to a hardcoded sample PBIX.
    """
    if pbix_path is not None:
        return Path(pbix_path).expanduser().resolve()

    for meta_path in (ROOT / "CURRENT_PBIX.json", OUT / "CURRENT_PBIX.json"):
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        candidate = Path(meta.get("pbix_path") or "")
        if candidate.exists() and candidate.suffix.lower() == ".pbix":
            return candidate.resolve()

    uploads = sorted((ROOT / "uploads").glob("*.pbix"))
    if len(uploads) == 1:
        return uploads[0].resolve()
    if len(uploads) > 1:
        names = ", ".join(p.name for p in uploads)
        raise FileNotFoundError(
            f"Multiple PBIX files in phase1/uploads/ ({names}). "
            "Pass one path explicitly, or re-upload so only the current file remains."
        )
    raise FileNotFoundError(
        "No PBIX specified. Pass a .pbix path, or upload one in the Streamlit UI "
        "(writes phase1/uploads/<file>.pbix)."
    )


def agent1_schema(pbix: PBIXRay) -> dict:
    schema = pbix.schema
    tm_tables, err_t = safe_df(pbix, "tmschema_tables")
    tm_cols, err_c = safe_df(pbix, "tmschema_columns")
    dax_tables = pbix.dax_tables
    dax_cols = pbix.dax_columns

    table_names = list(pbix.tables)
    tm_by_name = {}
    if tm_tables is not None and not tm_tables.empty:
        for rec in df_records(tm_tables):
            tm_by_name[rec.get("Name")] = rec

    calc_table_names = set()
    if dax_tables is not None and not dax_tables.empty:
        calc_table_names = set(dax_tables["TableName"].tolist())

    calc_col_map = {}
    if dax_cols is not None and not dax_cols.empty:
        for _, r in dax_cols.iterrows():
            calc_col_map[(r["TableName"], r["ColumnName"])] = r["Expression"]

    tm_col_map = {}
    if tm_cols is not None and not tm_cols.empty:
        for rec in df_records(tm_cols):
            # Type 2 = calculated in this model; keep all rows keyed by table+name
            key = (rec.get("TableName"), rec.get("Name"))
            # Prefer calculated / richer metadata when duplicates
            prev = tm_col_map.get(key)
            if prev is None or (rec.get("Type") == 2 and prev.get("Type") != 2):
                tm_col_map[key] = rec

    tables = []
    internal_tables = []
    for name in table_names:
        meta = tm_by_name.get(name, {})
        is_internal = is_internal_table(name)
        is_calc = name in calc_table_names
        is_business = not is_internal
        if is_internal:
            ttype = "internal_auto_date"
        elif is_calc:
            ttype = "calculated_table"
        else:
            ttype = "business"
        entry = {
            "table_name": name,
            "table_type": ttype,
            "hidden": bool(meta.get("IsHidden")) if meta else None,
            "private": bool(meta.get("IsPrivate")) if meta else None,
            "description": meta.get("Description"),
            "is_internal": is_internal,
            "is_business": is_business,
            "is_calculated_table": is_calc,
        }
        tables.append(entry)
        if is_internal:
            internal_tables.append(entry)

    columns = []
    calculated_column_count = 0
    for _, row in schema.iterrows():
        tname = row["TableName"]
        cname = row["ColumnName"]
        tm = tm_col_map.get((tname, cname), {})
        expr = calc_col_map.get((tname, cname))
        if expr is None:
            expr = tm.get("Expression")
        is_calc_col = expr is not None and str(expr).strip() != ""
        if tm.get("Type") == 2:
            is_calc_col = True
        if is_calc_col:
            calculated_column_count += 1
        columns.append(
            {
                "table_name": tname,
                "column_name": cname,
                "data_type": tm.get("DataType") or row.get("PandasDataType"),
                "pandas_dtype": row.get("PandasDataType"),
                "source_column": tm.get("SourceColumn"),
                "hidden": bool(tm.get("IsHidden")) if tm else None,
                "is_calculated_column": is_calc_col,
                "expression": expr if is_calc_col else None,
                "format_string": tm.get("FormatString"),
                "description": tm.get("Description"),
                "display_folder": tm.get("DisplayFolder"),
                "is_key": bool(tm.get("IsKey")) if tm else None,
                "data_category": tm.get("DataCategory"),
            }
        )

    calculated_tables = []
    if dax_tables is not None and not dax_tables.empty:
        for _, r in dax_tables.iterrows():
            meta = tm_by_name.get(r["TableName"], {})
            calculated_tables.append(
                {
                    "table_name": r["TableName"],
                    "expression": r["Expression"],
                    "hidden": bool(meta.get("IsHidden")) if meta else None,
                    "is_internal": is_internal_table(r["TableName"]),
                }
            )

    out = {
        "agent": "1_tabular_schema",
        "source_pbix": str(PBIX_PATH),
        "extraction_errors": [e for e in [err_t, err_c] if e],
        "tables": tables,
        "columns": columns,
        "calculated_tables": calculated_tables,
        "internal_tables": internal_tables,
        "validation": {
            "total_tables": len(tables),
            "total_columns": len(columns),
            "total_calculated_columns": calculated_column_count,
            "total_calculated_tables": len(calculated_tables),
            "internal_table_count": len(internal_tables),
            "business_table_count": sum(1 for t in tables if t["is_business"]),
        },
    }
    write_json(OUT / "01_tables_columns.json", out)
    return out


def agent2_relationships(pbix: PBIXRay) -> dict:
    rel = pbix.relationships
    relationships = []
    for rec in df_records(rel):
        relationships.append(
            {
                "from_table": rec.get("FromTableName"),
                "from_column": rec.get("FromColumnName"),
                "to_table": rec.get("ToTableName"),
                "to_column": rec.get("ToColumnName"),
                "cardinality": rec.get("Cardinality"),
                "cross_filter": rec.get("CrossFilteringBehavior"),
                "active": bool(rec.get("IsActive")),
                "from_key_count": rec.get("FromKeyCount"),
                "to_key_count": rec.get("ToKeyCount"),
                "rely_on_referential_integrity": bool(rec.get("RelyOnReferentialIntegrity"))
                if rec.get("RelyOnReferentialIntegrity") is not None
                else None,
                "relationship_type": "single_column",
            }
        )

    active = sum(1 for r in relationships if r["active"])
    inactive = len(relationships) - active
    out = {
        "agent": "2_relationships",
        "source_pbix": str(PBIX_PATH),
        "relationships": relationships,
        "validation": {
            "total_relationships": len(relationships),
            "active_relationships": active,
            "inactive_relationships": inactive,
            "cross_filter_directions": dict(
                Counter(r["cross_filter"] for r in relationships)
            ),
            "cardinality_distribution": dict(
                Counter(r["cardinality"] for r in relationships)
            ),
        },
    }
    write_json(OUT / "03_relationships.json", out)
    return out


def agent3_dax(pbix: PBIXRay) -> dict:
    measures = []
    complexity_counter = Counter()
    for rec in df_records(pbix.dax_measures):
        expr = rec.get("Expression") or ""
        complexity = classify_complexity(expr)
        complexity_counter[complexity] += 1
        measures.append(
            {
                "table": rec.get("TableName"),
                "measure_name": rec.get("Name"),
                "expression": expr,
                "format_string": None,  # not exposed on dax_measures in this pbixray version
                "description": rec.get("Description"),
                "hidden": None,
                "display_folder": rec.get("DisplayFolder"),
                "complexity": complexity,
            }
        )

    calculated_columns = []
    for rec in df_records(pbix.dax_columns):
        expr = rec.get("Expression") or ""
        complexity = classify_complexity(expr)
        complexity_counter[f"calc_col_{complexity}"] += 1
        calculated_columns.append(
            {
                "table": rec.get("TableName"),
                "column_name": rec.get("ColumnName"),
                "expression": expr,
                "data_type": None,
                "format_string": None,
                "complexity": complexity,
            }
        )

    calculated_tables = []
    for rec in df_records(pbix.dax_tables):
        expr = rec.get("Expression") or ""
        complexity = classify_complexity(expr)
        calculated_tables.append(
            {
                "table_name": rec.get("TableName"),
                "expression": expr,
                "complexity": complexity,
            }
        )

    # Enrich calc columns with TM metadata when available
    tm_cols, _ = safe_df(pbix, "tmschema_columns")
    if tm_cols is not None and not tm_cols.empty:
        idx = {
            (r["TableName"], r["Name"]): r
            for r in df_records(tm_cols)
            if r.get("Type") == 2
        }
        for c in calculated_columns:
            meta = idx.get((c["table"], c["column_name"]), {})
            c["data_type"] = meta.get("DataType")
            c["format_string"] = meta.get("FormatString")

    # Enrich measures format/hidden from annotations if present — skip inventing

    out = {
        "agent": "3_dax",
        "source_pbix": str(PBIX_PATH),
        "measures": measures,
        "calculated_columns": calculated_columns,
        "calculated_tables": calculated_tables,
        "complexity_summary": {
            "measures": dict(Counter(m["complexity"] for m in measures)),
            "calculated_columns": dict(
                Counter(c["complexity"] for c in calculated_columns)
            ),
            "calculated_tables": dict(
                Counter(t["complexity"] for t in calculated_tables)
            ),
        },
        "validation": {
            "measure_count": len(measures),
            "calculated_column_count": len(calculated_columns),
            "calculated_table_count": len(calculated_tables),
            "simple_moderate_complex_measures": dict(
                Counter(m["complexity"] for m in measures)
            ),
        },
    }
    write_json(OUT / "02_dax_objects.json", out)
    return out


def classify_m(expression: str) -> dict:
    expr = expression or ""
    tags = []
    if "Sql.Database" in expr or "Sql.Databases" in expr:
        tags.append("sql_database")
    if "GoogleBigQuery" in expr or "BigQuery" in expr:
        tags.append("bigquery")
    if "Excel.Workbook" in expr or "Csv.Document" in expr:
        tags.append("file_source")
    if "Table.FromRows" in expr or "Binary.Decompress" in expr:
        tags.append("embedded_seed")
    if "Table.NestedJoin" in expr or "Table.Join" in expr or "JoinKind" in expr:
        tags.append("merge_join")
    if "Table.Combine" in expr or "union all" in expr.lower():
        tags.append("append_union")
    if re.search(r"#\"[^\"]+\"", expr):
        tags.append("query_reference")
    if "Table.AddColumn" in expr or "Table.TransformColumns" in expr:
        tags.append("column_transform")
    if "Table.SelectRows" in expr:
        tags.append("filter")
    if len(expr) > 1500 or expr.count("\n") > 25:
        tags.append("transformation_heavy")
    if not tags:
        tags.append("simple_transform")
    sql_statements = re.findall(
        r'(?:Query|Sql)=?"((?:[^"\\]|\\.)*)"', expr, flags=re.IGNORECASE
    )
    # Also capture common embedded SQL after Value.NativeQuery / Sql.Database
    native = re.findall(
        r'Value\.NativeQuery\([^,]+,\s*"((?:[^"\\]|\\.)*)"', expr
    )
    sqls = []
    for s in sql_statements + native:
        s2 = s.replace('\\"', '"').replace("\\n", "\n")
        if "select" in s2.lower() or "from" in s2.lower():
            sqls.append(s2)
    source_type = "unknown"
    if "sql_database" in tags:
        source_type = "sql_database"
    elif "bigquery" in tags:
        source_type = "bigquery"
    elif "file_source" in tags:
        source_type = "file"
    elif "embedded_seed" in tags:
        source_type = "embedded_static"
    return {
        "tags": tags,
        "source_type": source_type,
        "sql_statements": sqls,
        "has_sql": "sql_database" in tags or bool(sqls),
        "has_dependencies": "query_reference" in tags,
        "has_append_union": "append_union" in tags,
        "has_merge_join": "merge_join" in tags,
        "is_embedded_static": "embedded_seed" in tags,
        "is_transformation_heavy": "transformation_heavy" in tags,
    }


def agent4_power_query(pbix: PBIXRay) -> dict:
    M_RAW.mkdir(parents=True, exist_ok=True)
    # Clear prior .m files
    for old in M_RAW.glob("*.m"):
        old.unlink()

    queries = []
    pq = pbix.power_query
    for rec in df_records(pq):
        name = rec.get("TableName")
        expr = rec.get("Expression") or ""
        flags = classify_m(expr)
        # Safe filename
        safe_name = re.sub(r"[^\w.\-]+", "_", name)
        m_path = M_RAW / f"{safe_name}.m"
        m_path.write_text(expr, encoding="utf-8")
        queries.append(
            {
                "query_name": name,
                "m_file": f"04_m_raw/{safe_name}.m",
                "expression": expr,
                "source_type": flags["source_type"],
                "tags": flags["tags"],
                "sql_statements": flags["sql_statements"],
                "has_sql": flags["has_sql"],
                "has_dependencies": flags["has_dependencies"],
                "has_append_union": flags["has_append_union"],
                "has_merge_join": flags["has_merge_join"],
                "is_embedded_static": flags["is_embedded_static"],
                "is_transformation_heavy": flags["is_transformation_heavy"],
                "parameters": [],
                "referenced_queries": re.findall(r'#\"([^\"]+)\"', expr),
            }
        )

    m_params, _ = safe_df(pbix, "m_parameters")
    out = {
        "agent": "4_power_query_m",
        "source_pbix": str(PBIX_PATH),
        "queries": queries,
        "m_parameters": df_records(m_params) if m_params is not None else [],
        "validation": {
            "total_power_query_queries": len(queries),
            "queries_with_sql": sum(1 for q in queries if q["has_sql"]),
            "queries_with_dependencies": sum(1 for q in queries if q["has_dependencies"]),
            "append_union_queries": sum(1 for q in queries if q["has_append_union"]),
            "merge_join_queries": sum(1 for q in queries if q["has_merge_join"]),
            "embedded_static_tables": sum(1 for q in queries if q["is_embedded_static"]),
            "transformation_heavy_queries": sum(
                1 for q in queries if q["is_transformation_heavy"]
            ),
            "m_files_written": len(list(M_RAW.glob("*.m"))),
        },
    }
    write_json(OUT / "04_power_query_m.json", out)
    return out


def agent5_tm_extras(pbix: PBIXRay) -> dict:
    partitions = df_records(safe_df(pbix, "tmschema_partitions")[0])
    hierarchies = df_records(safe_df(pbix, "tmschema_hierarchies")[0])
    levels = df_records(safe_df(pbix, "tmschema_levels")[0])
    annotations = df_records(safe_df(pbix, "tmschema_annotations")[0])
    rls = df_records(safe_df(pbix, "rls")[0])
    ols = df_records(safe_df(pbix, "ols")[0])
    perspectives = df_records(safe_df(pbix, "perspectives")[0])
    tm_perspectives = df_records(safe_df(pbix, "tmschema_perspectives")[0])
    variations = df_records(safe_df(pbix, "tmschema_variations")[0])
    cultures = df_records(safe_df(pbix, "tmschema_cultures")[0])
    model = df_records(safe_df(pbix, "tmschema_model")[0])
    metadata = df_records(safe_df(pbix, "metadata")[0])
    attr_hier = df_records(safe_df(pbix, "tmschema_attribute_hierarchies")[0])
    role_memberships = df_records(safe_df(pbix, "tmschema_role_memberships")[0])
    column_permissions = df_records(safe_df(pbix, "tmschema_column_permissions")[0])

    # Sort-by from columns that have SortByColumn if present — check columns
    tm_cols = safe_df(pbix, "tmschema_columns")[0]
    sort_by_columns = []
    display_folders = []
    format_strings = []
    if tm_cols is not None and not tm_cols.empty:
        for rec in df_records(tm_cols):
            if rec.get("DisplayFolder"):
                display_folders.append(
                    {
                        "table": rec.get("TableName"),
                        "column": rec.get("Name"),
                        "display_folder": rec.get("DisplayFolder"),
                        "object_kind": "column",
                    }
                )
            if rec.get("FormatString"):
                format_strings.append(
                    {
                        "table": rec.get("TableName"),
                        "column": rec.get("Name"),
                        "format_string": rec.get("FormatString"),
                        "object_kind": "column",
                    }
                )
            # SortByColumnName may not exist in this schema version

    # hierarchy levels nested
    levels_by_h = {}
    for lv in levels:
        key = (lv.get("TableName"), lv.get("HierarchyName"))
        levels_by_h.setdefault(key, []).append(lv)
    hierarchies_rich = []
    for h in hierarchies:
        key = (h.get("TableName"), h.get("Name"))
        lv = sorted(levels_by_h.get(key, []), key=lambda x: x.get("Ordinal") or 0)
        hierarchies_rich.append(
            {
                "hierarchy_name": h.get("Name"),
                "table": h.get("TableName"),
                "description": h.get("Description"),
                "hidden": bool(h.get("IsHidden")) if h.get("IsHidden") is not None else None,
                "display_folder": h.get("DisplayFolder"),
                "levels": [
                    {
                        "ordinal": x.get("Ordinal"),
                        "level_name": x.get("Name"),
                        "column_name": x.get("ColumnName"),
                    }
                    for x in lv
                ],
            }
        )

    # Auto date tables detail from schema + dax_tables + hierarchies
    schema = pbix.schema
    auto_date_tables = []
    for tname in pbix.tables:
        if not is_internal_table(tname):
            continue
        cols = schema[schema["TableName"] == tname]
        dax_expr = None
        for rec in df_records(pbix.dax_tables):
            if rec.get("TableName") == tname:
                dax_expr = rec.get("Expression")
                break
        auto_date_tables.append(
            {
                "table_name": tname,
                "columns": [
                    {"column_name": r.ColumnName, "pandas_dtype": r.PandasDataType}
                    for r in cols.itertuples()
                ],
                "dax_expression": dax_expr,
                "hierarchies": [
                    h for h in hierarchies_rich if h.get("table") == tname
                ],
            }
        )

    # Empty categories must remain present
    empty_named = {
        "rls": rls,
        "ols": ols,
        "perspectives": perspectives or tm_perspectives,
        "role_memberships": role_memberships,
        "column_permissions": column_permissions,
        "aggregations": df_records(safe_df(pbix, "aggregations")[0]),
        "connections": list(pbix.connections or []),
    }

    out = {
        "agent": "5_tm_extras",
        "source_pbix": str(PBIX_PATH),
        "partitions": partitions,
        "hierarchies": hierarchies_rich,
        "hierarchy_levels_flat": levels,
        "rls": rls if rls is not None else [],
        "ols": ols if ols is not None else [],
        "perspectives": empty_named["perspectives"] if empty_named["perspectives"] else [],
        "annotations": annotations,
        "display_folders": display_folders,
        "sort_by_columns": sort_by_columns,
        "format_strings": format_strings,
        "auto_date_tables": auto_date_tables,
        "attribute_hierarchies": attr_hier,
        "variations": variations,
        "cultures": cultures,
        "model": model,
        "metadata": metadata,
        "role_memberships": role_memberships if role_memberships else [],
        "column_permissions": column_permissions if column_permissions else [],
        "other": {
            "connections": empty_named["connections"],
            "aggregations": empty_named["aggregations"],
            "linguistic_metadata_present": not (
                safe_df(pbix, "tmschema_linguistic_metadata")[0] is None
                or safe_df(pbix, "tmschema_linguistic_metadata")[0].empty
            ),
        },
        "validation": {
            "partitions": len(partitions),
            "hierarchies": len(hierarchies_rich),
            "hierarchy_levels": len(levels),
            "rls": len(rls) if rls else 0,
            "ols": len(ols) if ols else 0,
            "perspectives": len(empty_named["perspectives"] or []),
            "annotations": len(annotations),
            "display_folders": len(display_folders),
            "sort_by_columns": len(sort_by_columns),
            "format_strings": len(format_strings),
            "auto_date_tables": len(auto_date_tables),
            "attribute_hierarchies": len(attr_hier),
            "variations": len(variations),
            "role_memberships": len(role_memberships) if role_memberships else 0,
            "column_permissions": len(column_permissions) if column_permissions else 0,
        },
    }
    write_json(OUT / "05_tmschema_extras.json", out)
    return out


def agent6_merger(a1, a2, a3, a4, a5) -> dict:
    """Merge specialist outputs into OBJECT_INVENTORY.md + count summary. No gates."""
    m_files = sorted(M_RAW.glob("*.m"))
    counts = {
        "tables": a1["validation"]["total_tables"],
        "business_tables": a1["validation"]["business_table_count"],
        "internal_tables": a1["validation"]["internal_table_count"],
        "columns": a1["validation"]["total_columns"],
        "measures": a3["validation"]["measure_count"],
        "calculated_columns": a3["validation"]["calculated_column_count"],
        "calculated_tables": a3["validation"]["calculated_table_count"],
        "relationships": a2["validation"]["total_relationships"],
        "power_query": a4["validation"]["total_power_query_queries"],
        "m_files": len(m_files),
        "rls_roles": len(a5.get("rls") or []),
        "hierarchies": a5["validation"]["hierarchies"],
        "partitions": a5["validation"]["partitions"],
        "auto_date_tables": a5["validation"]["auto_date_tables"],
        "annotations": a5["validation"]["annotations"],
        "sort_by_columns": a5["validation"]["sort_by_columns"],
        "format_strings": a5["validation"]["format_strings"],
        "perspectives": a5["validation"]["perspectives"],
        "display_folders": a5["validation"]["display_folders"],
    }

    lines = []
    lines.append(f"# OBJECT INVENTORY — {PBIX_PATH.name}")
    lines.append("")
    lines.append(f"**Source:** `{PBIX_PATH}`")
    lines.append("")
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Tables | {counts['tables']} |")
    lines.append(f"| Business tables | {counts['business_tables']} |")
    lines.append(f"| Internal tables | {counts['internal_tables']} |")
    lines.append(f"| Columns | {counts['columns']} |")
    lines.append(f"| Measures | {counts['measures']} |")
    lines.append(f"| Calculated columns | {counts['calculated_columns']} |")
    lines.append(f"| Calculated tables | {counts['calculated_tables']} |")
    lines.append(f"| Relationships | {counts['relationships']} |")
    lines.append(f"| Power Query queries | {counts['power_query']} |")
    lines.append(f"| M raw files | {counts['m_files']} |")
    lines.append(f"| Hierarchies | {counts['hierarchies']} |")
    lines.append(f"| Partitions | {counts['partitions']} |")
    lines.append(f"| Auto date tables | {counts['auto_date_tables']} |")
    lines.append(f"| RLS roles | {counts['rls_roles']} |")
    lines.append("")
    lines.append("## 2. Tables")
    lines.append("")
    for t in a1["tables"]:
        cols = [c for c in a1["columns"] if c["table_name"] == t["table_name"]]
        calc_cols = [c for c in cols if c["is_calculated_column"]]
        msrc = next(
            (q for q in a4["queries"] if q["query_name"] == t["table_name"]), None
        )
        lines.append(f"### `{t['table_name']}`")
        lines.append("")
        lines.append(f"- **type:** {t['table_type']}")
        lines.append(
            f"- **business:** {t['is_business']} | **internal:** {t['is_internal']}"
        )
        lines.append(f"- **columns:** {len(cols)} ({len(calc_cols)} calculated)")
        if msrc:
            lines.append(
                f"- **Power Query:** `{msrc['m_file']}` ({msrc['source_type']})"
            )
        elif t["is_calculated_table"]:
            lines.append("- **source:** calculated table (DAX)")
        lines.append("")

    lines.append("## 3. Measures")
    lines.append("")
    for m in a3["measures"]:
        lines.append(f"### `{m['table']}[{m['measure_name']}]` — {m['complexity']}")
        lines.append("")
        lines.append("```dax")
        lines.append(m["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## 4. Calculated Columns")
    lines.append("")
    for c in a3["calculated_columns"]:
        lines.append(f"### `{c['table']}[{c['column_name']}]` — {c['complexity']}")
        lines.append("")
        lines.append("```dax")
        lines.append(c["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## 5. Calculated Tables")
    lines.append("")
    for t in a3["calculated_tables"]:
        lines.append(f"### `{t['table_name']}` — {t['complexity']}")
        lines.append("")
        lines.append("```dax")
        lines.append(t["expression"])
        lines.append("```")
        lines.append("")

    lines.append("## 6. Relationships")
    lines.append("")
    lines.append(
        "| From | Column | To | Column | Cardinality | Cross-filter | Active |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for r in a2["relationships"]:
        lines.append(
            f"| {r['from_table']} | {r['from_column']} | {r['to_table']} | "
            f"{r['to_column']} | {r['cardinality']} | {r['cross_filter']} | {r['active']} |"
        )
    lines.append("")

    lines.append("## 7. Power Query")
    lines.append("")
    for q in a4["queries"]:
        lines.append(f"### `{q['query_name']}`")
        lines.append("")
        lines.append(f"- **file:** `{q['m_file']}`")
        lines.append(f"- **source_type:** {q['source_type']}")
        lines.append(f"- **tags:** {', '.join(q['tags'])}")
        if q.get("referenced_queries"):
            lines.append(
                f"- **referenced_queries:** {', '.join(q['referenced_queries'])}"
            )
        lines.append("")

    lines.append("## 8. TM Extras")
    lines.append("")
    lines.append(f"- **partitions:** {counts['partitions']}")
    lines.append(f"- **hierarchies:** {counts['hierarchies']}")
    lines.append(
        f"- **RLS:** {counts['rls_roles']} (empty list = none in source)"
    )
    lines.append(f"- **perspectives:** {counts['perspectives']}")
    lines.append(f"- **annotations:** {counts['annotations']}")
    lines.append(f"- **sort-by columns:** {counts['sort_by_columns']}")
    lines.append(f"- **display folders:** {counts['display_folders']}")
    lines.append(f"- **format strings:** {counts['format_strings']}")
    lines.append(f"- **auto date tables:** {counts['auto_date_tables']}")
    lines.append("")
    if a5.get("hierarchies"):
        lines.append("### Hierarchies")
        lines.append("")
        for h in a5["hierarchies"]:
            lv = " → ".join(
                f"{x.get('level_name')}({x.get('column_name')})"
                for x in (h.get("levels") or [])
            )
            lines.append(f"- `{h['table']}.{h['hierarchy_name']}`: {lv}")
        lines.append("")

    inv_path = OUT / "OBJECT_INVENTORY.md"
    inv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(OUT / "OBJECT_COUNTS.json", {"source_pbix": str(PBIX_PATH), "counts": counts})

    return {"counts": counts, "inventory_path": str(inv_path)}


def format_summary(counts: dict, pbix_name: str) -> str:
    c = counts
    return "\n".join(
        [
            "PHASE 1 COMPLETE - OBJECT SUMMARY",
            "",
            f"Source PBIX: {pbix_name}",
            "",
            f"Tables:                 {c['tables']}",
            f"  Business:             {c['business_tables']}",
            f"  Internal auto-date:   {c['internal_tables']}",
            f"Columns:                {c['columns']}",
            f"Measures:               {c['measures']}",
            f"Calculated columns:     {c['calculated_columns']}",
            f"Calculated tables:      {c['calculated_tables']}",
            f"Relationships:          {c['relationships']}",
            f"Power Query queries:    {c['power_query']}",
            f"M raw files:            {c['m_files']}",
            f"Hierarchies:            {c['hierarchies']}",
            f"Partitions:             {c['partitions']}",
            f"Auto date tables:       {c['auto_date_tables']}",
            f"RLS roles:              {c['rls_roles']}",
            f"Annotations:            {c.get('annotations', 0)}",
            f"Format strings:         {c.get('format_strings', 0)}",
            f"Perspectives:           {c.get('perspectives', 0)}",
        ]
    )


def run_extraction(pbix_path: Path | None = None) -> dict:
    """Run deterministic extract stages 1-6 against a PBIX. Returns counts + summary_text.

    Refreshes phase1 dynamic outputs in place for this PBIX only (no backups).
    """
    global PBIX_PATH

    resolved = resolve_pbix_path(pbix_path)
    reset_dynamic_outputs()
    PBIX_PATH = set_current_pbix(resolved)

    if not PBIX_PATH.exists():
        raise FileNotFoundError(f"PBIX not found at {PBIX_PATH}")

    OUT.mkdir(parents=True, exist_ok=True)
    M_RAW.mkdir(parents=True, exist_ok=True)

    pbix = PBIXRay(str(PBIX_PATH))
    a1 = agent1_schema(pbix)
    a2 = agent2_relationships(pbix)
    a3 = agent3_dax(pbix)
    a4 = agent4_power_query(pbix)
    a5 = agent5_tm_extras(pbix)
    merged = agent6_merger(a1, a2, a3, a4, a5)
    counts = merged["counts"]
    summary = format_summary(counts, PBIX_PATH.name)
    (OUT / "OBJECT_SUMMARY.txt").write_text(summary + "\n", encoding="utf-8")
    return {
        "counts": counts,
        "summary_text": summary,
        "inventory_path": merged["inventory_path"],
        "pbix_path": str(PBIX_PATH),
    }


def main() -> int:
    pbix_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    try:
        result = run_extraction(pbix_arg)
    except FileNotFoundError as e:
        print(str(e))
        return 1

    print()
    print(result["summary_text"])
    print()
    print("Files:")
    for p in [
        "01_tables_columns.json",
        "02_dax_objects.json",
        "03_relationships.json",
        "04_power_query_m.json",
        "04_m_raw/*.m",
        "05_tmschema_extras.json",
        "OBJECT_INVENTORY.md",
        "OBJECT_COUNTS.json",
        "OBJECT_SUMMARY.txt",
    ]:
        print(f"- inventory/{p}")
    print("- DATA_MODEL.md / .pdf / .png  (regenerate via generate_data_model_diagram.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
