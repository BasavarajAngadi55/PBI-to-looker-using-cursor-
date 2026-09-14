#!/usr/bin/env python3
"""Generate reviewable PDF from LOOKML_MAPPING_ASSESSMENT.md (Phase 2)."""
from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
MD = ROOT / "LOOKML_MAPPING_ASSESSMENT.md"
PDF = ROOT / "LOOKML_MAPPING_ASSESSMENT.pdf"


def latin1(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    repl = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u00b7": "-",
        "·": "-",
        "—": "-",
        "–": "-",
        "→": "->",
        "×": "x",
        "≤": "<=",
        "≥": ">=",
        "…": "...",
        "\u00a0": " ",
    }
    for a, b in repl.items():
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


def parse_md(text: str):
    """Yield ('h1'|'h2'|'p'|'table', payload)."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("## "):
            yield ("h1", line[2:].strip())
            i += 1
            continue
        if line.startswith("## "):
            yield ("h2", line[3:].strip())
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*---", lines[i + 1]):
            headers = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                row = [c.strip().replace("<br>", "\n") for c in lines[i].strip("|").split("|")]
                rows.append(row)
                i += 1
            yield ("table", (headers, rows))
            continue
        if line.strip() == "":
            i += 1
            continue
        if line.startswith("_") and line.endswith("_"):
            yield ("p", line.strip("_"))
            i += 1
            continue
        # paragraph block
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("|"):
            buf.append(lines[i])
            i += 1
        yield ("p", " ".join(buf))


class MappingPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, latin1("Phase 2 - LOOKML Mapping Assessment (review)"), align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            8,
            latin1(f"Page {self.page_no()}/{{nb}} | github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-"),
            align="C",
        )


def truncate(s: str, n: int) -> str:
    s = latin1(s)
    if len(s) <= n:
        return s
    return s[: n - 3] + "..."


def col_widths(pdf: FPDF, headers: list[str], usable: float) -> list[float]:
    n = len(headers)
    # Prefer wider columns for DAX / Comments / Suggestion
    weights = []
    for h in headers:
        hl = h.lower()
        if "dax" in hl or "original" in hl or "expression" in hl:
            weights.append(3.2)
        elif "comment" in hl or "suggestion" in hl or "why" in hl or "impact" in hl:
            weights.append(2.2)
        elif "status" in hl or "type" in hl or "complexity" in hl:
            weights.append(1.1)
        elif "table" in hl or "measure" in hl or "column" in hl or "object" in hl:
            weights.append(1.4)
        else:
            weights.append(1.0)
    total = sum(weights)
    return [usable * w / total for w in weights]


def draw_table(pdf: MappingPDF, headers, rows):
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    widths = col_widths(pdf, headers, usable)
    # Cap very wide tables: reduce font
    font_size = 6.5 if len(headers) > 8 else 7.5
    row_lh = 3.6 if len(headers) > 8 else 4.0

    def header_row():
        pdf.set_font("Helvetica", "B", font_size)
        pdf.set_fill_color(30, 60, 110)
        pdf.set_text_color(255, 255, 255)
        pdf.set_x(pdf.l_margin)
        # single-line headers truncated
        y0 = pdf.get_y()
        max_h = 8
        for i, h in enumerate(headers):
            pdf.set_xy(pdf.l_margin + sum(widths[:i]), y0)
            pdf.rect(pdf.l_margin + sum(widths[:i]), y0, widths[i], max_h, style="DF")
            pdf.set_xy(pdf.l_margin + sum(widths[:i]) + 0.5, y0 + 1)
            pdf.multi_cell(widths[i] - 1, 3.2, truncate(h, 40))
        pdf.set_y(y0 + max_h)
        pdf.set_text_color(30, 30, 30)

    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    header_row()

    fill = False
    for row in rows:
        # normalize cell count
        cells = list(row) + [""] * max(0, len(headers) - len(row))
        cells = cells[: len(headers)]
        # truncate long DAX for readability in PDF (full text remains in MD)
        for i, h in enumerate(headers):
            if "dax" in h.lower() or "original" in h.lower():
                cells[i] = truncate(cells[i], 280)
            else:
                cells[i] = truncate(cells[i], 220)

        # compute row height
        pdf.set_font("Helvetica", "", font_size)
        line_counts = []
        for i, cell in enumerate(cells):
            lines = pdf.multi_cell(widths[i], row_lh, latin1(cell), dry_run=True, output="LINES")
            line_counts.append(max(len(lines), 1))
        rh = max(line_counts) * row_lh + 1
        rh = min(rh, 55)  # cap extreme rows

        if pdf.get_y() + rh > pdf.h - 18:
            pdf.add_page()
            header_row()
            pdf.set_font("Helvetica", "", font_size)

        y0 = pdf.get_y()
        x0 = pdf.l_margin
        pdf.set_fill_color(248, 248, 248) if fill else pdf.set_fill_color(255, 255, 255)
        for i, cell in enumerate(cells):
            pdf.set_xy(x0 + sum(widths[:i]), y0)
            pdf.rect(x0 + sum(widths[:i]), y0, widths[i], rh, style="DF" if fill else "D")
            pdf.set_xy(x0 + sum(widths[:i]) + 0.4, y0 + 0.4)
            pdf.multi_cell(widths[i] - 0.8, row_lh, latin1(cell))
        pdf.set_y(y0 + rh)
        fill = not fill


def main():
    text = MD.read_text(encoding="utf-8")
    pdf = MappingPDF(orientation="L", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(10, 12, 10)
    pdf.add_page()

    # Cover / intro
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 40, 80)
    pdf.multi_cell(0, 10, latin1("Phase 2: Power BI -> LookML Mapping Assessment"))
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(
        0,
        6,
        latin1(
            "This PDF is the reviewable mapping layer only. It does NOT generate LookML or warehouse SQL. "
            "Use it to walk section-by-section through every extracted Power BI object and the recommended "
            "Looker destination for the next implementation phase."
        ),
    )
    pdf.ln(2)
    pdf.set_fill_color(245, 248, 252)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(
        0,
        5,
        latin1(
            "How to review:\n"
            "1) Section 16 first - overall Direct / Partial / Complex / Warehouse / Skip counts.\n"
            "2) Section 15 - HIGH priority complex / blocked items (SPLY, EmpCount, Employee.m, TO % Norm).\n"
            "3) Sections 1, 3, 6, 7 - views, measures, joins, Power Query destinations.\n"
            "4) Sections 2/4 - columns and calculated columns.\n"
            "5) Sections 8-14 - hierarchies, RLS, partitions, formats, auto dates, annotations.\n"
            "Note: Very long DAX may be truncated in this PDF; full original DAX is in LOOKML_MAPPING_ASSESSMENT.md."
        ),
        fill=True,
    )
    pdf.ln(4)

    for kind, payload in parse_md(text):
        if kind == "h1":
            # already titled on cover; skip duplicate main title
            if "LOOKML Mapping Assessment" in payload:
                continue
            if pdf.get_y() > 180:
                pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(20, 40, 80)
            pdf.multi_cell(0, 8, latin1(payload))
            pdf.ln(1)
        elif kind == "h2":
            if pdf.get_y() > 170:
                pdf.add_page()
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(30, 60, 110)
            pdf.multi_cell(0, 7, latin1(payload))
            pdf.ln(1)
        elif kind == "p":
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, latin1(payload))
            pdf.ln(1)
        elif kind == "table":
            headers, rows = payload
            draw_table(pdf, headers, rows)
            pdf.ln(2)

    pdf.output(str(PDF))
    print(f"Wrote {PDF} ({PDF.stat().st_size} bytes, pages~ check)")


if __name__ == "__main__":
    main()
