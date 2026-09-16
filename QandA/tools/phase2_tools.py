"""Phase 2 tools — LookML / mapping facts only."""
from __future__ import annotations

from config import MAX_LIST_ITEMS, PHASE2
from tools.pbix_context import get_current_pbix_meta, load_phase2_json, read_repo_text, truncate_payload


def get_phase2_summary() -> dict:
    """Return PHASE2_SUMMARY.json for the current migration run."""
    data = load_phase2_json("PHASE2_SUMMARY.json")
    if not data:
        return {"found": False, "message": "Phase 2 not run yet."}
    return truncate_payload(
        {"found": True, "current_pbix": get_current_pbix_meta().get("pbix_name"), "summary": data}
    )


def list_mapped_objects(status: str = "", kind: str = "", limit: int = 40) -> dict:
    """List OBJECT_MAPPING generated_objects filtered by status and/or kind.

    Args:
        status: mapped|todo|partial|skip|inactive_alias (optional)
        kind: measure|view|join (optional)
    """
    mapping = load_phase2_json("OBJECT_MAPPING.json")
    if not mapping:
        return {"found": False, "message": "OBJECT_MAPPING.json missing."}
    objs = mapping.get("generated_objects") or []
    st = (status or "").strip().lower()
    kd = (kind or "").strip().lower()
    out = []
    for o in objs:
        if st and str(o.get("status", "")).lower() != st:
            continue
        if kd and str(o.get("kind", "")).lower() != kd:
            continue
        out.append(
            {
                "kind": o.get("kind"),
                "status": o.get("status"),
                "lookml_name": o.get("lookml_name") or o.get("looker") or o.get("name"),
                "pbi_name": o.get("pbi_name") or o.get("source") or o.get("pbi"),
                "notes": (o.get("notes") or o.get("reason") or "")[:200],
            }
        )
        if len(out) >= min(limit, MAX_LIST_ITEMS):
            break
    return truncate_payload(
        {
            "found": True,
            "source_pbix": mapping.get("source_pbix"),
            "model_name": mapping.get("model_name"),
            "filter_status": status or None,
            "filter_kind": kind or None,
            "count": len(out),
            "objects": out,
        }
    )


def list_lookml_views() -> dict:
    """List generated LookML view files under phase2/lookml/views."""
    views_dir = PHASE2 / "lookml" / "views"
    if not views_dir.exists():
        return {"found": False, "message": "phase2/lookml/views missing."}
    files = sorted(p.name for p in views_dir.glob("*.view.lkml"))
    return {"found": True, "count": len(files), "views": files}


def get_user_input_placeholders() -> dict:
    """Scan phase2 LookML for YOUR_LOOKER_CONNECTION / YOUR_PROJECT placeholders and TODO markers."""
    root = PHASE2 / "lookml"
    if not root.exists():
        return {"found": False, "message": "phase2/lookml missing."}
    hits = []
    markers = (
        "YOUR_LOOKER_CONNECTION",
        "YOUR_PROJECT.YOUR_DATASET",
        "# TODO",
        "complex_todo",
    )
    for path in sorted(root.rglob("*.lkml")):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            for m in markers:
                if m in line:
                    hits.append(
                        {
                            "file": str(path.relative_to(PHASE2)),
                            "line": i,
                            "marker": m,
                            "snippet": line.strip()[:140],
                        }
                    )
                    break
            if len(hits) >= MAX_LIST_ITEMS:
                break
        if len(hits) >= MAX_LIST_ITEMS:
            break
    return truncate_payload({"found": True, "count": len(hits), "placeholders": hits})


def read_object_mapping_md(limit_chars: int = 5000) -> dict:
    """Read OBJECT_MAPPING.md excerpt for human-readable mapping notes."""
    return read_repo_text("phase2/OBJECT_MAPPING.md", limit=limit_chars)
