#!/usr/bin/env python3
"""Generate Power Query M → Looker/warehouse recommendations + SQL/LookML stubs.

Outputs (included in LOOKML_PROJECT.zip under lookml/m_migration/):
  M_QUERY_RECOMMENDATIONS.json
  M_QUERY_RECOMMENDATIONS.md
  sql/<query>.sql
  lookml_stubs/<query>_recommended.lkml
"""
from __future__ import annotations

import json
from pathlib import Path

from lib.m_query_patterns import classify_m_query
from lib.naming import snake_case

ROOT = Path(__file__).resolve().parent
PHASE1_INV = ROOT.parent / "phase1" / "inventory"
OUT_DIR = ROOT / "lookml" / "m_migration"


def generate(inv_dir: Path | None = None, out_dir: Path | None = None) -> dict:
    inv = inv_dir or PHASE1_INV
    out = out_dir or OUT_DIR
    a4_path = inv / "04_power_query_m.json"
    if not a4_path.exists():
        raise FileNotFoundError(f"Missing {a4_path}")

    a4 = json.loads(a4_path.read_text())
    queries = a4.get("queries") or []
    sql_dir = out / "sql"
    stub_dir = out / "lookml_stubs"
    sql_dir.mkdir(parents=True, exist_ok=True)
    stub_dir.mkdir(parents=True, exist_ok=True)

    # clean previous stubs
    for p in sql_dir.glob("*.sql"):
        p.unlink()
    for p in stub_dir.glob("*.lkml"):
        p.unlink()

    recs = []
    pattern_counts: dict[str, int] = {}
    for q in queries:
        rec = classify_m_query(q)
        recs.append(rec)
        pattern_counts[rec.recommended_pattern] = pattern_counts.get(rec.recommended_pattern, 0) + 1
        stem = snake_case(rec.query_name)
        (sql_dir / f"{stem}.sql").write_text(rec.sql_stub)
        (stub_dir / f"{stem}_recommended.lkml").write_text(rec.lookml_stub)

    payload = {
        "approach": "deterministic",
        "source_pbix": a4.get("source_pbix"),
        "best_practice_order": [
            "1. Warehouse table/view (ETL/dbt) + straight LookML view (sql_table_name) — preferred",
            "2. LookML SQL derived table (SDT) — temporary bridge for light SQL only",
            "3. Native derived table (NDT) — rarely a Power Query replacement",
            "4. Never put heavy M merges/appends only in LookML",
        ],
        "pattern_counts": pattern_counts,
        "query_count": len(recs),
        "recommendations": [r.to_dict() for r in recs],
    }
    (out / "M_QUERY_RECOMMENDATIONS.json").write_text(json.dumps(payload, indent=2))
    (out / "M_QUERY_RECOMMENDATIONS.md").write_text(_markdown(payload, recs))
    (out / "README.md").write_text(
        "# Power Query M → Looker migration stubs\n\n"
        "Generated deterministically from Phase 1 `04_power_query_m.json`.\n\n"
        "- `M_QUERY_RECOMMENDATIONS.md` — decision + steps per query\n"
        "- `sql/` — recommended warehouse SQL stubs\n"
        "- `lookml_stubs/` — recommended LookML (straight view and/or temporary SDT)\n\n"
        "Best practice: implement SQL in the warehouse, then use the generated "
        "`views/*.view.lkml` with updated `sql_table_name`.\n"
    )
    print("Wrote M migration stubs:", out, f"({len(recs)} queries)")
    return {
        "out_dir": str(out),
        "query_count": len(recs),
        "pattern_counts": pattern_counts,
    }


def _markdown(payload: dict, recs: list) -> str:
    lines = [
        "# Power Query M → Looker / warehouse recommendations",
        "",
        f"**Source:** `{Path(payload.get('source_pbix') or 'PBIX').name}`  ",
        f"**Queries:** {payload.get('query_count')}  ",
        "**Approach:** deterministic (no LLM)",
        "",
        "## Best-practice decision order",
        "",
    ]
    for b in payload.get("best_practice_order") or []:
        lines.append(f"- {b}")
    lines += [
        "",
        "## Pattern summary",
        "",
        "| Pattern | Count |",
        "|---|---|",
    ]
    for k, v in sorted((payload.get("pattern_counts") or {}).items()):
        lines.append(f"| `{k}` | {v} |")

    lines += ["", "## Per-query recommendations", ""]
    for r in recs:
        lines += [
            f"### `{r.query_name}`",
            "",
            f"- **Recommended pattern:** `{r.recommended_pattern}`",
            f"- **Looker object:** {r.looker_object}",
            f"- **Build in:** `{r.build_in}` (confidence: {r.confidence})",
            f"- **Why:** {r.rationale}",
            f"- **Signals:** {', '.join(r.m_signals) or '-'}",
            "",
            "**Build steps:**",
            "",
        ]
        for i, s in enumerate(r.steps, 1):
            lines.append(f"{i}. {s}")
        lines += ["", "**Checks:**", ""]
        for c in r.checks:
            lines.append(f"- [ ] {c}")
        lines += [
            "",
            f"**SQL stub:** `m_migration/sql/{snake_case(r.query_name)}.sql`",
            f"**LookML stub:** `m_migration/lookml_stubs/{snake_case(r.query_name)}_recommended.lkml`",
            "",
            "<details><summary>SQL preview</summary>",
            "",
            "```sql",
            r.sql_stub.strip(),
            "```",
            "",
            "</details>",
            "",
            "<details><summary>LookML preview</summary>",
            "",
            "```lookml",
            r.lookml_stub.strip(),
            "```",
            "",
            "</details>",
            "",
        ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2))
