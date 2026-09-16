#!/usr/bin/env python3
"""Phase 3 orchestrator — deterministic PBIX report → LookML dashboards.

Usage:
  ../.venv312/bin/python run_phase3.py
  ../.venv312/bin/python run_phase3.py --pbix ../phase1/uploads/dashboards.pbix
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

ZIP_OUT = ROOT / "LOOKML_DASHBOARDS.zip"
SUMMARY_OUT = ROOT / "PHASE3_SUMMARY.json"


def package_zip() -> Path:
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    with zipfile.ZipFile(ZIP_OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        dash_root = ROOT / "lookml_dashboards"
        for path in sorted(dash_root.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(ROOT)))
        cmp = ROOT / "comparison" / "PAGE_COMPARISON.md"
        if cmp.exists():
            zf.write(cmp, arcname="comparison/PAGE_COMPARISON.md")
        cov = ROOT / "inventory" / "COVERAGE.json"
        if cov.exists():
            zf.write(cov, arcname="inventory/COVERAGE.json")
        guide_md = ROOT / "DASHBOARD_DEVELOPER_GUIDE.md"
        if guide_md.exists():
            zf.write(guide_md, arcname="DASHBOARD_DEVELOPER_GUIDE.md")
        guide_pdf = ROOT / "DASHBOARD_DEVELOPER_GUIDE.pdf"
        if guide_pdf.exists():
            zf.write(guide_pdf, arcname="DASHBOARD_DEVELOPER_GUIDE.pdf")
    return ZIP_OUT


def run(pbix: Path | None = None) -> dict:
    import extract_report_layout as extract_mod
    import generate_lookml_dashboards as dash_mod

    extract_mod = importlib.reload(extract_mod)
    dash_mod = importlib.reload(dash_mod)

    try:
        import generate_architecture_assets as arch_mod

        arch_mod = importlib.reload(arch_mod)
        arch_mod.main()
    except Exception as e:
        print("Architecture diagram warn:", e)

    extract_info = extract_mod.extract(pbix)
    gen_info = dash_mod.generate()

    try:
        import generate_dashboard_guide as guide_mod

        guide_mod = importlib.reload(guide_mod)
        guide_mod.main()
    except Exception as e:
        print("Dashboard guide warn:", e)

    zip_path = package_zip()
    coverage = gen_info.get("coverage") or {}
    pct = gen_info.get("completion_pct", coverage.get("weighted_completion_pct", 0))

    summary = {
        "phase": 3,
        "approach": "deterministic",
        "source_pbix": extract_info.get("pbix"),
        "pages": extract_info.get("pages"),
        "visuals": extract_info.get("visuals"),
        "dashboards": gen_info.get("dashboards"),
        "weighted_completion_pct": pct,
        "target_pct": 70,
        "meets_target": bool(pct >= 70),
        "model": coverage.get("model"),
        "explore": coverage.get("explore"),
        "status_counts": coverage.get("status_counts"),
        "zip": str(zip_path),
        "guide_pdf": str(ROOT / "DASHBOARD_DEVELOPER_GUIDE.pdf"),
        "guide_md": str(ROOT / "DASHBOARD_DEVELOPER_GUIDE.md"),
        "comparison": str(ROOT / "comparison" / "PAGE_COMPARISON.md"),
        "architecture_pdf": str(ROOT / "AGENTIC_ARCHITECTURE.pdf"),
        "lookml_dir": str(ROOT / "lookml_dashboards"),
    }
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2))

    print("=" * 60)
    print("PHASE 3 COMPLETE — LOOKER DASHBOARDS")
    print("=" * 60)
    print(f"Source:        {summary['source_pbix']}")
    print(f"Pages:         {summary['pages']}")
    print(f"Visuals:       {summary['visuals']}")
    print(f"Dashboards:    {summary['dashboards']}")
    print(f"Completion:    {pct}% (target >= 70%: {'YES' if pct >= 70 else 'NOT YET'})")
    print(f"Model/explore: {summary.get('model')} / {summary.get('explore')}")
    print(f"Guide PDF:     {summary['guide_pdf']}")
    print(f"Dashboards ZIP:{summary['zip']}")
    print(f"Comparison:    {summary['comparison']}")
    print(f"Architecture:  {summary['architecture_pdf']}")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase 3: PBIX report → LookML dashboards")
    ap.add_argument("--pbix", type=Path, default=None, help="Path to PBIX (optional)")
    args = ap.parse_args()
    pbix = args.pbix.resolve() if args.pbix else None
    run(pbix)


if __name__ == "__main__":
    main()
