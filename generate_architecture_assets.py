#!/usr/bin/env python3
"""Generate updated 3-phase agentic architecture PDF + PNG."""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "AGENTIC_ARCHITECTURE.pdf"
PNG_OUT = ROOT / "AGENTIC_ARCHITECTURE.png"
MD_OUT = ROOT / "AGENTIC_ARCHITECTURE.md"


def latin1(s: str) -> str:
    repl = {
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u2192": "->", "·": "-", "—": "-", "–": "-",
    }
    for a, b in repl.items():
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


class ArchPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, latin1("PBIX to Looker - 3-Phase Agentic Architecture"), align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            10,
            latin1(f"Page {self.page_no()}/{{nb}} | github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-"),
            align="C",
        )

    def h1(self, t):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 10, latin1(t))
        self.ln(2)

    def h2(self, t):
        self.ln(2)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 60, 110)
        self.multi_cell(0, 8, latin1(t))
        self.ln(1)

    def body(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, latin1(t))
        self.ln(1)

    def bullet(self, t, indent=6):
        self.set_font("Helvetica", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, latin1(f"- {t}"))

    def box(self, x, y, w, h, title, lines, fill=(232, 240, 254), border=(40, 80, 140)):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 2, y + 2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(20, 40, 80)
        self.cell(w - 4, 5, latin1(title))
        self.set_font("Helvetica", "", 7)
        self.set_text_color(40, 40, 40)
        ty = y + 8
        for line in lines:
            self.set_xy(x + 2, ty)
            self.cell(w - 4, 4, latin1(line)[:70])
            ty += 4

    def arrow_down(self, x, y1, y2):
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.5)
        self.line(x, y1, x, y2)
        self.line(x, y2, x - 2, y2 - 3)
        self.line(x, y2, x + 2, y2 - 3)


def page_overview(pdf: ArchPDF):
    pdf.add_page()
    pdf.h1("3-Phase Agentic Architecture")
    pdf.body(
        "Power BI (.pbix) to Google Looker migration using specialist Cursor agents. "
        "Reports/visuals are out of scope. Base warehouse tables are assumed to exist; "
        "agents capture inventory, map to LookML, and implement gaps (M/DAX) + LookML."
    )

    left = pdf.l_margin
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    y = pdf.get_y() + 2
    cx = left + usable / 2

    pdf.box(left + usable * 0.15, y, usable * 0.7, 14, "INPUT: .pbix", [
        "Semantic model only | pbixray | never invent objects",
    ], fill=(255, 245, 230), border=(180, 100, 40))
    pdf.arrow_down(cx, y + 14, y + 20)
    y += 22

    # Phase 1
    pdf.box(left, y, usable, 36, "PHASE 1 - Inventory Orchestrator (6 agents)", [
        "1 Schema | 2 Relationships | 3 DAX | 4 Power Query M | 5 TM Extras",
        "6 Merger -> OBJECT_INVENTORY + ACTION_MATRIX + COMPLETENESS_GATE",
        "Script: inventory/run_phase1_six_agents.py | Gate must PASS before Phase 2",
    ], fill=(230, 245, 235), border=(40, 120, 70))
    pdf.arrow_down(cx, y + 36, y + 42)
    y += 44

    # Phase 2
    pdf.box(left, y, usable, 36, "PHASE 2 - Mapping Orchestrator (4 agents)", [
        "A Tables/Columns mapping | B DAX measures/calc mapping",
        "C Relationships + M + TM extras mapping | D Merger assessment",
        "Output: LOOKML_MAPPING_ASSESSMENT.md/.pdf | phase2_agents/ | Gate PASS",
    ], fill=(232, 240, 254), border=(40, 80, 140))
    pdf.arrow_down(cx, y + 36, y + 42)
    y += 44

    # Phase 3
    pdf.box(left, y, usable, 40, "PHASE 3 - Implementation Orchestrator (subagents)", [
        "W Warehouse gaps (seeds/calc only if missing on base tables)",
        "L LookML views/measures/joins accountability",
        "Docs: MIGRATION_SUMMARY + LOOKER_DEVELOPER_GUIDE + COVERAGE",
        "Output folder: phase3/ | Coverage PARTIAL until SPLY/EmpCount/TO%Norm + KPI parity",
    ], fill=(255, 248, 230), border=(160, 120, 40))
    pdf.arrow_down(cx, y + 40, y + 46)
    y += 48

    half = (usable - 4) / 2
    pdf.box(left, y, half, 18, "DONE when accountable", [
        "Every object IMPLEMENTED/PARTIAL/TODO/SKIP",
        "KPI parity separate validation step",
    ], fill=(220, 245, 220), border=(40, 130, 60))
    pdf.box(left + half + 4, y, half, 18, "NOT forced conversion", [
        "Complex DAX stays TODO - never fake",
        "Base tables assumed - capture M/DAX gaps",
    ], fill=(255, 230, 230), border=(160, 50, 50))


def page_detail(pdf: ArchPDF):
    pdf.add_page()
    pdf.h2("Phase 1 agents (extract)")
    pdf.bullet("Schema -> inventory/01_tables_columns.json")
    pdf.bullet("Relationships -> 03_relationships.json")
    pdf.bullet("DAX -> 02_dax_objects.json (full expressions)")
    pdf.bullet("Power Query M -> 04_power_query_m.json + 04_m_raw/*.m")
    pdf.bullet("TM Extras -> 05_tmschema_extras.json (RLS=[] if none)")
    pdf.bullet("Merger -> OBJECT_INVENTORY.md, ACTION_MATRIX.csv, COMPLETENESS_GATE.json")
    pdf.ln(1)

    pdf.h2("Phase 2 agents (map only - no LookML)")
    pdf.bullet("Agent A - tables/columns -> phase2_agents/01_tables_columns_mapping.md")
    pdf.bullet("Agent B - measures/calc -> phase2_agents/02_dax_mapping.md")
    pdf.bullet("Agent C - joins/M/TM -> phase2_agents/03_rels_m_tm_mapping.md")
    pdf.bullet("Agent D Merger -> LOOKML_MAPPING_ASSESSMENT.md + PDF + PHASE2_MERGE_GATE.json")
    pdf.ln(1)

    pdf.h2("Phase 3 agents (implement)")
    pdf.bullet("Agent W - warehouse gaps only (base tables exist) -> phase3_agents/01_warehouse_gaps.md")
    pdf.bullet("Agent L - LookML accountability -> phase3_agents/02_lookml_accountability.md")
    pdf.bullet("Deliverables under phase3/: views/, models/, warehouse_sql/ templates, guides, coverage")
    pdf.ln(1)

    pdf.h2("Dependency chain")
    pdf.set_font("Courier", "", 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.multi_cell(
        0,
        5,
        latin1(
            "PBIX\n"
            "  -> Phase1 inventory (gate PASS)\n"
            "  -> Phase2 mapping assessment (gate PASS)\n"
            "  -> Phase3 LookML + gap SQL (coverage PARTIAL/PASS)\n"
            "  -> KPI parity validation (separate)\n\n"
            "M / calc gaps -> warehouse add-ons (only if not on base)\n"
            "relationships -> LookML joins\n"
            "Date/PeriodNumber -> SPLY / EmpCount (TODO until PoP)"
        ),
        fill=True,
    )
    pdf.ln(3)

    pdf.h2("Thesis")
    pdf.body(
        "Capture everything. Tag everything. Map with specialists. "
        "Implement with accountability. Block with names. Never silently drop objects. "
        "Do not claim KPI parity until compared to Power BI."
    )


def write_md():
    MD_OUT.write_text(
        """# Agentic Architecture — 3 Phases (Updated)

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png**.

## Overview

```text
PBIX
  └─ PHASE 1 Inventory Orchestrator
        ├─ Agent 1 Schema
        ├─ Agent 2 Relationships
        ├─ Agent 3 DAX
        ├─ Agent 4 Power Query M
        ├─ Agent 5 TM Extras
        └─ Agent 6 Merger + COMPLETENESS_GATE (must PASS)
              │
              ▼
         PHASE 2 Mapping Orchestrator
        ├─ Agent A Tables/Columns
        ├─ Agent B DAX Measures/Calc
        ├─ Agent C Rel / M / TM
        └─ Agent D Merger -> LOOKML_MAPPING_ASSESSMENT (+ PDF)
              │
              ▼
         PHASE 3 Implementation Orchestrator
        ├─ Agent W Warehouse gaps (base tables assumed)
        ├─ Agent L LookML accountability
        └─ Outputs in phase3/ (views, model, gap SQL templates, docs)
              │
              ▼
         KPI Parity Validation (not automatic)
```

## Folders

| Phase | Path |
|-------|------|
| 1 | `inventory/` |
| 2 | `phase2_agents/` + `LOOKML_MAPPING_ASSESSMENT.*` |
| 3 | `phase3/` + `phase3_agents/` |

## Principle

**100% object accountability**, not 100% forced conversion.

Base warehouse tables are assumed present. Capture **M/DAX gaps** (seeds, transforms, calculated columns) and build LookML on top.
""",
        encoding="utf-8",
    )


def render_png():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow missing - skip PNG")
        return

    W, H = 1600, 2200
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font_b = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_s = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
    except Exception:
        font_b = font = font_s = ImageFont.load_default()

    def box(xy, fill, outline, title, lines):
        draw.rounded_rectangle(xy, radius=14, fill=fill, outline=outline, width=3)
        x1, y1, _, _ = xy
        draw.text((x1 + 18, y1 + 14), title, fill=(20, 40, 80), font=font_b)
        ty = y1 + 52
        for line in lines:
            draw.text((x1 + 18, ty), line, fill=(40, 40, 40), font=font_s)
            ty += 24

    def arrow(x, y1, y2):
        draw.line((x, y1, x, y2), fill=(80, 80, 80), width=3)
        draw.polygon([(x, y2), (x - 8, y2 - 12), (x + 8, y2 - 12)], fill=(80, 80, 80))

    m = 60
    draw.text((m, 30), "PBIX -> Looker: 3-Phase Agentic Architecture", fill=(20, 40, 80), font=font_b)
    draw.text((m, 70), "Specialist agents per phase | Base tables assumed | Account for every object", fill=(80, 80, 80), font=font)

    y = 120
    box((400, y, 1200, y + 90), (255, 245, 230), (180, 100, 40), "INPUT .pbix", [
        "Semantic model extraction via pbixray - never invent objects",
    ])
    arrow(800, y + 90, y + 120)
    y += 130

    box((m, y, W - m, y + 160), (230, 245, 235), (40, 120, 70), "PHASE 1 - Inventory (6 agents)", [
        "Schema | Relationships | DAX | Power Query M | TM Extras",
        "Merger -> inventory/ + COMPLETENESS_GATE (PASS required)",
        "run_phase1_six_agents.py",
    ])
    arrow(800, y + 160, y + 190)
    y += 200

    box((m, y, W - m, y + 160), (232, 240, 254), (40, 80, 140), "PHASE 2 - Mapping (4 agents)", [
        "A Tables/Columns | B DAX | C Rel/M/TM | D Merger",
        "LOOKML_MAPPING_ASSESSMENT.md + PDF | phase2_agents/",
        "Analysis only - no LookML generation",
    ])
    arrow(800, y + 160, y + 190)
    y += 200

    box((m, y, W - m, y + 180), (255, 248, 230), (160, 120, 40), "PHASE 3 - Implementation (subagents)", [
        "W Warehouse gaps (M/DAX only if not on base tables)",
        "L LookML views / measures / joins accountability",
        "Outputs: phase3/views, models, warehouse_sql templates, docs",
        "Coverage PARTIAL until complex DAX + KPI parity",
    ])
    arrow(800, y + 180, y + 210)
    y += 220

    mid = W // 2
    box((m, y, mid - 12, y + 120), (220, 245, 220), (40, 130, 60), "Accountable", [
        "IMPLEMENTED / PARTIAL / TODO / SKIP",
        "Nothing silently dropped",
    ])
    box((mid + 12, y, W - m, y + 120), (255, 230, 230), (160, 50, 50), "Not complete yet", [
        "SPLY / EmpCount / TO % Norm = TODO",
        "KPI parity NOT VALIDATED",
    ])

    draw.text((m, H - 70), "github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-", fill=(80, 80, 80), font=font)
    draw.text((m, H - 40), "Thesis: Capture -> Map -> Implement gaps -> Validate KPIs", fill=(80, 80, 80), font=font_s)
    img.save(PNG_OUT)
    print("Wrote", PNG_OUT)


def main():
    write_md()
    pdf = ArchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    page_overview(pdf)
    page_detail(pdf)
    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)
    render_png()


if __name__ == "__main__":
    main()
