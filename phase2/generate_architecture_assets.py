#!/usr/bin/env python3
"""Phase-2 deterministic LookML mapping architecture diagram (PDF + PNG + MD).

Look-and-feel matches phase1/generate_architecture_assets.py (dark navy cards,
teal/coral/gold accents, stage cards, orchestrator flow).
"""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "AGENTIC_ARCHITECTURE.pdf"
PNG_OUT = ROOT / "AGENTIC_ARCHITECTURE.png"
MD_OUT = ROOT / "AGENTIC_ARCHITECTURE.md"

BG = (18, 32, 48)
CARD = (28, 48, 68)
INK = (240, 245, 250)
MUTED = (170, 190, 210)
TEAL = (32, 178, 166)
CORAL = (255, 120, 90)
GOLD = (255, 196, 84)
SKY = (90, 170, 230)
LIME = (120, 210, 140)
VIOLET = (140, 160, 220)


def font(size: int, bold: bool = False):
    path = "/System/Library/Fonts/Helvetica.ttc"
    try:
        return ImageFont.truetype(path, size, index=1 if bold else 0)
    except Exception:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()


def rounded(draw, xy, fill, outline=None, width=2, radius=18):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def stage_card(draw, x, y, w, h, num, title, role, does, color):
    rounded(draw, (x, y, x + w, y + h), fill=CARD, outline=color, width=3, radius=16)
    draw.ellipse((x + 14, y + 14, x + 52, y + 52), fill=color)
    draw.text((x + 24, y + 20), str(num), fill=BG, font=font(20, True))
    draw.text((x + 62, y + 18), title, fill=INK, font=font(18, True))
    draw.text((x + 62, y + 42), role, fill=color, font=font(13, True))
    yy = y + 70
    for line in does:
        draw.text((x + 18, yy), f"- {line}", fill=MUTED, font=font(12))
        yy += 18


def make_png():
    W, H = 1600, 1680
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    rounded(d, (40, 30, W - 40, 165), fill=(24, 42, 62), outline=TEAL, width=2, radius=20)
    d.text((70, 48), "PBIX  ->  Looker", fill=TEAL, font=font(18, True))
    d.text((70, 76), "Deterministic LookML Mapping  |  Phase 2", fill=INK, font=font(30, True))
    d.text(
        (70, 118),
        "No LLM in mapping  ·  fixed Python rules + looker-skills patterns  ·  no invent  ·  LookML out",
        fill=MUTED,
        font=font(14),
    )
    d.text(
        (70, 140),
        "Input is Phase 1 inventory only  ·  warehouse/ETL documented as gaps  ·  KPI parity not automatic",
        fill=GOLD,
        font=font(13),
    )

    rounded(d, (40, 190, 520, 310), fill=CARD, outline=GOLD, width=3, radius=16)
    d.text((60, 208), "INPUT", fill=GOLD, font=font(14, True))
    d.text((60, 234), "Phase 1 inventory JSON", fill=INK, font=font(22, True))
    d.text((60, 266), "Tables · DAX · M · relationships · TM", fill=MUTED, font=font(13))
    d.text((60, 286), "Source: phase1/inventory/*.json", fill=MUTED, font=font(13))

    rounded(d, (560, 190, W - 40, 310), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((580, 208), "ORCHESTRATOR (deterministic)", fill=LIME, font=font(14, True))
    d.text((580, 234), "Runs the 6-stage mapping pipeline", fill=INK, font=font(22, True))
    d.text((580, 266), "Stages 1-5  ->  Packager 6  ->  ZIP + Guide PDF", fill=MUTED, font=font(13))
    d.text((580, 286), "Fixed code paths · never invents objects · no LLM", fill=MUTED, font=font(13))

    d.line((280, 310, 280, 350), fill=MUTED, width=3)
    d.line((1080, 310, 1080, 350), fill=MUTED, width=3)
    d.line((280, 350, 1080, 350), fill=MUTED, width=3)
    d.line((800, 350, 800, 380), fill=MUTED, width=3)
    d.polygon([(790, 380), (810, 380), (800, 395)], fill=TEAL)

    d.text((500, 405), "MAPPING STAGES 1-5  ·  DETERMINISTIC (same inventory = same LookML)", fill=TEAL, font=font(15, True))

    stages = [
        (
            1,
            "Ingest",
            "ROLE: Load inventory",
            ["Read 01..05 JSON", "OBJECT_COUNTS.json", "Detect fact table", "Skip LocalDate*"],
            SKY,
        ),
        (
            2,
            "Equivalence",
            "ROLE: Object map",
            ["PBI -> Looker rules", "Build OBJECT_MAPPING", "Flag HIGH gaps", "looker-skills rules"],
            TEAL,
        ),
        (
            3,
            "Views",
            "ROLE: Dimensions",
            ["One view per table", "primary_key: yes", "dimension_group dates", "Calc cols as dims"],
            CORAL,
        ),
        (
            4,
            "Model/Joins",
            "ROLE: Explore graph",
            ["Model + connection", "Explore on fact", "Joins + relationship", "Alias inactive/M:M"],
            GOLD,
        ),
        (
            5,
            "Measures",
            "ROLE: DAX patterns",
            ["SUM/AVG/COUNT map", "SAFE_DIVIDE ratios", "Complex DAX = TODO", "Keep original DAX"],
            LIME,
        ),
    ]

    gap = 18
    card_w = (W - 80 - 4 * gap) // 5
    card_h = 220
    y0 = 440
    for i, (num, title, role, does, color) in enumerate(stages):
        x = 40 + i * (card_w + gap)
        stage_card(d, x, y0, card_w, card_h, num, title, role, does, color)
        cx = x + card_w // 2
        d.line((cx, y0 + card_h, cx, y0 + card_h + 30), fill=MUTED, width=2)
        d.line((cx, y0 + card_h + 30, 800, y0 + card_h + 55), fill=MUTED, width=2)

    d.polygon([(790, y0 + card_h + 55), (810, y0 + card_h + 55), (800, y0 + card_h + 70)], fill=CORAL)

    my = y0 + card_h + 85
    rounded(d, (40, my, W - 40, my + 120), fill=CARD, outline=CORAL, width=3, radius=18)
    d.ellipse((70, my + 30, 120, my + 80), fill=CORAL)
    d.text((85, my + 43), "6", fill=BG, font=font(24, True))
    d.text((145, my + 22), "Packager (deterministic)", fill=INK, font=font(24, True))
    d.text((145, my + 52), "ROLE: Guide + ZIP + summary", fill=CORAL, font=font(14, True))
    d.text(
        (145, my + 78),
        "LOOKER_DEVELOPER_GUIDE.pdf  ·  LOOKML_PROJECT.zip  ·  GAPS.json  ·  PHASE2_SUMMARY.json",
        fill=MUTED,
        font=font(13),
    )
    d.text(
        (145, my + 98),
        "Full build instructions  ·  prioritized gaps  ·  validation checklists  ·  no LLM",
        fill=MUTED,
        font=font(13),
    )

    oy = my + 145
    rounded(d, (40, oy, 760, oy + 140), fill=CARD, outline=SKY, width=3, radius=16)
    d.text((60, oy + 14), "LOOKML OUTPUTS", fill=SKY, font=font(14, True))
    outs = [
        "lookml/manifest.lkml",
        "lookml/models/<pbix>.model.lkml",
        "lookml/views/*.view.lkml",
        "OBJECT_MAPPING.md + .json",
        "GAPS.json (HIGH / MEDIUM / LOW)",
        "PHASE2_SUMMARY.json",
    ]
    for i, line in enumerate(outs):
        d.text((60, oy + 42 + i * 15), f"- {line}", fill=MUTED, font=font(12))

    rounded(d, (800, oy, W - 40, oy + 140), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((820, oy + 14), "FINAL DELIVERABLES", fill=LIME, font=font(14, True))
    d.text((820, oy + 48), "LOOKML ZIP", fill=INK, font=font(24, True))
    d.text((820, oy + 80), "+ Developer Guide PDF", fill=INK, font=font(18, True))
    d.text((820, oy + 108), "UI download  ·  import into Looker", fill=MUTED, font=font(13))

    fy = oy + 160
    rounded(d, (40, fy, W - 40, fy + 120), fill=CARD, outline=VIOLET, width=3, radius=16)
    d.text(
        (60, fy + 16),
        "DEVELOPER WORK AFTER PHASE 2 (not automated)",
        fill=VIOLET,
        font=font(14, True),
    )
    d.text((60, fy + 44), "Set connection + warehouse tables  ·  close HIGH gaps  ·  validate LookML", fill=INK, font=font(18, True))
    d.text(
        (60, fy + 74),
        "Rebuild Power Query M in ETL/dbt  ·  materialize calculated columns  ·  implement complex DAX TODOs",
        fill=MUTED,
        font=font(13),
    )
    d.text(
        (60, fy + 94),
        "Side-by-side KPI checks vs Power BI before publishing — parity is never assumed.",
        fill=MUTED,
        font=font(13),
    )

    d.text(
        (40, H - 36),
        "Hard rules: never invent  |  inventory-only input  |  PK on every view  |  explicit join relationship  |  M = warehouse  |  no LLM in mapping",
        fill=MUTED,
        font=font(12),
    )

    img.save(PNG_OUT)
    print("Wrote", PNG_OUT)


def make_pdf():
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.set_fill_color(18, 32, 48)
    pdf.rect(0, 0, 297, 210, style="F")

    pdf.set_text_color(32, 178, 166)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 8)
    pdf.cell(0, 6, "PBIX -> Looker")
    pdf.set_text_color(240, 245, 250)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_xy(12, 16)
    pdf.cell(0, 9, "Deterministic LookML Mapping Architecture | Phase 2")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(170, 190, 210)
    pdf.set_xy(12, 27)
    pdf.cell(
        0,
        4,
        "No LLM in mapping. Fixed Python rules + looker-skills. Inventory in -> LookML ZIP + developer guide out.",
    )

    def card(x, y, w, h, title, role, body_lines, r, g, b):
        pdf.set_fill_color(28, 48, 68)
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.8)
        pdf.rect(x, y, w, h, style="DF")
        pdf.set_xy(x + 3, y + 3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(w - 6, 5, title)
        pdf.set_xy(x + 3, y + 10)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(240, 245, 250)
        pdf.cell(w - 6, 4, role)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(170, 190, 210)
        yy = y + 17
        for line in body_lines:
            pdf.set_xy(x + 3, yy)
            pdf.cell(w - 6, 3.5, f"- {line}")
            yy += 3.8

    card(
        12,
        36,
        130,
        26,
        "INPUT",
        "ROLE: Phase 1 inventory",
        ["01..05 JSON + OBJECT_COUNTS", "No PBIX re-extract in Phase 2"],
        255,
        196,
        84,
    )
    card(
        150,
        36,
        135,
        26,
        "ORCHESTRATOR",
        "ROLE: Deterministic control",
        ["Run stages 1-5 then Packager 6", "Never invent objects / no LLM"],
        120,
        210,
        140,
    )

    stages = [
        ("1 INGEST", "ROLE: Load", ["Read inventory", "Detect fact", "Skip internals"], 90, 170, 230),
        ("2 EQUIVALENCE", "ROLE: Map", ["PBI->Looker rules", "OBJECT_MAPPING", "Gap flags"], 32, 178, 166),
        ("3 VIEWS", "ROLE: Dims", ["view per table", "primary_key", "date groups"], 255, 120, 90),
        ("4 MODEL/JOINS", "ROLE: Explore", ["model file", "joins+rel", "aliases"], 255, 196, 84),
        ("5 MEASURES", "ROLE: DAX", ["sum/avg/count", "ratios", "TODO complex"], 120, 210, 140),
    ]
    aw = 52
    for i, (t, role, body, r, g, b) in enumerate(stages):
        card(12 + i * (aw + 3), 70, aw, 44, t, role, body, r, g, b)

    card(
        12,
        122,
        273,
        26,
        "6 PACKAGER",
        "ROLE: Guide + ZIP + summary",
        [
            "LOOKER_DEVELOPER_GUIDE.pdf + LOOKML_PROJECT.zip + GAPS.json + PHASE2_SUMMARY.json",
            "UI downloads: LookML ZIP and developer guide PDF",
        ],
        255,
        120,
        90,
    )

    card(
        12,
        154,
        273,
        28,
        "AFTER PHASE 2 (developer / warehouse - not automated)",
        "ROLE: Make LookML production-ready",
        [
            "Set connection + sql_table_name; rebuild Power Query in warehouse; materialize calc columns.",
            "Implement complex DAX TODOs; close HIGH gaps; validate LookML; side-by-side KPI checks vs Power BI.",
        ],
        140,
        160,
        220,
    )

    pdf.set_xy(12, 190)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(170, 190, 210)
    pdf.multi_cell(
        273,
        4,
        "Hard rules: Never invent | Inventory-only input | PK on every view | Explicit join relationship | M=warehouse | No LLM in mapping | No dashboard migration in Phase 2",
    )

    pdf.add_page()
    pdf.set_fill_color(18, 32, 48)
    pdf.rect(0, 0, 297, 210, style="F")
    pdf.set_text_color(240, 245, 250)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(12, 12)
    pdf.cell(0, 8, "What each mapping stage does")

    detail = [
        ("1 Ingest", "Load Phase 1 inventory JSON; detect fact table; exclude LocalDateTable_* / DateTableTemplate_*."),
        ("2 Equivalence", "Apply fixed PBI->Looker object rules; write OBJECT_MAPPING; start HIGH/MEDIUM/LOW gap list."),
        ("3 Views", "Emit one .view.lkml per business table with primary_key, dimensions, dimension_groups."),
        ("4 Model/Joins", "Emit model + explore; map relationships to joins with explicit relationship:; alias inactive/M:M."),
        ("5 Measures", "Classify DAX deterministically (sum/avg/count/ratio vs TODO); preserve original DAX in descriptions."),
        ("6 Packager", "Build developer guide PDF, LOOKML_PROJECT.zip, GAPS.json, PHASE2_SUMMARY.json for UI download."),
    ]
    y = 28
    for title, body in detail:
        pdf.set_fill_color(28, 48, 68)
        pdf.set_draw_color(32, 178, 166)
        pdf.rect(12, y, 273, 22, style="DF")
        pdf.set_xy(16, y + 3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(32, 178, 166)
        pdf.cell(0, 5, title)
        pdf.set_xy(16, y + 10)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(210, 220, 230)
        pdf.multi_cell(265, 4, body)
        y += 25

    pdf.set_xy(12, y + 4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(140, 160, 220)
    pdf.cell(0, 6, "Standards: Looker docs + looker-open-source/looker-skills")
    pdf.set_xy(12, y + 12)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(170, 190, 210)
    pdf.multi_cell(
        273,
        4,
        "lookml-view (PK), lookml-explore (relationship), modeling-guidelines (granular includes). "
        "Phase 2 does not create dashboards (Phase 3) and does not invent warehouse tables.",
    )

    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def make_md():
    MD_OUT.write_text(
        """# Deterministic LookML Mapping Architecture — Phase 2

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf** (filenames kept consistent with Phase 1 links).

## Important

Phase 2 is a **deterministic** Python pipeline — **not** an LLM / agentic system.  
It reads Phase 1 inventory and emits LookML + a Looker developer guide with fixed rules. Same inventory → same LookML.

## Mapping stages

| Stage | Role | Does |
|-------|------|------|
| 1 Ingest | Load inventory | Read 01..05 JSON + counts; detect fact; skip internals |
| 2 Equivalence | Object map | PBI → Looker rules; OBJECT_MAPPING; gap flags |
| 3 Views | Dimensions | One view per table; primary_key; dimension_group dates |
| 4 Model/Joins | Explore graph | Model file; explore; joins with explicit relationship |
| 5 Measures | DAX patterns | SUM/AVG/COUNT/ratios; complex DAX → TODO |
| 6 Packager | Guide + ZIP | LOOKER_DEVELOPER_GUIDE.pdf + LOOKML_PROJECT.zip + GAPS |

Flow: **Phase 1 inventory → Orchestrator → Stages 1–5 → Packager → LookML ZIP + Guide PDF**

## After Phase 2 (developer work)

- Set `connection` and real `sql_table_name` values
- Rebuild Power Query M in warehouse / dbt
- Materialize calculated columns; implement complex DAX TODOs
- Close HIGH gaps; validate LookML; side-by-side KPI checks vs Power BI

## Standards

- [LookML terms and concepts](https://cloud.google.com/looker/docs/lookml-terms-and-concepts)
- [looker-open-source/looker-skills](https://github.com/looker-open-source/looker-skills)
"""
    )
    print("Wrote", MD_OUT)


def main():
    make_png()
    make_pdf()
    make_md()


if __name__ == "__main__":
    main()
