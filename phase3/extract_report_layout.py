#!/usr/bin/env python3
"""Extract Power BI report pages/visuals from PBIX Report/Layout (deterministic)."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHASE1 = ROOT.parent / "phase1"
INV = ROOT / "inventory"

_NON_ALNUM = re.compile(r"[^a-zA-Z0-9]+")


def _slug(name: str) -> str:
    s = _NON_ALNUM.sub("_", str(name or "page")).strip("_").lower()
    return s or "page"


def resolve_pbix(pbix: Path | None = None) -> Path:
    if pbix and pbix.exists():
        return pbix
    meta = PHASE1 / "CURRENT_PBIX.json"
    if meta.exists():
        p = Path(json.loads(meta.read_text()).get("pbix_path") or "")
        if p.exists():
            return p
    uploads = list((PHASE1 / "uploads").glob("*.pbix"))
    if len(uploads) == 1:
        return uploads[0]
    if uploads:
        return max(uploads, key=lambda x: x.stat().st_mtime)
    raise FileNotFoundError("No PBIX found. Upload via Phase 1 UI or pass --pbix")


def read_layout_json(pbix: Path) -> dict:
    with zipfile.ZipFile(pbix, "r") as z:
        # Layout path is typically Report/Layout
        name = next((n for n in z.namelist() if n.replace("\\", "/").endswith("Report/Layout")), None)
        if not name:
            raise FileNotFoundError(f"Report/Layout not found in {pbix.name}")
        raw = z.read(name)
    # PBIX Layout is UTF-16-LE JSON
    if raw[:2] == b"\xff\xfe" or (len(raw) > 3 and raw[1] == 0):
        text = raw.decode("utf-16-le")
    else:
        text = raw.decode("utf-8")
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    return json.loads(text)


def _parse_maybe_json(val):
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return val
    return val


def _title_from_single_visual(sv: dict) -> str | None:
    # vcObjects.title[0].properties.text.expr.Literal.Value = "'My Title'"
    vc = sv.get("vcObjects") or {}
    title_arr = vc.get("title") or []
    if isinstance(title_arr, list) and title_arr:
        props = (title_arr[0] or {}).get("properties") or {}
        text = ((props.get("text") or {}).get("expr") or {}).get("Literal") or {}
        val = text.get("Value")
        if isinstance(val, str):
            return val.strip("'").strip('"')
    # Fallback: visualContainerObjects title
    vco = sv.get("visualContainerObjects") or {}
    title_arr = vco.get("title") or []
    if isinstance(title_arr, list) and title_arr:
        props = (title_arr[0] or {}).get("properties") or {}
        text = ((props.get("text") or {}).get("expr") or {}).get("Literal") or {}
        val = text.get("Value")
        if isinstance(val, str):
            return val.strip("'").strip('"')
    return None


def _textbox_content(sv: dict) -> str | None:
    """Best-effort plain text from a textbox visual."""
    objs = sv.get("objects") or {}
    # Common path: general / paragraphs
    for key in ("general", "title", "labels"):
        arr = objs.get(key) or []
        if not isinstance(arr, list):
            continue
        for item in arr:
            props = (item or {}).get("properties") or {}
            for pval in props.values():
                if not isinstance(pval, dict):
                    continue
                expr = pval.get("expr") or {}
                lit = expr.get("Literal") or {}
                val = lit.get("Value")
                if isinstance(val, str) and len(val.strip("'\"")) > 1:
                    return val.strip("'").strip('"')
    return None


def _walk_select(select_items: list) -> list[dict]:
    fields = []
    for item in select_items or []:
        if not isinstance(item, dict):
            continue
        native = item.get("NativeReferenceName") or item.get("Name")
        if "Measure" in item:
            m = item["Measure"]
            prop = m.get("Property")
            # source entity via From alias resolved later
            fields.append({"kind": "measure", "property": prop, "native": native, "raw": item})
        elif "Column" in item:
            c = item["Column"]
            fields.append({"kind": "column", "property": c.get("Property"), "native": native, "raw": item})
        elif "Aggregation" in item:
            agg = item["Aggregation"]
            expr = agg.get("Expression") or {}
            col = (expr.get("Column") or {}) if isinstance(expr, dict) else {}
            fields.append(
                {
                    "kind": "aggregation",
                    "property": col.get("Property"),
                    "function": agg.get("Function"),
                    "native": native,
                    "raw": item,
                }
            )
        else:
            fields.append({"kind": "other", "native": native, "raw": item})
    return fields


def _resolve_sources(from_list: list) -> dict[str, str]:
    """alias -> Entity name"""
    out = {}
    for f in from_list or []:
        if isinstance(f, dict) and f.get("Name") and f.get("Entity"):
            out[f["Name"]] = f["Entity"]
    return out


def _attach_entities(fields: list[dict], alias_map: dict[str, str]) -> list[dict]:
    enriched = []
    for f in fields:
        raw = f.get("raw") or {}
        entity = None
        # dig SourceRef.Source
        blob = json.dumps(raw)

        def find_source(obj):
            if isinstance(obj, dict):
                if "SourceRef" in obj and isinstance(obj["SourceRef"], dict):
                    return obj["SourceRef"].get("Source")
                for v in obj.values():
                    s = find_source(v)
                    if s:
                        return s
            elif isinstance(obj, list):
                for v in obj:
                    s = find_source(v)
                    if s:
                        return s
            return None

        alias = find_source(raw)
        if alias and alias in alias_map:
            entity = alias_map[alias]
        item = {k: v for k, v in f.items() if k != "raw"}
        item["table"] = entity
        item["alias"] = alias
        enriched.append(item)
    return enriched


def extract_visual(vc: dict, page_name: str, ordinal: int) -> dict:
    cfg = _parse_maybe_json(vc.get("config")) or {}
    if not isinstance(cfg, dict):
        cfg = {}
    sv = cfg.get("singleVisual") or {}
    if not isinstance(sv, dict):
        sv = {}
    vtype = sv.get("visualType") or "unknown"
    pq = sv.get("prototypeQuery") or {}
    alias_map = _resolve_sources(pq.get("From") or [])
    fields = _attach_entities(_walk_select(pq.get("Select") or []), alias_map)
    title = _title_from_single_visual(sv)
    if not title and vtype == "textbox":
        title = _textbox_content(sv)
    if not title:
        # Prefer field-based label over opaque config name GUIDs
        field_label = None
        for f in fields:
            if f.get("property"):
                field_label = f.get("property")
                break
        cfg_name = cfg.get("name")
        if isinstance(cfg_name, str) and len(cfg_name) >= 20 and all(c in "0123456789abcdef" for c in cfg_name.lower()):
            title = field_label or f"{vtype}_{ordinal}"
        else:
            title = cfg_name or field_label or f"{vtype}_{ordinal}"
    return {
        "page": page_name,
        "ordinal": ordinal,
        "visual_type": vtype,
        "title": title,
        "x": vc.get("x"),
        "y": vc.get("y"),
        "width": vc.get("width"),
        "height": vc.get("height"),
        "z": vc.get("z"),
        "fields": fields,
        "entities": sorted(set(alias_map.values())),
        "projections": list((sv.get("projections") or {}).keys()) if isinstance(sv.get("projections"), dict) else [],
    }


def extract(pbix: Path | None = None) -> dict:
    path = resolve_pbix(pbix)
    layout = read_layout_json(path)
    sections = layout.get("sections") or []
    pages = []
    visuals = []
    for s in sections:
        page_name = s.get("displayName") or s.get("name") or "Page"
        page_w = s.get("width") or 1280
        page_h = s.get("height") or 720
        page_visuals = []
        for i, vc in enumerate(s.get("visualContainers") or []):
            vis = extract_visual(vc, page_name, i)
            vis["page_width"] = page_w
            vis["page_height"] = page_h
            page_visuals.append(vis)
            visuals.append(vis)
        pages.append(
            {
                "name": page_name,
                "display_name": page_name,
                "slug": _slug(page_name),
                "ordinal": s.get("ordinal"),
                "width": page_w,
                "height": page_h,
                "visual_count": len(page_visuals),
                "filter_blob_present": bool(s.get("filters")),
            }
        )

    INV.mkdir(parents=True, exist_ok=True)
    pages_path = INV / "01_report_pages.json"
    visuals_path = INV / "02_visuals.json"
    payload_pages = {"source_pbix": str(path), "page_count": len(pages), "pages": pages}
    payload_visuals = {
        "source_pbix": str(path),
        "visual_count": len(visuals),
        "visuals": visuals,
    }
    pages_path.write_text(json.dumps(payload_pages, indent=2))
    visuals_path.write_text(json.dumps(payload_visuals, indent=2))
    print("Wrote", pages_path)
    print("Wrote", visuals_path)
    return {"pbix": str(path), "pages": len(pages), "visuals": len(visuals)}


if __name__ == "__main__":
    print(json.dumps(extract(), indent=2))
