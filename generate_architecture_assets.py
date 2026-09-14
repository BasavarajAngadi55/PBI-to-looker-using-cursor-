#!/usr/bin/env python3
"""Generate agentic architecture PDF + PNG for PBIX -> Looker 6-agent system."""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "AGENTIC_ARCHITECTURE.pdf"
PNG_OUT = ROOT / "AGENTIC_ARCHITECTURE.png"
MD_OUT = ROOT / "AGENTIC_ARCHITECTURE.md"


class ArchPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "PBIX to Looker - 6-Agent Agentic Architecture", align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            10,
            f"Page {self.page_no()}/{{nb}}  |  github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-",
            align="C",
        )

    def h1(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 10, text)
        self.ln(2)

    def h2(self, text):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 60, 110)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=6):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin + indent)
        usable = self.w - self.l_margin - self.r_margin - indent
        self.multi_cell(usable, 5.5, f"- {text}")

    def box(self, x, y, w, h, title, lines, fill=(232, 240, 254), border=(40, 80, 140)):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 2, y + 2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(20, 40, 80)
        self.cell(w - 4, 5, title)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(40, 40, 40)
        ty = y + 8
        for line in lines:
            self.set_xy(x + 2, ty)
            self.cell(w - 4, 4, line)
            ty += 4

    def arrow_down(self, x, y1, y2):
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.5)
        self.line(x, y1, x, y2)
        self.line(x, y2, x - 2, y2 - 3)
        self.line(x, y2, x + 2, y2 - 3)

    def callout(self, title, text):
        usable = self.w - self.l_margin - self.r_margin
        self.set_x(self.l_margin)
        self.set_fill_color(245, 248, 252)
        self.set_draw_color(60, 100, 160)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 60, 110)
        self.multi_cell(usable, 6, title, fill=True)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(usable, 5, text, fill=True)
        self.ln(2)


def draw_diagram_page(pdf: ArchPDF):
    pdf.add_page()
    pdf.h1("6-Agent Agentic Architecture")
    pdf.body(
        "Power BI (.pbix) semantic model inventory for Google Looker migration. "
        "Reports/visuals/dashboards are out of scope. Phase 1 = inventory only; "
        "LookML and warehouse SQL only after Completeness Gate = PASS."
    )

    left = pdf.l_margin
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    y = pdf.get_y() + 2

    # INPUT
    pdf.box(left + usable * 0.2, y, usable * 0.6, 16, "INPUT", [
        "Human Resources Sample PBIX (or your .pbix)",
        "Extracted via pbixray - no invented objects",
    ], fill=(255, 245, 230), border=(180, 100, 40))
    pdf.arrow_down(left + usable * 0.5, y + 16, y + 22)
    y += 24

    # ORCHESTRATOR
    pdf.box(left, y, usable, 18, "ORCHESTRATOR (Cursor Agent)", [
        "Checks PBIX path - creates inventory/ - runs Agents 1-5 - validates files exist",
        "Only then runs Merger - prints Phase 1 report - blocks LookML if gate FAIL",
        "Script: inventory/run_phase1_six_agents.py",
    ], fill=(230, 245, 235), border=(40, 120, 70))
    pdf.arrow_down(left + usable * 0.5, y + 18, y + 24)
    y += 26

    # 5 specialists
    gap = 2.5
    bw = (usable - 4 * gap) / 5
    labels = [
        ("1 Schema", ["tables", "columns", "calc tables", "internal dates"]),
        ("2 Relations", ["from/to", "cardinality", "cross-filter", "active"]),
        ("3 DAX", ["measures", "calc cols", "calc tables", "complexity"]),
        ("4 Power Query", ["full M code", "SQL tags", "04_m_raw/", "seeds"]),
        ("5 TM Extras", ["partitions", "hierarchies", "RLS=[]", "auto dates"]),
    ]
    colors = [
        (232, 240, 254),
        (236, 245, 255),
        (240, 236, 255),
        (255, 240, 245),
        (240, 250, 245),
    ]
    for i, ((title, lines), fill) in enumerate(zip(labels, colors)):
        pdf.box(left + i * (bw + gap), y, bw, 28, title, lines, fill=fill)
    pdf.arrow_down(left + usable * 0.5, y + 28, y + 34)
    y += 36

    # Artifacts strip
    pdf.box(left, y, usable, 14, "SPECIALIST ARTIFACTS (do not invent; empty = [])", [
        "01_tables_columns.json - 03_relationships.json - 02_dax_objects.json - "
        "04_power_query_m.json + 04_m_raw/*.m - 05_tmschema_extras.json",
    ], fill=(250, 250, 250), border=(100, 100, 100))
    pdf.arrow_down(left + usable * 0.5, y + 14, y + 20)
    y += 22

    # Merger
    pdf.box(left, y, usable, 16, "6. MERGER AGENT", [
        "OBJECT_INVENTORY.md - ACTION_MATRIX.csv - COMPLETENESS_GATE.json",
        "One primary action per object: LOOKML_* | WAREHOUSE_* | SKIP_PBI_INTERNAL | NONE_IN_SOURCE",
    ], fill=(255, 248, 230), border=(160, 120, 40))
    pdf.arrow_down(left + usable * 0.5, y + 16, y + 22)
    y += 24

    # Gate
    half = (usable - gap) / 2
    pdf.box(left, y, half, 20, "GATE = PASS", [
        "Tables/cols/measures/M match",
        "Proceed to Phase 2+",
    ], fill=(220, 245, 220), border=(40, 130, 60))
    pdf.box(left + half + gap, y, half, 20, "GATE = FAIL", [
        "Missing objects / files",
        "STOP - do not claim LookML ready",
    ], fill=(255, 230, 230), border=(160, 50, 50))
    pdf.arrow_down(left + half * 0.5, y + 20, y + 26)
    y += 28

    # Phase 2+
    pdf.box(left, y, usable, 16, "PHASE 2+ (only after PASS)", [
        "Warehouse SQL / seeds from M  ->  LookML views + model  ->  KPI parity vs Power BI",
        "Thesis: Capture everything. Tag everything. Block with names. Then build LookML.",
    ], fill=(235, 245, 255), border=(50, 90, 150))


def write_explanation_pages(pdf: ArchPDF):
    pdf.add_page()
    pdf.h2("1. Why an agentic architecture?")
    pdf.body(
        "A PBIX is not one LookML file waiting to happen. It packs tabular schema, "
        "relationships, DAX, Power Query M, and TM extras (partitions, hierarchies, RLS, "
        "auto date tables). A single convert-to-LookML pass typically skips M dependencies, "
        "stubs complex DAX without disclosure, drops LocalDateTable_* objects, and omits "
        "empty categories instead of confirming NONE_IN_SOURCE."
    )
    pdf.bullet("Specialists = one contract each -> less hallucination / skipped categories")
    pdf.bullet("Empty categories must be listed as empty (e.g. RLS: [])")
    pdf.bullet("Merger enforces a hard completeness gate before LookML is trusted")
    pdf.ln(2)

    pdf.h2("2. How the system works (runtime)")
    pdf.bullet("Step 1 - Verify PBIX path exists")
    pdf.bullet("Step 2 - Create inventory/ and inventory/04_m_raw/")
    pdf.bullet("Step 3 - Run Agents 1-5 (schema, relationships, DAX, M, TM extras)")
    pdf.bullet("Step 4 - Orchestrator validates all specialist JSON + .m files exist")
    pdf.bullet("Step 5 - Run Merger Agent")
    pdf.bullet("Step 6 - Emit OBJECT_INVENTORY.md, ACTION_MATRIX.csv, COMPLETENESS_GATE.json")
    pdf.bullet("Step 7 - Print Phase 1 report (counts + PASS/FAIL + blockers)")
    pdf.ln(1)
    pdf.callout(
        "Hard rule",
        "Do NOT generate warehouse SQL or LookML while Completeness Gate = FAIL. "
        "Phase 1 purpose is a complete, trustworthy semantic-model inventory.",
    )

    pdf.h2("3. Agent responsibilities")
    pdf.bullet("Agent 1 Schema -> every table/column including LocalDateTable_* and DateTableTemplate_*")
    pdf.bullet("Agent 2 Relationships -> from/to, cardinality, cross-filter, active/inactive")
    pdf.bullet("Agent 3 DAX -> full measure/calc column/calc table expressions + SIMPLE/MODERATE/COMPLEX")
    pdf.bullet("Agent 4 M -> verbatim Power Query to 04_m_raw/<Table>.m + SQL/seed/union tags")
    pdf.bullet("Agent 5 TM Extras -> partitions, hierarchies, RLS/OLS, perspectives, annotations, auto dates")
    pdf.bullet("Agent 6 Merger -> inventory markdown, action matrix, gate JSON")
    pdf.ln(2)

    pdf.h2("4. Dependency chain the architecture protects")
    pdf.set_font("Courier", "", 9)
    pdf.set_x(pdf.l_margin)
    pdf.set_fill_color(240, 240, 240)
    pdf.multi_cell(
        0,
        5,
        "M (Power Query)  ->  warehouse tables / seeds\n"
        "                ->  calculated columns\n"
        "                ->  measures / LookML\n"
        "relationships    ->  LookML joins\n"
        "Date/PeriodNumber ->  SPLY, EmpCount, YoY",
        fill=True,
    )
    pdf.ln(3)

    pdf.h2("5. HR Sample results (this repo)")
    pdf.bullet("Tables 15 (9 business + 6 internal auto date)")
    pdf.bullet("Columns 87 - Measures 30 - Calc columns 43 - Calc tables 6")
    pdf.bullet("Relationships 8 (all M:1, Single, active)")
    pdf.bullet("Power Query 9 (.m files) - RLS 0 (captured empty)")
    pdf.bullet("Completeness Gate: PASS")
    pdf.ln(2)

    pdf.h2("6. Known blockers after inventory")
    pdf.bullet("Employee.m must load to warehouse before runnable HR KPIs")
    pdf.bullet("SAMEPERIODLASTYEAR / max PeriodNumber EmpCount / TO % Norm -> LOOKML_TODO_COMPLEX")
    pdf.bullet("KPI parity vs Power BI remains PENDING until data + complex DAX patterns exist")
    pdf.ln(2)

    pdf.h2("7. How to re-run")
    pdf.set_font("Courier", "", 9)
    pdf.set_x(pdf.l_margin)
    pdf.set_fill_color(240, 240, 240)
    pdf.multi_cell(
        0,
        5,
        "python3.12 -m venv .venv312\n"
        "source .venv312/bin/activate\n"
        "pip install pbixray pandas fpdf2\n"
        "python inventory/run_phase1_six_agents.py\n"
        "python generate_architecture_assets.py",
        fill=True,
    )
    pdf.ln(3)
    pdf.body(
        "Full reusable prompt: PROMPT.md. LookML builder guide (after gate PASS): "
        "LOOKML_DEVELOPER_GUIDE.md. Repo: https://github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-"
    )


def write_markdown():
    MD_OUT.write_text(
        """# Agentic Architecture - PBIX -> Looker (6 Agents)

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png** for the diagram + full explanation.

## Flow

```text
PBIX
  -> Orchestrator
      -> Agent 1 Schema      -> 01_tables_columns.json
      -> Agent 2 Relations   -> 03_relationships.json
      -> Agent 3 DAX         -> 02_dax_objects.json
      -> Agent 4 Power Query -> 04_power_query_m.json + 04_m_raw/*.m
      -> Agent 5 TM Extras   -> 05_tmschema_extras.json
  -> Merger (only if files exist)
      -> OBJECT_INVENTORY.md
      -> ACTION_MATRIX.csv
      -> COMPLETENESS_GATE.json  (PASS | FAIL)
  -> if PASS -> warehouse -> LookML -> KPI parity
```

## Thesis

Capture everything. Tag everything. Block with names. Then build LookML.

## Run

```bash
.venv312/bin/python inventory/run_phase1_six_agents.py
.venv312/bin/python generate_architecture_assets.py
```
""",
        encoding="utf-8",
    )


def render_png():
    """Draw a simple architecture PNG with Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed - skipping PNG (PDF still written)")
        return False

    W, H = 1600, 2000
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font_b = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except Exception:
        font_b = font = font_s = ImageFont.load_default()

    def rounded_box(xy, fill, outline, title, lines, title_fill=None):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle(xy, radius=12, fill=fill, outline=outline, width=3)
        draw.text((x1 + 16, y1 + 12), title, fill=(20, 40, 80), font=font_b)
        ty = y1 + 50
        for line in lines:
            draw.text((x1 + 16, ty), line, fill=(40, 40, 40), font=font_s)
            ty += 22

    def arrow(x, y1, y2):
        draw.line((x, y1, x, y2), fill=(80, 80, 80), width=3)
        draw.polygon([(x, y2), (x - 8, y2 - 12), (x + 8, y2 - 12)], fill=(80, 80, 80))

    margin = 60
    draw.text((margin, 30), "PBIX -> Looker - 6-Agent Agentic Architecture", fill=(20, 40, 80), font=font_b)
    draw.text(
        (margin, 70),
        "Inventory-first migration | Reports/visuals out of scope | Gate before LookML",
        fill=(80, 80, 80),
        font=font,
    )

    y = 120
    rounded_box(
        (400, y, 1200, y + 90),
        (255, 245, 230),
        (180, 100, 40),
        "INPUT: .pbix",
        ["Semantic model only - pbixray extraction - never invent objects"],
    )
    arrow(800, y + 90, y + 120)
    y += 130

    rounded_box(
        (margin, y, W - margin, y + 110),
        (230, 245, 235),
        (40, 120, 70),
        "ORCHESTRATOR",
        [
            "Validate PBIX - run Agents 1-5 - require output files - then Merger",
            "Script: inventory/run_phase1_six_agents.py",
        ],
    )
    arrow(800, y + 110, y + 140)
    y += 150

    # five agents
    gap = 16
    aw = (W - 2 * margin - 4 * gap) // 5
    agents = [
        ("1 Schema", ["tables/cols", "calc tables", "internal dates"], (232, 240, 254)),
        ("2 Relations", ["cardinality", "cross-filter", "active"], (236, 245, 255)),
        ("3 DAX", ["measures", "calc cols", "complexity"], (240, 236, 255)),
        ("4 M / PQ", ["full M", "SQL/seeds", "04_m_raw"], (255, 240, 245)),
        ("5 TM Extras", ["hierarchies", "RLS=[]", "auto dates"], (240, 250, 245)),
    ]
    for i, (title, lines, fill) in enumerate(agents):
        x1 = margin + i * (aw + gap)
        rounded_box((x1, y, x1 + aw, y + 140), fill, (60, 90, 140), title, lines)
    arrow(800, y + 140, y + 170)
    y += 180

    rounded_box(
        (margin, y, W - margin, y + 90),
        (250, 250, 250),
        (100, 100, 100),
        "ARTIFACTS",
        ["01_tables - 03_rel - 02_dax - 04_m + 04_m_raw/*.m - 05_tm_extras"],
    )
    arrow(800, y + 90, y + 120)
    y += 130

    rounded_box(
        (margin, y, W - margin, y + 100),
        (255, 248, 230),
        (160, 120, 40),
        "6. MERGER",
        [
            "OBJECT_INVENTORY.md - ACTION_MATRIX.csv - COMPLETENESS_GATE.json",
            "Actions: LOOKML_* | WAREHOUSE_* | SKIP_PBI_INTERNAL | NONE_IN_SOURCE",
        ],
    )
    arrow(800, y + 100, y + 130)
    y += 140

    mid = W // 2
    rounded_box(
        (margin, y, mid - 10, y + 100),
        (220, 245, 220),
        (40, 130, 60),
        "PASS",
        ["Counts match extraction", "-> Phase 2+ allowed"],
    )
    rounded_box(
        (mid + 10, y, W - margin, y + 100),
        (255, 230, 230),
        (160, 50, 50),
        "FAIL",
        ["Missing objects/files", "STOP - no LookML claim"],
    )
    arrow(margin + (mid - margin) // 2, y + 100, y + 130)
    y += 140

    rounded_box(
        (margin, y, W - margin, y + 110),
        (235, 245, 255),
        (50, 90, 150),
        "PHASE 2+ (after PASS only)",
        [
            "Warehouse SQL/seeds from M -> LookML views/model -> KPI parity",
            "Thesis: Capture everything. Tag everything. Block with names. Then build LookML.",
        ],
    )

    y = H - 80
    draw.text(
        (margin, y),
        "github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-",
        fill=(80, 80, 80),
        font=font,
    )
    draw.text(
        (margin, y + 30),
        "HR Sample gate: 15 tables - 30 measures - 9 M - 8 joins - RLS=[] - PASS",
        fill=(80, 80, 80),
        font=font_s,
    )

    img.save(PNG_OUT, "PNG")
    print(f"Wrote {PNG_OUT}")
    return True


def main():
    write_markdown()
    pdf = ArchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    draw_diagram_page(pdf)
    write_explanation_pages(pdf)
    pdf.output(str(PDF_OUT))
    print(f"Wrote {PDF_OUT}")
    render_png()
    print(f"Wrote {MD_OUT}")


if __name__ == "__main__":
    main()
