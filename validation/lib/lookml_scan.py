"""Scan LookML for placeholders and user-required edits."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

PLACEHOLDER_PATTERNS: list[tuple[str, str, str]] = [
    (
        r'connection:\s*"YOUR_LOOKER_CONNECTION"',
        "HIGH",
        "Set Looker connection name (Admin > Connections)",
    ),
    (
        r"YOUR_PROJECT\.YOUR_DATASET",
        "HIGH",
        "Replace BigQuery project.dataset in sql_table_name",
    ),
    (
        r"YOUR_PROJECT\.SOURCE_DATASET",
        "HIGH",
        "Replace source dataset for warehouse SQL / M migration",
    ),
    (
        r"#\s*TODO",
        "MEDIUM",
        "Resolve TODO — complex DAX / parity / missing logic",
    ),
    (
        r"complex_todo",
        "MEDIUM",
        "Measure stubbed as complex_todo — implement SQL + KPI parity",
    ),
    (
        r"KPI parity not yet validated",
        "MEDIUM",
        "Explore/view notes KPI parity still required",
    ),
    (
        r"sql_trigger:.*YOUR_PROJECT",
        "LOW",
        "Enable/fix datagroup sql_trigger after warehouse load",
    ),
    (
        r"description:\s*\"Migrated from Power BI",
        "LOW",
        "Optional: rewrite explore/dashboard description for end users",
    ),
    (
        r"#\s*deficiency:",
        "MEDIUM",
        "Dashboard tile deficiency — verify field or replace gap tile",
    ),
    (
        r"preferred_viewer:\s*dashboards-next",
        "LOW",
        "Confirm dashboards-next is enabled in your Looker instance",
    ),
]


@dataclass
class Finding:
    severity: str
    category: str
    file: str
    line: int
    snippet: str
    action: str


def scan_lookml_trees(roots: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".lkml", ".lookml", ".sql", ".md"}:
                continue
            # Skip huge binary-ish / generated zip companions
            if path.name.endswith(".zip"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            lines = text.splitlines()
            rel = str(path)
            for i, line in enumerate(lines, start=1):
                for pat, sev, action in PLACEHOLDER_PATTERNS:
                    if re.search(pat, line):
                        key = (rel, i, pat)
                        if key in seen:
                            continue
                        seen.add(key)
                        findings.append(
                            Finding(
                                severity=sev,
                                category=_category(pat),
                                file=rel,
                                line=i,
                                snippet=line.strip()[:160],
                                action=action,
                            )
                        )
    return findings


def _category(pat: str) -> str:
    if "connection" in pat:
        return "connection"
    if "YOUR_PROJECT" in pat or "sql_table_name" in pat:
        return "warehouse_binding"
    if "TODO" in pat or "complex_todo" in pat:
        return "measure_todo"
    if "deficiency" in pat:
        return "dashboard_gap"
    if "description" in pat or "KPI parity" in pat:
        return "descriptions"
    if "sql_trigger" in pat or "datagroup" in pat:
        return "datagroup"
    if "preferred_viewer" in pat:
        return "looker_platform"
    return "other"


def findings_to_dicts(findings: list[Finding]) -> list[dict]:
    return [asdict(f) for f in findings]


def summarize_findings(findings: list[Finding]) -> dict:
    by_sev = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_cat: dict[str, int] = {}
    files = set()
    for f in findings:
        by_sev[f.severity] = by_sev.get(f.severity, 0) + 1
        by_cat[f.category] = by_cat.get(f.category, 0) + 1
        files.add(f.file)
    return {
        "total_findings": len(findings),
        "files_touched": len(files),
        "by_severity": by_sev,
        "by_category": by_cat,
    }
