#!/usr/bin/env python3
"""Prove Phase-1 deterministic extract matches live pbixray + cross-checks."""
from __future__ import annotations

import json
from pathlib import Path

from fpdf import FPDF
from pbixray import PBIXRay

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
MD_OUT = ROOT / "AGENT_VALIDATION_PROOF.md"
PDF_OUT = ROOT / "AGENT_VALIDATION_PROOF.pdf"
PNG_OUT = ROOT / "AGENT_VALIDATION_PROOF.png"


def latin1(s: str) -> str:
    return (
        str(s)
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2192", "->")
        .replace("✓", "OK")
        .replace("✗", "FAIL")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def load_json(name: str) -> dict:
    return json.loads((INV / name).read_text(encoding="utf-8"))


def check(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def run_proof(pbix_path: Path | None = None) -> dict:
    counts_meta = load_json("OBJECT_COUNTS.json")
    pbix_path = Path(pbix_path or counts_meta.get("source_pbix") or "")
    a1 = load_json("01_tables_columns.json")
    a2 = load_json("03_relationships.json")
    a3 = load_json("02_dax_objects.json")
    a4 = load_json("04_power_query_m.json")
    a5 = load_json("05_tmschema_extras.json")

    pbix = PBIXRay(str(pbix_path))
    live_tables = sorted(list(pbix.tables))
    inv_tables = sorted(t["table_name"] for t in a1.get("tables", []))
    live_measures = pbix.dax_measures
    live_rels = pbix.relationships
    live_pq = pbix.power_query
    live_dax_cols = pbix.dax_columns
    live_dax_tables = pbix.dax_tables

    m_files = sorted((INV / "04_m_raw").glob("*.m"))
    m_names = {p.stem for p in m_files}
    pq_names = {q["query_name"] for q in a4.get("queries", [])}

    table_set = set(inv_tables)
    rel_ok_tables = all(
        r["from_table"] in table_set and r["to_table"] in table_set
        for r in a2.get("relationships", [])
    )

    # sample expression equality for first 3 measures
    measure_samples = []
    if live_measures is not None and len(live_measures):
        name_col = "Name" if "Name" in live_measures.columns else live_measures.columns[0]
        expr_col = (
            "Expression"
            if "Expression" in live_measures.columns
            else ("expression" if "expression" in live_measures.columns else None)
        )
        inv_by_name = {m["measure_name"]: m.get("expression") for m in a3.get("measures", [])}
        for _, row in live_measures.head(5).iterrows():
            n = str(row[name_col])
            live_expr = str(row[expr_col]).strip() if expr_col else ""
            inv_expr = (inv_by_name.get(n) or "").strip()
            measure_samples.append(
                {
                    "name": n,
                    "match": live_expr == inv_expr and bool(inv_expr),
                    "live_len": len(live_expr),
                    "inv_len": len(inv_expr),
                    "preview": (inv_expr[:80] + "...") if len(inv_expr) > 80 else inv_expr,
                }
            )

    checks = [
        check(
            "A1 tables == live pbix.tables",
            inv_tables == live_tables,
            f"inventory={len(inv_tables)} live={len(live_tables)} "
            f"missing_in_inv={sorted(set(live_tables)-set(inv_tables))} "
            f"extra_in_inv={sorted(set(inv_tables)-set(live_tables))}",
        ),
        check(
            "A1 columns present",
            len(a1.get("columns", [])) > 0,
            f"columns={len(a1.get('columns', []))}",
        ),
        check(
            "A2 relationships == live count",
            len(a2.get("relationships", [])) == len(live_rels),
            f"inventory={len(a2.get('relationships', []))} live={len(live_rels)}",
        ),
        check(
            "A2 relationships reference known tables",
            rel_ok_tables,
            "all from/to tables exist in schema extract",
        ),
        check(
            "A3 measures == live dax_measures",
            len(a3.get("measures", [])) == len(live_measures),
            f"inventory={len(a3.get('measures', []))} live={len(live_measures)}",
        ),
        check(
            "A3 calc columns == live dax_columns",
            len(a3.get("calculated_columns", [])) == len(live_dax_cols),
            f"inventory={len(a3.get('calculated_columns', []))} live={len(live_dax_cols)}",
        ),
        check(
            "A3 calc tables == live dax_tables",
            len(a3.get("calculated_tables", [])) == len(live_dax_tables),
            f"inventory={len(a3.get('calculated_tables', []))} live={len(live_dax_tables)}",
        ),
        check(
            "A3 measure expressions match (sample)",
            all(s["match"] for s in measure_samples) if measure_samples else False,
            f"checked={len(measure_samples)} matched={sum(1 for s in measure_samples if s['match'])}",
        ),
        check(
            "A4 power query == live count",
            len(a4.get("queries", [])) == len(live_pq),
            f"inventory={len(a4.get('queries', []))} live={len(live_pq)}",
        ),
        check(
            "A4 m_raw files == queries",
            m_names == pq_names and len(m_files) == len(pq_names),
            f"m_files={sorted(m_names)} queries={sorted(pq_names)}",
        ),
        check(
            "A4 m files non-empty",
            all(p.stat().st_size > 0 for p in m_files),
            f"bytes={[p.stem+':'+str(p.stat().st_size) for p in m_files]}",
        ),
        check(
            "A5 RLS captured as list",
            isinstance(a5.get("rls"), list),
            f"rls_count={len(a5.get('rls') or [])}",
        ),
        check(
            "A5 auto date tables captured",
            len(a5.get("auto_date_tables") or [])
            == sum(
                1
                for t in inv_tables
                if t.startswith("LocalDateTable_") or t.startswith("DateTableTemplate_")
            ),
            f"auto_date={len(a5.get('auto_date_tables') or [])}",
        ),
        check(
            "Cross: calc table names align A1/A3",
            sorted(t["table_name"] for t in a1.get("calculated_tables", []))
            == sorted(t["table_name"] for t in a3.get("calculated_tables", [])),
            "calculated_tables name sets equal",
        ),
        check(
            "Merger counts file present",
            (INV / "OBJECT_COUNTS.json").exists() and (INV / "OBJECT_INVENTORY.md").exists(),
            "OBJECT_COUNTS.json + OBJECT_INVENTORY.md",
        ),
    ]

    # evidence snippets
    evidence = {
        "pbix": str(pbix_path),
        "tables_live": live_tables,
        "relationships_sample": a2.get("relationships", [])[:3],
        "measure_samples": measure_samples,
        "m_file_sizes": {p.name: p.stat().st_size for p in m_files},
        "employee_m_preview": (
            (INV / "04_m_raw" / "Employee.m").read_text(encoding="utf-8")[:400]
            if (INV / "04_m_raw" / "Employee.m").exists()
            else ""
        ),
    }

    passed = sum(1 for c in checks if c["status"] == "PASS")
    failed = sum(1 for c in checks if c["status"] == "FAIL")
    verdict = "PASS" if failed == 0 else "FAIL"

    return {
        "verdict": verdict,
        "passed": passed,
        "failed": failed,
        "checks": checks,
        "evidence": evidence,
        "counts": counts_meta.get("counts", {}),
    }


def write_md(proof: dict) -> None:
    lines = [
        "# Extract Validation Proof — Phase 1",
        "",
        f"**Verdict:** `{proof['verdict']}`  ",
        f"**Checks passed:** {proof['passed']} / {proof['passed'] + proof['failed']}  ",
        f"**Source PBIX:** `{proof['evidence']['pbix']}`",
        "",
        "Phase 1 extract is **deterministic** (no LLM). "
        "Method: compare inventory JSON against a **fresh live pbixray read**, then cross-check extract stages against each other.",
        "",
        "## Check results",
        "",
        "| # | Check | Status | Detail |",
        "|---|--------|--------|--------|",
    ]
    for i, c in enumerate(proof["checks"], 1):
        lines.append(f"| {i} | {c['name']} | **{c['status']}** | `{c['detail']}` |")
    lines += [
        "",
        "## Live table list (pbixray)",
        "",
        "```text",
        "\n".join(proof["evidence"]["tables_live"]),
        "```",
        "",
        "## Measure expression samples",
        "",
        "| Measure | Match | Preview |",
        "|---------|-------|---------|",
    ]
    for s in proof["evidence"]["measure_samples"]:
        prev = (s["preview"] or "").replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{s['name']}` | {'PASS' if s['match'] else 'FAIL'} | `{prev}` |")
    lines += [
        "",
        "## Relationship sample (inventory)",
        "",
        "```json",
        json.dumps(proof["evidence"]["relationships_sample"], indent=2),
        "```",
        "",
        "## Power Query M proof",
        "",
        "### File sizes",
        "",
        "```json",
        json.dumps(proof["evidence"]["m_file_sizes"], indent=2),
        "```",
        "",
        "### Employee.m preview (first 400 chars)",
        "",
        "```m",
        proof["evidence"]["employee_m_preview"],
        "```",
        "",
        "## Object counts (merger)",
        "",
        "```json",
        json.dumps(proof["counts"], indent=2),
        "```",
        "",
    ]
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def write_pdf(proof: dict) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(True, 12)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, latin1("Extract Validation Proof - Phase 1"), ln=1)
    pdf.set_font("Helvetica", "B", 12)
    color = (20, 120, 60) if proof["verdict"] == "PASS" else (160, 40, 40)
    pdf.set_text_color(*color)
    pdf.cell(
        0,
        8,
        latin1(
            f"Verdict: {proof['verdict']}  ({proof['passed']} passed / {proof['failed']} failed)"
        ),
        ln=1,
    )
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(
        0,
        5,
        latin1(
            "Deterministic extract (no LLM). Proof method: re-open PBIX with pbixray and compare "
            "live object counts/names/expressions to each stage inventory file. Also cross-check stages."
        ),
    )
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Checks", ln=1)
    pdf.set_font("Helvetica", "", 8)
    for i, c in enumerate(proof["checks"], 1):
        mark = "[PASS]" if c["status"] == "PASS" else "[FAIL]"
        if c["status"] == "PASS":
            pdf.set_text_color(20, 110, 50)
        else:
            pdf.set_text_color(150, 30, 30)
        pdf.set_x(10)
        pdf.multi_cell(190, 4, latin1(f"{i}. {mark} {c['name']}"))
        pdf.set_text_color(70, 70, 70)
        detail = c["detail"]
        if len(detail) > 140:
            detail = detail[:137] + "..."
        pdf.set_x(10)
        pdf.multi_cell(190, 4, latin1(f"    {detail}"))
    pdf.set_text_color(40, 40, 40)
    pdf.ln(3)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Measure sample matches", ln=1)
    pdf.set_font("Courier", "", 8)
    for s in proof["evidence"]["measure_samples"]:
        pdf.set_x(10)
        pdf.multi_cell(
            190,
            4,
            latin1(
                f"{'[OK]' if s['match'] else '[FAIL]'} {s['name']}: {s['preview']}"
            ),
        )
    pdf.ln(2)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "M file sizes", ln=1)
    pdf.set_font("Courier", "", 8)
    for k, v in proof["evidence"]["m_file_sizes"].items():
        pdf.set_x(10)
        pdf.cell(0, 4, latin1(f"{k}: {v} bytes"), ln=1)
    pdf.output(str(PDF_OUT))


def write_png(proof: dict) -> None:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (1200, 900), (248, 250, 252))
    d = ImageDraw.Draw(img)
    try:
        font_b = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except Exception:
        font_b = font = font_s = ImageFont.load_default()

    d.text((40, 30), "Extract Validation Proof", fill=(15, 40, 60), font=font_b)
    verdict_color = (20, 130, 70) if proof["verdict"] == "PASS" else (170, 40, 40)
    d.rounded_rectangle((40, 80, 420, 140), radius=12, fill=verdict_color)
    d.text(
        (60, 98),
        f"VERDICT: {proof['verdict']}   {proof['passed']}/{proof['passed']+proof['failed']} checks",
        fill=(255, 255, 255),
        font=font,
    )
    d.text((40, 160), "Live pbixray vs inventory (deterministic stages 1-6)", fill=(80, 90, 100), font=font_s)

    y = 190
    for i, c in enumerate(proof["checks"], 1):
        ok = c["status"] == "PASS"
        fill = (220, 245, 230) if ok else (255, 230, 230)
        outline = (40, 140, 80) if ok else (170, 50, 50)
        d.rounded_rectangle((40, y, 1160, y + 34), radius=6, fill=fill, outline=outline, width=1)
        d.text(
            (55, y + 8),
            f"{i:02d}  {'PASS' if ok else 'FAIL'}  {c['name']}",
            fill=(20, 30, 40),
            font=font_s,
        )
        y += 40
        if y > 850:
            break
    img.save(PNG_OUT)


def main() -> None:
    proof = run_proof()
    write_md(proof)
    write_pdf(proof)
    write_png(proof)
    (INV / "AGENT_VALIDATION_PROOF.json").write_text(
        json.dumps(proof, indent=2), encoding="utf-8"
    )
    print(f"Verdict: {proof['verdict']} ({proof['passed']} pass / {proof['failed']} fail)")
    print("Wrote", MD_OUT)
    print("Wrote", PDF_OUT)
    print("Wrote", PNG_OUT)


if __name__ == "__main__":
    main()
