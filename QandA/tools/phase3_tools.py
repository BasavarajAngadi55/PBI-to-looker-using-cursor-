"""Phase 3 + validation tools — dashboard/coverage facts only."""
from __future__ import annotations

from config import MAX_LIST_ITEMS, PHASE3
from tools.pbix_context import (
    get_current_pbix_meta,
    load_phase3_inventory,
    load_phase3_json,
    load_validation_json,
    read_repo_text,
    truncate_payload,
)


def get_phase3_summary() -> dict:
    """Return PHASE3_SUMMARY.json."""
    data = load_phase3_json("PHASE3_SUMMARY.json")
    if not data:
        return {"found": False, "message": "Phase 3 not run yet."}
    return truncate_payload(
        {"found": True, "current_pbix": get_current_pbix_meta().get("pbix_name"), "summary": data}
    )


def get_dashboard_coverage() -> dict:
    """Return weighted dashboard coverage from COVERAGE.json."""
    data = load_phase3_inventory("COVERAGE.json")
    if not data:
        return {"found": False, "message": "phase3/inventory/COVERAGE.json missing."}
    return truncate_payload({"found": True, "coverage": data})


def list_report_pages() -> dict:
    """List Power BI report pages extracted in Phase 3."""
    data = load_phase3_inventory("01_report_pages.json")
    if not data:
        return {"found": False, "message": "01_report_pages.json missing."}
    pages = data.get("pages") or []
    out = [
        {
            "name": p.get("display_name") or p.get("name"),
            "slug": p.get("slug"),
            "visual_count": p.get("visual_count"),
        }
        for p in pages
    ]
    return truncate_payload(
        {"found": True, "source_pbix": data.get("source_pbix"), "pages": out}
    )


def search_visuals(page: str = "", status: str = "", limit: int = 30) -> dict:
    """Search mapped visuals by page name and/or status (mapped|partial|gap|skip)."""
    mapping = load_phase3_inventory("03_dashboard_mapping.json")
    if not mapping:
        return {"found": False, "message": "03_dashboard_mapping.json missing."}
    items = mapping.get("mapped_visuals") or []
    pg = (page or "").strip().lower()
    st = (status or "").strip().lower()
    out = []
    for v in items:
        if pg and pg not in str(v.get("page", "")).lower():
            continue
        if st and str(v.get("status", "")).lower() != st:
            continue
        out.append(
            {
                "page": v.get("page"),
                "title": v.get("pbi_title"),
                "pbi_type": v.get("pbi_type"),
                "looker": v.get("looker_object"),
                "status": v.get("status"),
                "deficiencies": (v.get("deficiencies") or [])[:2],
            }
        )
        if len(out) >= min(limit, MAX_LIST_ITEMS):
            break
    return truncate_payload({"found": True, "count": len(out), "visuals": out})


def list_lookml_dashboards() -> dict:
    """List generated .dashboard.lookml files."""
    d = PHASE3 / "lookml_dashboards" / "dashboards"
    if not d.exists():
        return {"found": False, "message": "lookml_dashboards/dashboards missing."}
    files = sorted(p.name for p in d.glob("*.dashboard.lookml"))
    return {"found": True, "count": len(files), "dashboards": files}


def get_validation_summary() -> dict:
    """Return validation overall % done/left and confidence."""
    data = load_validation_json("VALIDATION_SUMMARY.json")
    if not data:
        data = load_validation_json("VALIDATION_REPORT.json")
        if data and "overall" in data:
            o = data["overall"]
            data = {
                "overall_pct_done": o.get("pct_done"),
                "overall_pct_left": o.get("pct_left"),
                "confidence": o.get("confidence"),
                "warning": o.get("warning"),
            }
    if not data:
        return {"found": False, "message": "Validation not run yet."}
    return truncate_payload(
        {"found": True, "current_pbix": get_current_pbix_meta().get("pbix_name"), "validation": data}
    )


def read_page_comparison(limit_chars: int = 5000) -> dict:
    """Read PAGE_COMPARISON.md excerpt (PBI vs Looker)."""
    return read_repo_text("phase3/comparison/PAGE_COMPARISON.md", limit=limit_chars)
