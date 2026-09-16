#!/usr/bin/env python3
"""Validation orchestrator — evidence-based conversion % + LookML user-input report.

Usage:
  ../.venv312/bin/python run_validation.py
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def run() -> dict:
    import generate_validation_report as gen

    gen = importlib.reload(gen)
    report = gen.generate()
    summary = {
        "phase": "validation",
        "approach": "deterministic_evidence",
        "overall_pct_done": report["overall"]["pct_done"],
        "overall_pct_left": report["overall"]["pct_left"],
        "confidence": report["overall"]["confidence"],
        "phase1_pct": report["phases"]["phase1"]["pct_done"],
        "phase2_pct": report["phases"]["phase2"]["pct_done"],
        "phase3_pct": report["phases"]["phase3"]["pct_done"],
        "user_input_findings": report["user_input_required"]["summary"]["total_findings"],
        "high_priority": report["user_input_required"]["summary"]["by_severity"].get("HIGH", 0),
        "report_pdf": str(ROOT / "VALIDATION_REPORT.pdf"),
        "report_md": str(ROOT / "VALIDATION_REPORT.md"),
        "report_json": str(ROOT / "VALIDATION_REPORT.json"),
        "warning": report["overall"].get("warning"),
    }
    (ROOT / "VALIDATION_SUMMARY.json").write_text(json.dumps(summary, indent=2))
    print("=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    print(f"Overall done:  {summary['overall_pct_done']}%")
    print(f"Overall left:  {summary['overall_pct_left']}%")
    print(f"Confidence:    {summary['confidence']}")
    print(f"P1 / P2 / P3:  {summary['phase1_pct']}% / {summary['phase2_pct']}% / {summary['phase3_pct']}%")
    print(f"User inputs:   {summary['user_input_findings']} markers ({summary['high_priority']} HIGH)")
    print(f"PDF:           {summary['report_pdf']}")
    if summary.get("warning"):
        print(f"WARNING:       {summary['warning']}")
    return summary


if __name__ == "__main__":
    run()
