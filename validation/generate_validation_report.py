#!/usr/bin/env python3
"""Generate Migration Validation Report (JSON + MD + PDF).

Evidence-based conversion % + LookML user-input checklist.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from fpdf import FPDF

from lib.lookml_scan import findings_to_dicts, scan_lookml_trees, summarize_findings
from lib.score import overall_score, score_phase1, score_phase2, score_phase3

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT_JSON = ROOT / "VALIDATION_REPORT.json"
OUT_MD = ROOT / "VALIDATION_REPORT.md"
OUT_PDF = ROOT / "VALIDATION_REPORT.pdf"


def latin1(s: str) -> str:
    return (
        str(s)
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2192", "->")
        .replace("\u2248", "~")
        .replace("\u2265", ">=")
        .replace("\u2022", "*")
        .replace("%", " pct")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


class ReportPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 7, latin1(text))
        self.ln(1)

    def h2(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 64, 175)
        self.multi_cell(0, 6, latin1(text))
        self.ln(1)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, latin1(text))
        self.ln(0.5)

    def bullet(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.5, latin1(f"  - {text}"))

    def mono(self, text: str):
        self.set_x(self.l_margin)
        usable = self.w - self.l_margin - self.r_margin
        self.set_font("Courier", "", 7.5)
        self.set_text_color(30, 41, 59)
        self.set_fill_color(241, 245, 249)
        self.multi_cell(usable, 4, latin1(text), fill=True)
        self.ln(1)


def build_report() -> dict:
    p1 = score_phase1(REPO)
    p2 = score_phase2(REPO)
    p3 = score_phase3(REPO)
    overall = overall_score(p1, p2, p3)

    scan_roots = [
        REPO / "phase2" / "lookml",
        REPO / "phase3" / "lookml_dashboards",
        REPO / "phase3" / "views",
        REPO / "phase3" / "models",
        REPO / "phase3" / "warehouse_sql",
    ]
    findings = scan_lookml_trees(scan_roots)
    # Prefer repo-relative paths in report
    for f in findings:
        try:
            f.file = str(Path(f.file).resolve().relative_to(REPO.resolve()))
        except Exception:
            pass

    # Priority checklist (deduped by file+action for HIGH)
    checklist = []
    seen_actions = set()
    for f in sorted(findings, key=lambda x: ({"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(x.severity, 9), x.file, x.line)):
        key = (f.severity, f.file, f.action)
        if key in seen_actions and f.severity != "HIGH":
            continue
        if f.severity == "HIGH":
            # keep one HIGH per file+category
            key2 = (f.severity, f.file, f.category)
            if key2 in seen_actions:
                continue
            seen_actions.add(key2)
        else:
            seen_actions.add(key)
        checklist.append(
            {
                "severity": f.severity,
                "file": f.file,
                "line": f.line,
                "what": f.snippet,
                "user_must": f.action,
                "category": f.category,
            }
        )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "approach": "deterministic_evidence",
        "accuracy_statement": (
            "Percentages are computed from inventory JSON / OBJECT_MAPPING / COVERAGE only. "
            "They measure migration generation coverage — NOT live Looker KPI parity or warehouse deploy success. "
            "Confidence reflects evidence completeness, not business acceptance."
        ),
        "overall": overall,
        "phases": {"phase1": p1, "phase2": p2, "phase3": p3},
        "user_input_required": {
            "summary": summarize_findings(findings),
            "checklist": checklist[:120],
            "all_findings": findings_to_dicts(findings)[:400],
        },
        "how_to_use": [
            "1. Fix HIGH items first: connection + YOUR_PROJECT.YOUR_DATASET in every view/model.",
            "2. Implement Phase 2 TODO measures (complex DAX) and re-validate KPIs vs Power BI.",
            "3. Open Phase 3 dashboards; replace gap/partial tiles listed in remaining work.",
            "4. Re-run validation/run_validation.py after edits to refresh this report.",
        ],
    }
    return report


def write_markdown(report: dict) -> None:
    o = report["overall"]
    lines = [
        "# Migration Validation Report",
        "",
        f"_Generated {report['generated_at_utc']}_",
        "",
        "## Accuracy / confidence",
        "",
        report["accuracy_statement"],
        "",
        f"**Overall conversion done:** **{o['pct_done']}%**  ",
        f"**Left:** **{o['pct_left']}%**  ",
        f"**Confidence:** **{o['confidence']}**  ",
        f"Formula: `{o['formula']}`  ",
        f"Weights: `{o.get('weights')}`",
        "",
    ]
    if o.get("warning"):
        lines += ["### Warning", "", o["warning"], ""]

    lines += ["## Phase breakdown", ""]
    for key in ("phase1", "phase2", "phase3"):
        p = report["phases"][key]
        lines += [
            f"### Phase {p['phase']} — {p['name']}",
            "",
            f"- Done: **{p['pct_done']}%** | Left: **{p['pct_left']}%**",
            f"- Confidence: **{p['confidence']}** — {p['confidence_note']}",
            f"- Source PBIX: `{p.get('source_pbix') or 'n/a'}`",
            f"- Evidence: `{json.dumps(p.get('evidence'), ensure_ascii=True)[:300]}`",
            "",
        ]
        rem = p.get("remaining") or []
        if rem:
            lines.append("Remaining (sample):")
            for r in rem[:15]:
                lines.append(f"- `{r}`")
            lines.append("")

    ui = report["user_input_required"]
    lines += [
        "## Where YOU must provide input in LookML",
        "",
        f"Findings: **{ui['summary']['total_findings']}** across **{ui['summary']['files_touched']}** files.  ",
        f"By severity: `{ui['summary']['by_severity']}`  ",
        f"By category: `{ui['summary']['by_category']}`",
        "",
        "| Severity | File | Line | Snippet | What you must do |",
        "|---|---|---:|---|---|",
    ]
    for item in ui["checklist"][:80]:
        snip = (item["what"] or "").replace("|", "/").replace("\n", " ")[:80]
        act = (item["user_must"] or "").replace("|", "/")
        lines.append(
            f"| {item['severity']} | `{item['file']}` | {item['line']} | `{snip}` | {act} |"
        )

    lines += ["", "## Next steps", ""]
    for s in report["how_to_use"]:
        lines.append(f"- {s}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_MD)


def write_pdf(report: dict) -> None:
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(12, 12, 12)
    pdf.alias_nb_pages()
    pdf.add_page()

    o = report["overall"]
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 44, style="F")
    pdf.set_text_color(45, 212, 191)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(12, 10)
    pdf.cell(180, 6, latin1("PBIX -> Looker  |  Validation"))
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(12, 18)
    pdf.cell(180, 9, latin1("Migration Validation Report"))
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(12, 30)
    pdf.cell(
        180,
        5,
        latin1(
            f"Overall {o['pct_done']} pct done  |  {o['pct_left']} pct left  |  confidence {o['confidence']}"
        ),
    )
    pdf.set_xy(12, 36)
    pdf.cell(180, 5, latin1(report["generated_at_utc"]))

    pdf.set_y(52)
    pdf.h1("1. Accuracy statement")
    pdf.body(report["accuracy_statement"])
    pdf.body(f"Formula: {o['formula']}")
    pdf.body(f"Weights used: {o.get('weights')}")
    if o.get("warning"):
        pdf.h2("Warning")
        pdf.body(o["warning"])

    pdf.h1("2. Conversion scorecard")
    for key in ("phase1", "phase2", "phase3"):
        p = report["phases"][key]
        pdf.h2(f"Phase {p['phase']}: {p['name']}")
        pdf.body(
            f"Done {p['pct_done']} pct  |  Left {p['pct_left']} pct  |  Confidence {p['confidence']}"
        )
        pdf.body(p["confidence_note"])
        if p.get("source_pbix"):
            pdf.body(f"Source PBIX: {p['source_pbix']}")
        rem = p.get("remaining") or []
        if rem:
            pdf.body(f"Open items listed: {len(rem)} (see JSON/MD for full list)")
            for r in rem[:8]:
                if isinstance(r, dict):
                    label = r.get("lookml") or r.get("title") or r.get("pbi_type") or str(r)
                    st = r.get("status") or r.get("kind") or ""
                    pdf.bullet(f"{st} | {label}")
                else:
                    pdf.bullet(str(r))

    pdf.add_page()
    pdf.h1("3. Where you must edit LookML (user input)")
    ui = report["user_input_required"]
    pdf.body(
        f"Scanner found {ui['summary']['total_findings']} markers in "
        f"{ui['summary']['files_touched']} files. "
        f"Severity counts: {ui['summary']['by_severity']}"
    )
    pdf.body(
        "Go to each file/line below in your IDE. HIGH = must fix before Looker validate. "
        "MEDIUM = KPI/parity or gap tiles. LOW = polish."
    )

    # Group HIGH first
    for sev in ("HIGH", "MEDIUM", "LOW"):
        items = [x for x in ui["checklist"] if x["severity"] == sev]
        if not items:
            continue
        pdf.h2(f"{sev} priority ({len(items)})")
        for item in items[:35]:
            pdf.bullet(
                f"{item['file']}:{item['line']} — {item['user_must']}"
            )
            pdf.mono(item["what"][:140])

    pdf.h1("4. Recommended checklist order")
    for s in report["how_to_use"]:
        pdf.bullet(s)

    pdf.h1("5. What this report does NOT claim")
    pdf.body(
        "It does not prove warehouse tables exist, Looker connection works, or numbers match Power BI. "
        "Those require deploy + KPI parity tests after you replace placeholders and finish TODOs."
    )

    pdf.output(str(OUT_PDF))
    print("Wrote", OUT_PDF)


def generate() -> dict:
    report = build_report()
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT_JSON)
    write_markdown(report)
    write_pdf(report)
    return report


if __name__ == "__main__":
    r = generate()
    o = r["overall"]
    print(
        f"OVERALL {o['pct_done']}% done / {o['pct_left']}% left | confidence={o['confidence']}"
    )
