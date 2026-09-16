"""Phase 1 tools — inventory facts only."""
from __future__ import annotations

from config import MAX_LIST_ITEMS
from tools.pbix_context import get_current_pbix_meta, load_phase1_inventory, truncate_payload


def get_current_pbix() -> dict:
    """Return the currently active PBIX metadata from Phase 1 workspace."""
    return get_current_pbix_meta()


def get_object_counts() -> dict:
    """Return OBJECT_COUNTS.json for the current PBIX extract."""
    data = load_phase1_inventory("OBJECT_COUNTS.json")
    if data is None:
        return {"found": False, "message": "Phase 1 inventory not found. Run extract first."}
    meta = get_current_pbix_meta()
    return truncate_payload({"found": True, "current_pbix": meta.get("pbix_name"), "data": data})


def list_tables(business_only: bool = True) -> dict:
    """List tables from Phase 1 inventory.

    Args:
        business_only: If True, prefer business tables when flagged.
    """
    data = load_phase1_inventory("01_tables_columns.json")
    if not data:
        return {"found": False, "message": "01_tables_columns.json missing."}
    tables = data.get("tables") or []
    out = []
    for t in tables:
        if business_only and t.get("is_business") is False:
            continue
        out.append(
            {
                "table_name": t.get("table_name") or t.get("name"),
                "is_business": t.get("is_business", True),
                "column_count": t.get("column_count") or len(t.get("columns") or []),
            }
        )
        if len(out) >= MAX_LIST_ITEMS:
            break
    return truncate_payload(
        {
            "found": True,
            "count": len(out),
            "tables": out,
            "source_pbix": data.get("source_pbix"),
        }
    )


def search_columns(query: str, limit: int = 25) -> dict:
    """Search columns by name substring (case-insensitive)."""
    data = load_phase1_inventory("01_tables_columns.json")
    if not data:
        return {"found": False, "message": "01_tables_columns.json missing."}
    q = (query or "").strip().lower()
    cols = data.get("columns") or []
    hits = []
    for c in cols:
        name = str(c.get("column_name") or c.get("name") or "")
        table = str(c.get("table_name") or "")
        if q and q not in name.lower() and q not in table.lower():
            continue
        hits.append(
            {
                "table": table,
                "column": name,
                "data_type": c.get("data_type") or c.get("type"),
            }
        )
        if len(hits) >= min(limit, MAX_LIST_ITEMS):
            break
    return truncate_payload({"found": True, "query": query, "hits": hits})


def list_measures(search: str = "", limit: int = 30) -> dict:
    """List DAX measures; optional name search."""
    data = load_phase1_inventory("02_dax_objects.json")
    if not data:
        return {"found": False, "message": "02_dax_objects.json missing."}
    q = (search or "").strip().lower()
    measures = data.get("measures") or []
    out = []
    for m in measures:
        name = str(m.get("name") or m.get("measure_name") or "")
        table = str(m.get("table") or m.get("table_name") or "")
        if q and q not in name.lower() and q not in table.lower():
            continue
        expr = m.get("expression") or m.get("dax") or ""
        out.append(
            {
                "table": table,
                "name": name,
                "expression_preview": str(expr)[:240],
            }
        )
        if len(out) >= min(limit, MAX_LIST_ITEMS):
            break
    return truncate_payload({"found": True, "count": len(out), "measures": out})


def list_relationships(limit: int = 40) -> dict:
    """List model relationships from Phase 1."""
    data = load_phase1_inventory("03_relationships.json")
    if not data:
        return {"found": False, "message": "03_relationships.json missing."}
    rels = data.get("relationships") or []
    out = []
    for r in rels[: min(limit, MAX_LIST_ITEMS)]:
        out.append(
            {
                "from": f"{r.get('from_table')}.{r.get('from_column')}",
                "to": f"{r.get('to_table')}.{r.get('to_column')}",
                "cardinality": r.get("cardinality") or r.get("cross_filtering_behavior"),
                "is_active": r.get("is_active", r.get("active")),
            }
        )
    return truncate_payload({"found": True, "count": len(out), "relationships": out})


def list_power_query(limit: int = 30) -> dict:
    """List Power Query M query names and sources."""
    data = load_phase1_inventory("04_power_query_m.json")
    if not data:
        return {"found": False, "message": "04_power_query_m.json missing."}
    queries = data.get("queries") or []
    out = []
    for q in queries[: min(limit, MAX_LIST_ITEMS)]:
        out.append(
            {
                "name": q.get("name") or q.get("query_name"),
                "kind": q.get("kind") or q.get("pattern"),
                "source_preview": str(q.get("source") or q.get("formula") or "")[:160],
            }
        )
    return truncate_payload({"found": True, "count": len(out), "queries": out})
