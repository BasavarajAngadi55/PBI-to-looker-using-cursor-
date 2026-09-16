#!/usr/bin/env python3
"""Map Power BI visuals → LookML dashboards (deterministic, best-effort ~70% target).

Reads phase3/inventory visuals + Phase 2 model/explore hints.
Writes:
  inventory/03_dashboard_mapping.json
  inventory/COVERAGE.json
  lookml_dashboards/dashboards/*.dashboard.lookml
  comparison/PAGE_COMPARISON.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from lib.naming import lookml_field_name, lookml_field_ref, lookml_view_name, snake_case
from lib.visual_mapping import equivalence_table, map_visual_type

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
PHASE1 = ROOT.parent / "phase1"
PHASE2 = ROOT.parent / "phase2"
DASH_DIR = ROOT / "lookml_dashboards" / "dashboards"
CMP_DIR = ROOT / "comparison"


def _load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def _phase2_context() -> dict:
    summary = _load(PHASE2 / "PHASE2_SUMMARY.json")
    counts = _load(PHASE1 / "inventory" / "OBJECT_COUNTS.json")
    src = summary.get("source_pbix") or counts.get("source_pbix") or "PBIX"
    model = summary.get("model_name") or snake_case(Path(str(src)).stem)
    fact = summary.get("fact_table") or "FactTable"
    explore = lookml_view_name(fact)
    return {
        "model": model,
        "explore": explore,
        "fact_table": fact,
        "measure_host_view": explore,
        "source_pbix": src,
    }


def _yaml_escape(s: str) -> str:
    return (s or "").replace(":", " -").replace("\n", " ").strip()


def _pos(visual: dict) -> dict:
    page_w = float(visual.get("page_width") or 1280)
    page_h = float(visual.get("page_height") or 720)
    x = float(visual.get("x") or 0)
    y = float(visual.get("y") or 0)
    w = float(visual.get("width") or page_w / 4)
    h = float(visual.get("height") or page_h / 4)
    col = max(0, min(23, int(round(x / page_w * 24))))
    width = max(2, min(24 - col, int(round(w / page_w * 24))))
    # Looker newspaper rows are flexible; scale to ~12-16 row grid
    row = max(0, int(round(y / page_h * 16)))
    height = max(2, int(round(h / page_h * 16)))
    return {"col": col, "width": width, "row": row, "height": height}


def _bind_fields(fields: list[dict], ctx: dict) -> tuple[list[str], list[str], list[str]]:
    """Return dimensions, measures, gaps for LookML dashboard element."""
    dims: list[str] = []
    measures: list[str] = []
    gaps: list[str] = []
    host = ctx["measure_host_view"]
    for f in fields or []:
        kind = f.get("kind")
        prop = f.get("property")
        table = f.get("table")
        if not prop:
            gaps.append(f"unbound field {f.get('native')}")
            continue
        if kind == "measure":
            measures.append(lookml_field_ref(table or "Measure Table", prop, host))
        elif kind in {"column", "aggregation"}:
            # aggregations on columns → treat as measure on same view if possible
            if kind == "aggregation":
                # Prefer a generated sum measure name; fall back to dimension + note
                ref_view = lookml_view_name(table) if table else host
                # Use field as measure name guess: sum_col or the column itself if measure exists
                measures.append(f"{ref_view}.{lookml_field_name(prop)}")
                gaps.append(
                    f"PBI aggregation on {table}.{prop} mapped to field ref; "
                    f"confirm a measure exists on {ref_view} (Phase 2) or add type:sum"
                )
            else:
                # date dimension_groups in Looker often need _date suffix — keep base name
                dims.append(lookml_field_ref(table or host, prop, host))
        else:
            gaps.append(f"unsupported select kind={kind} native={f.get('native')}")
    # de-dupe preserve order
    def uniq(xs):
        seen = set()
        out = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return uniq(dims), uniq(measures), gaps


def map_visuals(visuals: list[dict], ctx: dict) -> list[dict]:
    mapped = []
    for i, v in enumerate(visuals):
        vm = map_visual_type(v.get("visual_type") or "")
        dims, meas, field_gaps = _bind_fields(v.get("fields") or [], ctx)
        status = vm.status
        weight = vm.coverage_weight
        deficiencies = list(field_gaps)
        # slicers become filters
        element = None
        looker_type = vm.looker_type
        if vm.pbi_type == "slicer":
            element = "filter"
            if not dims and not meas:
                deficiencies.append("slicer has no bound field")
                status = "gap"
                weight = 0.0
            else:
                status = "mapped"
                weight = 1.0
        elif status == "skip":
            element = None
        elif looker_type is None:
            element = None
            status = "gap"
            weight = 0.0
        else:
            element = "tile"
            if looker_type != "text" and not dims and not meas:
                deficiencies.append("no fields bound from prototypeQuery — tile will be incomplete")
                status = "partial" if status == "mapped" else status
                weight = min(weight, 0.4)
            if looker_type == "looker_map" and not any("lat" in d or "long" in d or "zip" in d for d in dims):
                deficiencies.append("map may lack location dimension — verify geo fields")
                status = "partial"
                weight = min(weight, 0.5)

        mapped.append(
            {
                "id": f"p{v.get('page','x')}_{i}_{snake_case(v.get('visual_type') or 'v')}",
                "page": v.get("page"),
                "pbi_title": v.get("title"),
                "pbi_type": v.get("visual_type"),
                "looker_type": looker_type,
                "looker_object": vm.looker_object,
                "element_kind": element,
                "status": status,
                "coverage_weight": weight,
                "notes": vm.notes,
                "dimensions": dims,
                "measures": meas,
                "deficiencies": deficiencies,
                "position": _pos(v),
                "entities": v.get("entities") or [],
            }
        )
    return mapped


def _render_dashboard(page_name: str, items: list[dict], ctx: dict, filters: list[dict]) -> str:
    dash_name = snake_case(page_name) or "page"
    lines = [
        f"- dashboard: {dash_name}",
        f"  title: {_yaml_escape(page_name)}",
        "  layout: newspaper",
        "  preferred_viewer: dashboards-next",
        "  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'",
        "",
    ]
    if filters:
        lines.append("  filters:")
        for f in filters:
            lines.append(f"  - name: {f['name']}")
            lines.append(f"    title: '{_yaml_escape(f['title'])}'")
            lines.append(f"    type: field_filter")
            lines.append(f"    model: {ctx['model']}")
            lines.append(f"    explore: {ctx['explore']}")
            lines.append(f"    field: {f['field']}")
            lines.append("    default_value: ''")
            lines.append("")

    lines.append("  elements:")
    # coverage note tile
    lines.append("  - name: migration_notes")
    lines.append(f"    title: 'Migration notes — {_yaml_escape(page_name)}'")
    lines.append("    type: text")
    lines.append("    body_text_as_html: true")
    note = (
        f"Migrated from Power BI page <b>{_yaml_escape(page_name)}</b>. "
        f"Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. "
        f"Model: <code>{ctx['model']}</code> / Explore: <code>{ctx['explore']}</code>."
    )
    lines.append(f"    body_text: '{note}'")
    lines.append("    row: 0")
    lines.append("    col: 0")
    lines.append("    width: 24")
    lines.append("    height: 2")
    lines.append("")

    row_cursor = 2
    for it in items:
        if it["element_kind"] != "tile" or not it.get("looker_type"):
            continue
        name = snake_case(it["id"])[:60]
        pos = it["position"]
        # stack if overlapping badly — use computed row but ensure after notes
        r = max(row_cursor, pos["row"] + 2)
        lines.append(f"  - name: {name}")
        lines.append(f"    title: '{_yaml_escape(it.get('pbi_title') or it['pbi_type'])}'")
        lines.append(f"    type: {it['looker_type']}")
        lines.append(f"    model: {ctx['model']}")
        lines.append(f"    explore: {ctx['explore']}")
        if it["looker_type"] == "text":
            body = _yaml_escape(it.get("pbi_title") or "Text from Power BI")
            lines.append(f"    body_text: '{body}'")
        else:
            if it["dimensions"]:
                lines.append("    dimensions: [" + ", ".join(it["dimensions"]) + "]")
            if it["measures"]:
                lines.append("    measures: [" + ", ".join(it["measures"]) + "]")
            if not it["dimensions"] and not it["measures"]:
                # still emit explore-only single_value placeholder
                lines.append(f"    # DEFICIENCY: no fields — using explore count as placeholder")
                lines.append(f"    measures: [{ctx['explore']}.count]")
            if filters:
                lines.append("    listen:")
                for f in filters:
                    lines.append(f"      {f['name']}: {f['field']}")
        lines.append(f"    row: {r}")
        lines.append(f"    col: {pos['col']}")
        lines.append(f"    width: {pos['width']}")
        lines.append(f"    height: {max(3, pos['height'])}")
        if it["deficiencies"] or it["status"] != "mapped":
            lines.append(f"    # status={it['status']} | {it['notes']}")
            for d in it["deficiencies"][:3]:
                lines.append(f"    # deficiency: {_yaml_escape(d)[:120]}")
        lines.append("")
        row_cursor = r + max(3, pos["height"])

    # gap summary text tile at end
    gaps = [it for it in items if it["status"] in {"gap", "partial", "skip"}]
    if gaps:
        lines.append("  - name: remaining_gaps")
        lines.append("    title: 'Gaps / partials (not fully migrated)'")
        lines.append("    type: text")
        lines.append("    body_text_as_html: true")
        bits = []
        for g in gaps[:25]:
            bits.append(
                f"<li><b>{_yaml_escape(g.get('pbi_title') or g['pbi_type'])}</b> "
                f"({g['pbi_type']} → {g['looker_object']}) — {g['status']}</li>"
            )
        body = "<ul>" + "".join(bits) + "</ul>"
        lines.append(f"    body_text: '{body}'")
        lines.append(f"    row: {row_cursor + 1}")
        lines.append("    col: 0")
        lines.append("    width: 24")
        lines.append("    height: 4")
        lines.append("")

    return "\n".join(lines) + "\n"


def generate() -> dict:
    visuals_payload = _load(INV / "02_visuals.json")
    pages_payload = _load(INV / "01_report_pages.json")
    visuals = visuals_payload.get("visuals") or []
    ctx = _phase2_context()
    mapped = map_visuals(visuals, ctx)

    # coverage
    content = [m for m in mapped if m["status"] != "skip"]
    skip_n = sum(1 for m in mapped if m["status"] == "skip")
    if content:
        score = sum(m["coverage_weight"] for m in content) / len(content)
    else:
        score = 0.0
    pct = round(100 * score, 1)
    by_status = Counter(m["status"] for m in mapped)
    by_type = Counter(m["pbi_type"] for m in mapped)

    coverage = {
        "source_pbix": ctx["source_pbix"],
        "model": ctx["model"],
        "explore": ctx["explore"],
        "visual_total": len(mapped),
        "content_visuals": len(content),
        "skipped_decorative": skip_n,
        "mapped_visuals": by_status.get("mapped", 0),
        "partial_visuals": by_status.get("partial", 0),
        "gap_visuals": by_status.get("gap", 0),
        "status_counts": dict(by_status),
        "pbi_type_counts": dict(by_type),
        "weighted_completion_pct": pct,
        "target_pct": 70,
        "meets_target": pct >= 70,
        "method": (
            "weighted: mapped=1.0, partial≈0.5–0.8, gap=0, skip excluded from denominator"
        ),
        "equivalence": equivalence_table(),
    }

    INV.mkdir(parents=True, exist_ok=True)
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    CMP_DIR.mkdir(parents=True, exist_ok=True)
    for p in DASH_DIR.glob("*.dashboard.lookml"):
        p.unlink()

    (INV / "03_dashboard_mapping.json").write_text(
        json.dumps({"context": ctx, "mapped_visuals": mapped}, indent=2)
    )
    (INV / "COVERAGE.json").write_text(json.dumps(coverage, indent=2))

    # filters from slicers per page
    by_page: dict[str, list] = defaultdict(list)
    for m in mapped:
        by_page[m["page"]].append(m)

    dash_files = []
    for page_name, items in by_page.items():
        filters = []
        for it in items:
            if it["element_kind"] == "filter" and it["status"] == "mapped":
                field = (it["dimensions"] or it["measures"] or [None])[0]
                if not field:
                    continue
                filters.append(
                    {
                        "name": snake_case(f"f_{it['pbi_title'] or field}")[:40],
                        "title": it.get("pbi_title") or field,
                        "field": field,
                    }
                )
        # de-dupe filters by field
        seen_f = set()
        uniq_filters = []
        for f in filters:
            if f["field"] in seen_f:
                continue
            seen_f.add(f["field"])
            uniq_filters.append(f)

        body = _render_dashboard(page_name, items, ctx, uniq_filters)
        fname = f"{snake_case(page_name)}.dashboard.lookml"
        (DASH_DIR / fname).write_text(body)
        dash_files.append(fname)

    # comparison markdown
    lines = [
        "# Power BI page → Looker dashboard comparison",
        "",
        f"**Source:** `{Path(str(ctx['source_pbix'])).name}`  ",
        f"**Looker model/explore:** `{ctx['model']}` / `{ctx['explore']}`  ",
        f"**Weighted completion:** **{pct}%** (target ≥ 70%: {'YES' if pct >= 70 else 'NOT YET'})",
        "",
        "## Status summary",
        "",
        f"- Total visuals: {len(mapped)} (decorative skips: {skip_n})",
        f"- Status counts: {dict(by_status)}",
        "",
        "## Visual type equivalence",
        "",
        "| Power BI | Looker | Status | Notes |",
        "|---|---|---|---|",
    ]
    for row in equivalence_table():
        lines.append(
            f"| `{row['pbi_type']}` | `{row['looker_object']}` | {row['status']} | {row['notes']} |"
        )

    for page_name, items in by_page.items():
        lines += ["", f"## Page: {page_name}", "", "| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |", "|---|---|---|---|---|"]
        for it in items:
            defs = "; ".join(it["deficiencies"][:2]) if it["deficiencies"] else "-"
            lines.append(
                f"| {it.get('pbi_title') or '-'} | `{it['pbi_type']}` | `{it['looker_object']}` | {it['status']} | {defs} |"
            )

    lines += [
        "",
        "## Looker dashboard files",
        "",
    ]
    for f in dash_files:
        lines.append(f"- `lookml_dashboards/dashboards/{f}`")
    lines.append("")
    (CMP_DIR / "PAGE_COMPARISON.md").write_text("\n".join(lines))

    # README for lookml_dashboards
    (ROOT / "lookml_dashboards" / "README.md").write_text(
        "# LookML dashboards (Phase 3)\n\n"
        f"Model: `{ctx['model']}`  Explore: `{ctx['explore']}`\n\n"
        "Import these `.dashboard.lookml` files into the same Looker project as Phase 2 views/model.\n"
        "Update connection/warehouse first (Phase 2). Validate LookML; expect field errors until measures exist.\n"
        f"Reported weighted completion: **{pct}%**.\n"
    )

    print("Wrote mapping, coverage, dashboards:", len(dash_files), "completion", pct, "%")
    return {"dashboards": len(dash_files), "completion_pct": pct, "coverage": coverage}


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2)[:2000])
