"""Deterministic conversion scoring from Phase 1/2/3 evidence files."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def _load(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _pbix_name(path_or_name) -> str:
    if not path_or_name:
        return ""
    return Path(str(path_or_name)).name


def score_phase1(root: Path) -> dict:
    inv = root / "phase1" / "inventory"
    counts = _load(inv / "OBJECT_COUNTS.json") or {}
    c = counts.get("counts") or {}
    tables = _load(inv / "01_tables_columns.json") or {}
    dax = _load(inv / "02_dax_objects.json") or {}
    rels = _load(inv / "03_relationships.json") or {}
    m = _load(inv / "04_power_query_m.json") or {}

    checks = [
        ("business_tables", bool(c.get("business_tables") or tables.get("tables")), 1.0),
        ("columns", bool(c.get("columns") or tables.get("columns")), 1.0),
        ("measures_inventory", bool(c.get("measures") is not None or dax.get("measures") is not None), 1.0),
        ("relationships", bool(c.get("relationships") is not None or rels.get("relationships") is not None), 1.0),
        ("power_query", bool(c.get("power_query") is not None or m.get("queries") is not None), 1.0),
        ("object_counts_file", bool(counts), 1.0),
    ]
    done = sum(w for _, ok, w in checks if ok)
    total = sum(w for _, _, w in checks)
    pct = round(100.0 * done / total, 1) if total else 0.0
    return {
        "phase": 1,
        "name": "Extract / inventory",
        "pct_done": pct,
        "pct_left": round(100.0 - pct, 1),
        "confidence": "HIGH",
        "confidence_note": "File presence + OBJECT_COUNTS evidence; extract is deterministic (pbixray).",
        "source_pbix": _pbix_name(counts.get("source_pbix")),
        "evidence": {
            "counts": c,
            "checks_passed": sum(1 for _, ok, _ in checks if ok),
            "checks_total": len(checks),
        },
        "remaining": [] if pct >= 99.9 else ["Re-run Phase 1 extract if inventory files are missing."],
    }


def score_phase2(root: Path) -> dict:
    mapping = _load(root / "phase2" / "OBJECT_MAPPING.json") or {}
    summary = _load(root / "phase2" / "PHASE2_SUMMARY.json") or {}
    objs = mapping.get("generated_objects") or []
    by_status = Counter(o.get("status") for o in objs)
    by_kind = Counter(o.get("kind") for o in objs)

    # Scoreable statuses only
    scored = [o for o in objs if o.get("status") in {"mapped", "todo", "partial", "inactive_alias", "skip"}]
    weights = {"mapped": 1.0, "partial": 0.5, "inactive_alias": 0.7, "todo": 0.0, "skip": 0.0}
    content = [o for o in scored if o.get("status") != "skip"]
    if content:
        pct = round(100.0 * sum(weights.get(o.get("status"), 0.0) for o in content) / len(content), 1)
    else:
        # Fall back to summary artifact presence
        pct = 0.0
        if summary.get("views"):
            pct = 40.0
        if (root / "phase2" / "LOOKML_PROJECT.zip").exists():
            pct = max(pct, 50.0)

    todos = [o for o in objs if o.get("status") == "todo"]
    remaining = []
    for o in todos[:40]:
        remaining.append(
            {
                "kind": o.get("kind"),
                "lookml": o.get("lookml_name") or o.get("looker") or o.get("name"),
                "pbi": o.get("pbi_name") or o.get("source") or o.get("pbi"),
                "note": o.get("notes") or o.get("reason") or "TODO in OBJECT_MAPPING",
            }
        )

    # Connection / sql_table placeholders count as remaining work (not inventing %)
    lookml_dir = root / "phase2" / "lookml"
    placeholder_files = 0
    if lookml_dir.exists():
        for p in lookml_dir.rglob("*.lkml"):
            t = p.read_text(encoding="utf-8", errors="replace")
            if "YOUR_LOOKER_CONNECTION" in t or "YOUR_PROJECT.YOUR_DATASET" in t:
                placeholder_files += 1

    return {
        "phase": 2,
        "name": "Semantic model / LookML",
        "pct_done": pct,
        "pct_left": round(100.0 - pct, 1),
        "confidence": "HIGH" if objs else "MEDIUM",
        "confidence_note": (
            "Weighted from phase2/OBJECT_MAPPING.json statuses "
            "(mapped=1.0, partial=0.5, todo=0). Placeholder connection/dataset still require user input."
        ),
        "source_pbix": _pbix_name(mapping.get("source_pbix") or summary.get("source_pbix")),
        "evidence": {
            "object_count": len(objs),
            "status_counts": dict(by_status),
            "kind_counts": dict(by_kind),
            "views": summary.get("views"),
            "measures": summary.get("measures"),
            "relationships": summary.get("relationships"),
            "placeholder_lookml_files": placeholder_files,
        },
        "remaining": remaining,
    }


def score_phase3(root: Path) -> dict:
    cov = _load(root / "phase3" / "inventory" / "COVERAGE.json") or {}
    summary = _load(root / "phase3" / "PHASE3_SUMMARY.json") or {}
    mapping = _load(root / "phase3" / "inventory" / "03_dashboard_mapping.json") or {}

    pct = cov.get("weighted_completion_pct")
    if pct is None:
        pct = summary.get("weighted_completion_pct", 0.0)
    pct = float(pct or 0.0)

    mapped = mapping.get("mapped_visuals") or []
    remaining = []
    for v in mapped:
        if v.get("status") in {"gap", "partial"}:
            remaining.append(
                {
                    "page": v.get("page"),
                    "title": v.get("pbi_title"),
                    "pbi_type": v.get("pbi_type"),
                    "status": v.get("status"),
                    "looker": v.get("looker_object"),
                    "notes": "; ".join((v.get("deficiencies") or [])[:2]) or v.get("notes"),
                }
            )

    confidence = "HIGH" if cov else ("MEDIUM" if summary else "LOW")
    return {
        "phase": 3,
        "name": "Dashboards / visuals",
        "pct_done": round(pct, 1),
        "pct_left": round(100.0 - pct, 1),
        "confidence": confidence,
        "confidence_note": (
            "Weighted visual coverage from phase3/inventory/COVERAGE.json "
            "(decorative skips excluded; mapped/partial/gap weights fixed)."
        ),
        "source_pbix": _pbix_name(cov.get("source_pbix") or summary.get("source_pbix")),
        "evidence": {
            "visual_total": cov.get("visual_total") or summary.get("visuals"),
            "status_counts": cov.get("status_counts") or summary.get("status_counts"),
            "dashboards": summary.get("dashboards"),
            "target_pct": cov.get("target_pct", 70),
            "meets_target": cov.get("meets_target", summary.get("meets_target")),
        },
        "remaining": remaining[:60],
    }


def overall_score(p1: dict, p2: dict, p3: dict) -> dict:
    """Overall = weighted mean of phases that have evidence.

    Weights reflect migration effort: model (P2) and dashboards (P3) dominate.
    """
    parts = []
    # Always include phase if evidence present
    if p1["evidence"].get("checks_total"):
        parts.append((p1["pct_done"], 0.15, "phase1"))
    if (p2["evidence"].get("object_count") or 0) > 0 or p2["pct_done"] > 0:
        parts.append((p2["pct_done"], 0.45, "phase2"))
    if (p3["evidence"].get("visual_total") or 0) > 0 or p3["pct_done"] > 0:
        parts.append((p3["pct_done"], 0.40, "phase3"))

    if not parts:
        return {
            "pct_done": 0.0,
            "pct_left": 100.0,
            "confidence": "LOW",
            "weights": {},
            "formula": "no evidence",
        }

    wsum = sum(w for _, w, _ in parts)
    done = sum(pct * w for pct, w, _ in parts) / wsum
    confs = {p1["confidence"], p2["confidence"], p3["confidence"]}
    if "LOW" in confs:
        conf = "LOW"
    elif "MEDIUM" in confs:
        conf = "MEDIUM"
    else:
        conf = "HIGH"

    # PBIX mismatch lowers confidence
    sources = {s for s in [p1.get("source_pbix"), p2.get("source_pbix"), p3.get("source_pbix")] if s}
    warning = None
    if len(sources) > 1:
        conf = "MEDIUM"
        warning = (
            "Phase source PBIX names differ — overall % mixes different reports. "
            f"Sources seen: {sorted(sources)}"
        )

    return {
        "pct_done": round(done, 1),
        "pct_left": round(100.0 - done, 1),
        "confidence": conf,
        "weights": {name: round(w / wsum, 3) for _, w, name in parts},
        "formula": "0.15*P1 + 0.45*P2 + 0.40*P3 (renormalized if a phase is missing)",
        "warning": warning,
        "source_pbix_set": sorted(sources),
    }
