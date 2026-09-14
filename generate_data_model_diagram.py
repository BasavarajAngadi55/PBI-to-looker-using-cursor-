#!/usr/bin/env python3
"""Generate full Power BI data model diagram (business + internal + relationships)."""
from __future__ import annotations

import json
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
PDF_OUT = ROOT / "DATA_MODEL.pdf"
PNG_OUT = ROOT / "DATA_MODEL.png"
MD_OUT = ROOT / "DATA_MODEL.md"

a1 = json.loads((INV / "01_tables_columns.json").read_text())
a2 = json.loads((INV / "03_relationships.json").read_text())
a3 = json.loads((INV / "02_dax_objects.json").read_text())
a5 = json.loads((INV / "05_tmschema_extras.json").read_text())


def latin1(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    for a, b in {
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u2192": "->", "—": "-", "–": "-", "→": "->",
    }.items():
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


def is_internal(n: str) -> bool:
    return n.startswith("LocalDateTable_") or n.startswith("DateTableTemplate_")


def short_internal(n: str) -> str:
    if n.startswith("LocalDateTable_"):
        return "LocalDateTable_" + n.split("_")[1][:8] + "..."
    if n.startswith("DateTableTemplate_"):
        return "DateTableTemplate_" + n.split("_")[1][:8] + "..."
    return n


# Logical PKs (from relationships / business knowledge - inventory only marks Date.Date as IsKey)
LOGICAL_PK = {
    "Employee": "(grain: EmplID + date) — no single PK in PBIX",
    "Date": "Date",
    "BU": "BU",
    "AgeGroup": "AgeGroupID",
    "Ethnicity": "Ethnic Group",
    "FP": "FP",
    "Gender": "ID",
    "PayType": "PayTypeID",
    "SeparationReason": "SeparationTypeID",
}


def build_markdown() -> str:
    lines = []
    lines.append("# Power BI Data Model Diagram — Human Resources Sample")
    lines.append("")
    lines.append("Generated from Phase 1 inventory. Includes **business**, **calculated**, and **internal auto-date** tables.")
    lines.append("")
    lines.append("## Star schema (business relationships)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("erDiagram")
    # entities with key columns
    biz = [t for t in a1["tables"] if not is_internal(t["table_name"])]
    for t in biz:
        name = t["table_name"].replace(" ", "_")
        lines.append(f"  {name} {{")
        cols = [c for c in a1["columns"] if c["table_name"] == t["table_name"]]
        for c in cols:
            dtype = str(c.get("pandas_dtype") or c.get("data_type") or "unknown")
            flag = " PK" if (
                LOGICAL_PK.get(t["table_name"]) == c["column_name"]
                or c.get("is_key")
            ) else (" CALC" if c.get("is_calculated_column") else "")
            # sanitize column names for mermaid
            cn = c["column_name"].replace(" ", "_").replace("-", "_")
            lines.append(f"    {dtype} {cn}{flag}")
        lines.append("  }")
    for r in a2["relationships"]:
        ft = r["from_table"].replace(" ", "_")
        tt = r["to_table"].replace(" ", "_")
        # M:1 => }o--||
        lines.append(
            f"  {ft} }}o--|| {tt} : \"{r['from_column']}->{r['to_column']} ({r['cardinality']})\""
        )
    lines.append("```")
    lines.append("")
    lines.append("## Relationship inventory (all 8 — active, Single, M:1)")
    lines.append("")
    lines.append("| # | From Table | From Column (FK) | To Table | To Column (PK side) | Cardinality | Cross-filter | Active |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(a2["relationships"], 1):
        lines.append(
            f"| {i} | {r['from_table']} | `{r['from_column']}` | {r['to_table']} | `{r['to_column']}` | {r['cardinality']} | {r['cross_filter']} | {r['active']} |"
        )
    lines.append("")
    lines.append("## Business tables — columns & keys")
    lines.append("")
    for t in biz:
        name = t["table_name"]
        cols = [c for c in a1["columns"] if c["table_name"] == name]
        lines.append(f"### `{name}` ({t['table_type']})")
        lines.append("")
        lines.append(f"- **Logical key / grain:** {LOGICAL_PK.get(name, 'see columns')}")
        lines.append(f"- **Column count:** {len(cols)}")
        lines.append("")
        lines.append("| Column | Type | Calculated | Role |")
        lines.append("|---|---|---|---|")
        for c in cols:
            role = []
            if c.get("is_key") or LOGICAL_PK.get(name) == c["column_name"]:
                role.append("PK")
            for r in a2["relationships"]:
                if r["from_table"] == name and r["from_column"] == c["column_name"]:
                    role.append(f"FK → {r['to_table']}.{r['to_column']}")
                if r["to_table"] == name and r["to_column"] == c["column_name"]:
                    role.append("PK-side (joined from Employee)")
            if c.get("is_calculated_column"):
                role.append("DAX calc")
            lines.append(
                f"| `{c['column_name']}` | {c.get('pandas_dtype') or c.get('data_type')} | "
                f"{'Yes' if c.get('is_calculated_column') else 'No'} | {', '.join(role) or 'attr'} |"
            )
        lines.append("")
    lines.append("## Calculated columns (business) — DAX")
    lines.append("")
    lines.append("| Table | Column | DAX |")
    lines.append("|---|---|---|")
    for c in a3["calculated_columns"]:
        if is_internal(c["table"]):
            continue
        expr = (c["expression"] or "").replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| {c['table']} | `{c['column_name']}` | `{expr}` |")
    lines.append("")
    lines.append("## Internal / calculated auto-date tables")
    lines.append("")
    lines.append(
        "Power BI auto time-intelligence tables. **No relationships** to business tables in `03_relationships.json` "
        "(hidden TI). Captured for completeness; LookML migration = SKIP_INTERNAL."
    )
    lines.append("")
    lines.append("| Internal Table | Type | Columns | Calculated cols | Hierarchy |")
    lines.append("|---|---|---:|---:|---|")
    hier_by_t = {h.get("table"): h for h in (a5.get("hierarchies") or [])}
    for t in a1["tables"]:
        if not is_internal(t["table_name"]):
            continue
        name = t["table_name"]
        cols = [c for c in a1["columns"] if c["table_name"] == name]
        calc = sum(1 for c in cols if c.get("is_calculated_column"))
        h = hier_by_t.get(name)
        hname = h.get("hierarchy_name") if h else "—"
        lines.append(
            f"| `{name}` | {t['table_type']} | {len(cols)} | {calc} | {hname} |"
        )
    lines.append("")
    lines.append("### Typical auto-date columns")
    lines.append("")
    # sample one LocalDateTable
    sample = next(t["table_name"] for t in a1["tables"] if t["table_name"].startswith("LocalDateTable_"))
    lines.append(f"Example from `{sample}`:")
    lines.append("")
    lines.append("| Column | Type | Calculated |")
    lines.append("|---|---|---|")
    for c in a1["columns"]:
        if c["table_name"] == sample:
            lines.append(
                f"| `{c['column_name']}` | {c.get('pandas_dtype') or c.get('data_type')} | "
                f"{'Yes' if c.get('is_calculated_column') else 'No'} |"
            )
    lines.append("")
    lines.append("### Calculated table DAX (Calendar)")
    lines.append("")
    for t in a3["calculated_tables"]:
        lines.append(f"#### `{t['table_name']}`")
        lines.append("")
        lines.append("```dax")
        lines.append(t["expression"])
        lines.append("```")
        lines.append("")
    lines.append("## Model notes")
    lines.append("")
    lines.append("1. **Fact:** `Employee` — monthly snapshot grain (`date` × `EmplID`).")
    lines.append("2. **All 8 relationships** are many-to-one from Employee → dimensions, active, single-direction cross-filter.")
    lines.append("3. **AgeGroupID** on Employee is a calculated column used as FK to AgeGroup.")
    lines.append("4. **Internal LocalDateTable_*** / **DateTableTemplate_*** are auto-generated; not part of the business star.")
    lines.append("5. **RLS:** none in this PBIX.")
    lines.append("")
    return "\n".join(lines)


class ModelPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, latin1("HR Sample - Full Data Model (business + internal)"), align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, latin1(f"Page {self.page_no()}/{{nb}} | From Phase 1 inventory"), align="C")

    def h1(self, t):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 9, latin1(t))
        self.ln(2)

    def h2(self, t):
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 60, 110)
        self.multi_cell(0, 7, latin1(t))
        self.ln(1)

    def body(self, t):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, latin1(t))
        self.ln(1)

    def box(self, x, y, w, h, title, lines, fill, border):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 1.5, y + 1.5)
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(20, 40, 80)
        self.cell(w - 3, 4, latin1(title)[:40])
        self.set_font("Helvetica", "", 5.5)
        self.set_text_color(30, 30, 30)
        ty = y + 6
        for line in lines[:12]:
            self.set_xy(x + 1.5, ty)
            self.cell(w - 3, 3.2, latin1(line)[:48])
            ty += 3.2


def make_pdf():
    pdf = ModelPDF(orientation="L", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(10, 12, 10)
    pdf.add_page()
    pdf.h1("Power BI Data Model - Human Resources Sample")
    pdf.body(
        "Star schema: Employee (fact) to 8 dimensions. All relationships M:1, active, single cross-filter. "
        "Also lists 6 internal auto-date calculated tables (no business joins in relationship inventory)."
    )

    # Layout star: Employee center, dims around
    left, top = 10, 42
    usable_w = pdf.w - 20
    # Employee center
    emp_cols = [c for c in a1["columns"] if c["table_name"] == "Employee"]
    emp_lines = []
    for c in emp_cols:
        mark = "*" if c.get("is_calculated_column") else ""
        fk = ""
        for r in a2["relationships"]:
            if r["from_table"] == "Employee" and r["from_column"] == c["column_name"]:
                fk = f" ->{r['to_table']}"
        emp_lines.append(f"{c['column_name']}{mark}{fk}")
    cx, cy = left + usable_w / 2 - 38, top + 55
    pdf.box(cx, cy, 76, 58, "FACT: Employee (16 cols)", emp_lines, (255, 240, 230), (180, 80, 40))

    # Dim positions around
    dims = [
        ("Date", left + 5, top),
        ("BU", left + 95, top),
        ("AgeGroup", left + 185, top),
        ("Gender", left + 250, top),
        ("Ethnicity", left + 5, top + 130),
        ("FP", left + 95, top + 130),
        ("PayType", left + 185, top + 130),
        ("SeparationReason", left + 250, top + 130),
    ]
    colors = {
        "Date": ((230, 245, 255), (40, 90, 150)),
        "BU": ((235, 255, 235), (40, 120, 70)),
        "AgeGroup": ((245, 235, 255), (100, 60, 140)),
        "Gender": ((255, 235, 245), (140, 50, 100)),
        "Ethnicity": ((255, 250, 230), (160, 120, 40)),
        "FP": ((240, 250, 255), (50, 100, 140)),
        "PayType": ((245, 245, 245), (80, 80, 80)),
        "SeparationReason": ((255, 235, 235), (140, 50, 50)),
    }
    for name, x, y in dims:
        cols = [c for c in a1["columns"] if c["table_name"] == name]
        lines = []
        pk = LOGICAL_PK.get(name, "")
        for c in cols:
            star = " [PK]" if c["column_name"] == pk or c.get("is_key") else ""
            calc = " *" if c.get("is_calculated_column") else ""
            lines.append(f"{c['column_name']}{star}{calc}")
        fill, border = colors[name]
        # find FK from employee
        rel = next(r for r in a2["relationships"] if r["to_table"] == name)
        title = f"{name}  PK:{pk}"
        pdf.box(x, y, 70, 8 + 3.2 * min(len(lines), 10) + 4, title, lines, fill, border)
        # line to center
        pdf.set_draw_color(120, 120, 120)
        pdf.set_line_width(0.3)
        pdf.line(x + 35, y + 20, cx + 38, cy + 20)
        pdf.set_font("Helvetica", "", 5)
        pdf.set_text_color(80, 80, 80)
        mid_x = (x + 35 + cx + 38) / 2
        mid_y = (y + 20 + cy + 20) / 2
        pdf.set_xy(mid_x - 15, mid_y - 2)
        pdf.cell(30, 3, latin1(f"M:1 {rel['from_column']}"))

    pdf.set_xy(pdf.l_margin, min(top + 195, pdf.h - 25))
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(60, 60, 60)
    usable0 = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(usable0, 4, latin1("* = calculated column (DAX). Lines = active M:1 relationships (Single cross-filter)."))

    # Page 2 relationships table + calc cols
    pdf.add_page()
    pdf.set_x(pdf.l_margin)
    pdf.h2("Relationships (complete)")
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_fill_color(30, 60, 110)
    pdf.set_text_color(255, 255, 255)
    headers = ["From", "FK", "To", "PK col", "Card", "XF", "Active"]
    widths = [35, 35, 40, 45, 18, 22, 18]
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 6, h, border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(30, 30, 30)
    for r in a2["relationships"]:
        vals = [r["from_table"], r["from_column"], r["to_table"], r["to_column"], r["cardinality"], r["cross_filter"], str(r["active"])]
        for i, v in enumerate(vals):
            pdf.cell(widths[i], 5, latin1(str(v))[:28], border=1)
        pdf.ln()

    pdf.h2("Business calculated columns")
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    for c in a3["calculated_columns"]:
        if is_internal(c["table"]):
            continue
        if pdf.get_y() > pdf.h - 40:
            pdf.add_page()
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(30, 60, 110)
        pdf.multi_cell(usable, 5, latin1(f"{c['table']}.{c['column_name']}"))
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Courier", "", 6.5)
        pdf.set_text_color(20, 20, 20)
        pdf.set_fill_color(245, 245, 245)
        pdf.multi_cell(usable, 3.5, latin1(c["expression"] or ""), fill=True)
        pdf.ln(1)

    # Page 3 internal tables
    pdf.add_page()
    pdf.h2("Internal auto-date / calculated tables (6)")
    pdf.body(
        "These are Power BI-generated time intelligence tables (Calendar DAX). "
        "They are NOT linked in the 8 business relationships inventory. LookML: SKIP_INTERNAL."
    )
    for t in a1["tables"]:
        if not is_internal(t["table_name"]):
            continue
        name = t["table_name"]
        cols = [c for c in a1["columns"] if c["table_name"] == name]
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(100, 40, 40)
        pdf.multi_cell(0, 5, latin1(f"{name}  ({t['table_type']}, {len(cols)} columns)"))
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.set_text_color(40, 40, 40)
        col_txt = ", ".join(
            f"{c['column_name']}{'*' if c.get('is_calculated_column') else ''}" for c in cols
        )
        usable3 = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(usable3, 3.5, latin1(col_txt))
        # dax snippet
        dax = next((x["expression"] for x in a3["calculated_tables"] if x["table_name"] == name), None)
        if dax:
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Courier", "", 6)
            pdf.set_fill_color(255, 245, 245)
            usable2 = pdf.w - pdf.l_margin - pdf.r_margin
            pdf.multi_cell(
                usable2,
                3.2,
                latin1(dax[:500] + ("..." if len(dax) > 500 else "")),
                fill=True,
            )
        pdf.ln(2)

    pdf.h2("Summary counts")
    pdf.set_x(pdf.l_margin)
    pdf.body(
        f"Business tables: 9 | Internal/calc auto-date tables: 6 | Total tables: 15 | "
        f"Business relationships: 8 | Columns total: 87 | Business calc columns: 7 | "
        f"RLS roles: 0 | Hierarchies: {len(a5.get('hierarchies') or [])}"
    )
    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def make_png():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("No Pillow")
        return

    W, H = 2200, 1600
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font_b = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except Exception:
        font_b = font = font_s = ImageFont.load_default()

    def tbox(xy, title, lines, fill, outline):
        draw.rounded_rectangle(xy, radius=10, fill=fill, outline=outline, width=2)
        x1, y1, x2, y2 = xy
        draw.text((x1 + 10, y1 + 8), title, fill=(20, 40, 80), font=font)
        ty = y1 + 32
        for line in lines:
            draw.text((x1 + 10, ty), line[:42], fill=(40, 40, 40), font=font_s)
            ty += 16

    draw.text((40, 20), "HR Sample Data Model - Business Star + Internal Auto-Dates", fill=(20, 40, 80), font=font_b)
    draw.text((40, 55), "All 8 relationships: Employee (M) -> Dim (1) | Active | Single cross-filter | * = calculated column", fill=(80, 80, 80), font=font_s)

    # Center Employee
    emp_cols = [c["column_name"] + ("*" if c.get("is_calculated_column") else "") for c in a1["columns"] if c["table_name"] == "Employee"]
    tbox((850, 520, 1350, 920), "FACT Employee", emp_cols, (255, 240, 230), (180, 80, 40))

    positions = {
        "Date": (80, 100),
        "BU": (500, 100),
        "AgeGroup": (1200, 100),
        "Gender": (1600, 100),
        "Ethnicity": (80, 1000),
        "FP": (500, 1000),
        "PayType": (1200, 1000),
        "SeparationReason": (1600, 1000),
    }
    fills = {
        "Date": ((230, 245, 255), (40, 90, 150)),
        "BU": ((235, 255, 235), (40, 120, 70)),
        "AgeGroup": ((245, 235, 255), (100, 60, 140)),
        "Gender": ((255, 235, 245), (140, 50, 100)),
        "Ethnicity": ((255, 250, 230), (160, 120, 40)),
        "FP": ((240, 250, 255), (50, 100, 140)),
        "PayType": ((245, 245, 245), (80, 80, 80)),
        "SeparationReason": ((255, 235, 235), (140, 50, 50)),
    }
    for name, (x, y) in positions.items():
        cols = []
        pk = LOGICAL_PK.get(name, "")
        for c in a1["columns"]:
            if c["table_name"] != name:
                continue
            label = c["column_name"]
            if label == pk or c.get("is_key"):
                label += " [PK]"
            if c.get("is_calculated_column"):
                label += "*"
            cols.append(label)
        fill, outline = fills[name]
        h = 40 + 16 * len(cols)
        tbox((x, y, x + 320, y + h), name, cols, fill, outline)
        # line to center
        draw.line((x + 160, y + h / 2, 1100, 720), fill=(120, 120, 120), width=2)
        rel = next(r for r in a2["relationships"] if r["to_table"] == name)
        draw.text((x + 80, y + h + 2), f"M:1 on {rel['from_column']}", fill=(80, 80, 80), font=font_s)

    # Internal strip at bottom
    draw.rectangle((40, 1450, 2160, 1570), fill=(255, 245, 245), outline=(160, 60, 60), width=2)
    draw.text((55, 1460), "INTERNAL auto-date calculated tables (SKIP for LookML) — no business relationships in inventory:", fill=(120, 40, 40), font=font)
    internals = [short_internal(t["table_name"]) for t in a1["tables"] if is_internal(t["table_name"])]
    draw.text((55, 1495), "  |  ".join(internals), fill=(80, 40, 40), font=font_s)
    draw.text((55, 1525), "Each typically: Date, Year, MonthNo, Month, QuarterNo, Quarter, Day  (+ Date Hierarchy)", fill=(80, 40, 40), font=font_s)

    img.save(PNG_OUT)
    print("Wrote", PNG_OUT)


def main():
    MD_OUT.write_text(build_markdown(), encoding="utf-8")
    print("Wrote", MD_OUT)
    make_pdf()
    make_png()


if __name__ == "__main__":
    main()
