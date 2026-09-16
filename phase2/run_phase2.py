#!/usr/bin/env python3
"""Phase 2 orchestrator — deterministic Power BI inventory → LookML + guide + ZIP.

Usage:
  ../.venv312/bin/python run_phase2.py
  ../.venv312/bin/python run_phase2.py --inventory ../phase1/inventory
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_INV = ROOT.parent / "phase1" / "inventory"
ZIP_OUT = ROOT / "LOOKML_PROJECT.zip"


def _activate_phase2_imports() -> None:
    """Ensure phase2/lib wins (phase3 also has a package named lib)."""
    for name in list(sys.modules):
        if name == "lib" or name.startswith("lib."):
            del sys.modules[name]
    root = str(ROOT)
    while root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)


def package_zip(lookml_dir: Path, zip_path: Path) -> Path:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(lookml_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(lookml_dir.parent)))
    return zip_path


def run(inventory: Path) -> dict:
    if not inventory.exists():
        raise SystemExit(f"Phase 1 inventory not found: {inventory}")

    _activate_phase2_imports()

    import generate_developer_guide as guide
    import generate_lookml as lookml

    lookml = importlib.reload(lookml)
    guide = importlib.reload(guide)

    try:
        import generate_architecture_assets as arch_mod

        arch_mod = importlib.reload(arch_mod)
        arch_mod.main()
    except Exception as e:
        print("Architecture diagram warn:", e)

    try:
        import generate_m_migration as m_mod

        m_mod = importlib.reload(m_mod)
        m_info = m_mod.generate(inv_dir=inventory, out_dir=ROOT / "lookml" / "m_migration")
    except Exception as e:
        m_info = {"error": str(e)}
        print("M migration stubs warn:", e)

    info = lookml.generate(inv_dir=inventory, out_root=ROOT)
    guide_info = guide.generate(ROOT / "OBJECT_MAPPING.json")
    zip_path = package_zip(ROOT / "lookml", ZIP_OUT)

    summary = {
        "phase": 2,
        "approach": "deterministic",
        "source_pbix": info.get("source_pbix"),
        "model_name": info.get("model_name"),
        "fact_table": info.get("fact"),
        "views": info.get("views"),
        "measures": info.get("measures"),
        "measures_mapped": info.get("measures_mapped"),
        "measures_todo": info.get("measures_todo"),
        "dependent_measures": info.get("dependent_measures"),
        "relationships": info.get("relationships"),
        "lookml_dir": str(ROOT / "lookml"),
        "measure_dependencies": str(ROOT / "MEASURE_DEPENDENCIES.md"),
        "zip": str(zip_path),
        "guide_pdf": guide_info["pdf"],
        "guide_md": guide_info["md"],
        "mapping_md": str(ROOT / "OBJECT_MAPPING.md"),
        "m_migration": m_info,
    }
    (ROOT / "PHASE2_SUMMARY.json").write_text(json.dumps(summary, indent=2))

    print("=" * 60)
    print("PHASE 2 COMPLETE — LOOKER MAPPING + LOOKML")
    print("=" * 60)
    print(f"Source:        {summary['source_pbix']}")
    print(f"Model:         {summary['model_name']}")
    print(f"Fact explore:  {summary['fact_table']}")
    print(f"Views:         {summary['views']}")
    print(
        f"Measures:      {summary['measures']} "
        f"(mapped={summary.get('measures_mapped')}, todo={summary.get('measures_todo')}, "
        f"dependent={summary.get('dependent_measures')})"
    )
    print(f"Relationships: {summary['relationships']}")
    print(f"Dependencies:  {summary['measure_dependencies']}")
    print(f"M queries:     {m_info.get('query_count', '?')} -> lookml/m_migration/")
    print(f"Guide PDF:     {summary['guide_pdf']}")
    print(f"LookML ZIP:    {summary['zip']}")
    print(f"Mapping:       {summary['mapping_md']}")
    print(f"Architecture:  {ROOT / 'AGENTIC_ARCHITECTURE.pdf'}")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase 2: inventory → LookML + developer guide")
    ap.add_argument(
        "--inventory",
        type=Path,
        default=DEFAULT_INV,
        help="Path to Phase 1 inventory directory",
    )
    args = ap.parse_args()
    run(args.inventory.resolve())


if __name__ == "__main__":
    main()
