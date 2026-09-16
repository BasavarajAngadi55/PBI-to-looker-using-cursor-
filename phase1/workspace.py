#!/usr/bin/env python3
"""Keep phase1 workspace dynamic: only current PBIX artifacts, no backups."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
M_RAW = INV / "04_m_raw"
UPLOADS = ROOT / "uploads"

# Regenerated on every extract for the active PBIX only
DYNAMIC_ROOT_FILES = [
    "DATA_MODEL.md",
    "DATA_MODEL.pdf",
    "DATA_MODEL.png",
    "DATA_MODEL_ER.png",
    "OBJECT_SUMMARY.pdf",
    "AGENT_VALIDATION_PROOF.md",
    "AGENT_VALIDATION_PROOF.pdf",
    "AGENT_VALIDATION_PROOF.png",
    "CURRENT_PBIX.json",
]

DYNAMIC_INV_FILES = [
    "01_tables_columns.json",
    "02_dax_objects.json",
    "03_relationships.json",
    "04_power_query_m.json",
    "05_tmschema_extras.json",
    "OBJECT_INVENTORY.md",
    "OBJECT_COUNTS.json",
    "OBJECT_SUMMARY.txt",
    "AGENT_VALIDATION_PROOF.json",
    "CURRENT_PBIX.json",
]


def reset_dynamic_outputs() -> None:
    """Wipe previous PBIX extract outputs inside phase1/ (no backup folders)."""
    for name in DYNAMIC_ROOT_FILES:
        p = ROOT / name
        if p.exists():
            p.unlink()

    for name in DYNAMIC_INV_FILES:
        p = INV / name
        if p.exists():
            p.unlink()

    if M_RAW.exists():
        shutil.rmtree(M_RAW)
    M_RAW.mkdir(parents=True, exist_ok=True)

    # Only keep tooling docs; clear any leftover caches
    for cache in (ROOT / "__pycache__", INV / "__pycache__"):
        if cache.exists():
            shutil.rmtree(cache, ignore_errors=True)


def set_current_pbix(pbix_path: Path) -> Path:
    """
    Store exactly one PBIX under phase1/uploads/ and record it as current.
    Removes any other uploaded .pbix files.
    """
    UPLOADS.mkdir(parents=True, exist_ok=True)
    pbix_path = Path(pbix_path).expanduser().resolve()
    if not pbix_path.exists():
        raise FileNotFoundError(f"PBIX not found: {pbix_path}")
    if pbix_path.suffix.lower() != ".pbix":
        raise ValueError("File must be a .pbix")

    target = UPLOADS / pbix_path.name
    if pbix_path.resolve() != target.resolve():
        shutil.copy2(pbix_path, target)

    # Remove other pbix files from uploads so only current remains
    for p in UPLOADS.glob("*.pbix"):
        if p.resolve() != target.resolve():
            p.unlink()

    meta = {
        "pbix_name": target.name,
        "pbix_path": str(target),
        "source_original": str(pbix_path),
        "size_bytes": target.stat().st_size,
    }
    (INV / "CURRENT_PBIX.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (ROOT / "CURRENT_PBIX.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return target
