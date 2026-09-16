#!/usr/bin/env python3
"""Phase-1 deterministic extraction architecture diagram (PDF + PNG + MD)."""
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
    d.text((70, 76), "Deterministic Extraction  |  Phase 1", fill=INK, font=font(30, True))
    d.text(
        (70, 118),
        "No LLM in extract  ·  6 specialist Python stages (pbixray)  ·  no invent  ·  data model out",
        fill=MUTED,
        font=font(14),
    )
    d.text(
        (70, 140),
        "To make it agentic: enable NL conversation on top so users ask about the CURRENT uploaded PBIX",
        fill=GOLD,
        font=font(13),
    )

    rounded(d, (40, 190, 520, 310), fill=CARD, outline=GOLD, width=3, radius=16)
    d.text((60, 208), "INPUT", fill=GOLD, font=font(14, True))
    d.text((60, 234), ".pbix semantic model", fill=INK, font=font(22, True))
    d.text((60, 266), "Tables · DAX · M · relationships · TM", fill=MUTED, font=font(13))
    d.text((60, 286), "Tool: pbixray + Python 3.12", fill=MUTED, font=font(13))

    rounded(d, (560, 190, W - 40, 310), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((580, 208), "ORCHESTRATOR (deterministic)", fill=LIME, font=font(14, True))
    d.text((580, 234), "Runs the 6-stage extract pipeline", fill=INK, font=font(22, True))
    d.text((580, 266), "Launch stages 1-5  ->  Merger 6  ->  DATA_MODEL", fill=MUTED, font=font(13))
    d.text((580, 286), "Fixed code paths · never invents objects · no LLM", fill=MUTED, font=font(13))

    d.line((280, 310, 280, 350), fill=MUTED, width=3)
    d.line((1080, 310, 1080, 350), fill=MUTED, width=3)
    d.line((280, 350, 1080, 350), fill=MUTED, width=3)
    d.line((800, 350, 800, 380), fill=MUTED, width=3)
    d.polygon([(790, 380), (810, 380), (800, 395)], fill=TEAL)

    d.text((560, 405), "EXTRACT STAGES 1-5  ·  DETERMINISTIC (same PBIX = same files)", fill=TEAL, font=font(15, True))

    stages = [
        (
            1,
            "Schema",
            "ROLE: Structure",
            ["List every table", "Capture all columns/types", "Include LocalDate* internals", "Flag calculated tables"],
            SKY,
        ),
        (
            2,
            "Relationships",
            "ROLE: Graph / joins",
            ["From/to table + column", "Cardinality (M:1 etc.)", "Cross-filter direction", "Active vs inactive"],
            TEAL,
        ),
        (
            3,
            "DAX",
            "ROLE: Business logic",
            ["All measures (full DAX)", "Calculated columns", "Calculated tables", "Complexity tags"],
            CORAL,
        ),
        (
            4,
            "Power Query M",
            "ROLE: Data prep logic",
            ["Verbatim M per query", "Write 04_m_raw/*.m", "Tag SQL / seeds / unions", "Capture dependencies"],
            GOLD,
        ),
        (
            5,
            "TM Extras",
            "ROLE: Model metadata",
            ["Partitions & hierarchies", "RLS / OLS ([] if none)", "Annotations / formats", "Auto-date details"],
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
    d.text((145, my + 22), "Merger (deterministic)", fill=INK, font=font(24, True))
    d.text((145, my + 52), "ROLE: Combine + summarize", fill=CORAL, font=font(14, True))
    d.text(
        (145, my + 78),
        "Merges stages 1-5  ->  OBJECT_INVENTORY.md  ·  OBJECT_COUNTS.json  ·  object summary",
        fill=MUTED,
        font=font(13),
    )
    d.text(
        (145, my + 98),
        "No COMPLETENESS_GATE  ·  No ACTION_MATRIX  ·  Accuracy over speed",
        fill=MUTED,
        font=font(13),
    )

    oy = my + 145
    rounded(d, (40, oy, 760, oy + 140), fill=CARD, outline=SKY, width=3, radius=16)
    d.text((60, oy + 14), "INVENTORY OUTPUTS", fill=SKY, font=font(14, True))
    outs = [
        "01_tables_columns.json",
        "02_dax_objects.json",
        "03_relationships.json",
        "04_power_query_m.json + 04_m_raw/*.m",
        "05_tmschema_extras.json",
        "OBJECT_INVENTORY.md + OBJECT_COUNTS.json",
    ]
    for i, line in enumerate(outs):
        d.text((60, oy + 42 + i * 15), f"- {line}", fill=MUTED, font=font(12))

    rounded(d, (800, oy, W - 40, oy + 140), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((820, oy + 14), "FINAL DELIVERABLE", fill=LIME, font=font(14, True))
    d.text((820, oy + 48), "DATA_MODEL", fill=INK, font=font(26, True))
    d.text((820, oy + 84), ".md  ·  .pdf  ·  .png", fill=MUTED, font=font(14))
    d.text((820, oy + 108), "ER + relationships · keys · internals", fill=MUTED, font=font(13))

    # Future layer
    fy = oy + 160
    rounded(d, (40, fy, W - 40, fy + 120), fill=CARD, outline=VIOLET, width=3, radius=16)
    d.text(
        (60, fy + 16),
        "HOW TO MAKE THIS AGENTIC (optional layer — not in Phase 1 extract)",
        fill=VIOLET,
        font=font(14, True),
    )
    d.text((60, fy + 44), "Enable natural-language conversation on top of the extract", fill=INK, font=font(18, True))
    d.text(
        (60, fy + 74),
        "After each PBIX upload/extract, inventory is replaced for THAT file only. An NL/LLM agent on top",
        fill=MUTED,
        font=font(13),
    )
    d.text(
        (60, fy + 94),
        "can answer any question about the current PBIX (tables, joins, DAX, M) from inventory — that is the agentic layer.",
        fill=MUTED,
        font=font(13),
    )

    d.text(
        (40, H - 36),
        "Hard rules: never invent  |  full DAX/M  |  empty=[]  |  include internals  |  no warehouse/LookML in Phase 1  |  no LLM in extract",
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
    pdf.cell(0, 9, "Deterministic Extraction Architecture | Phase 1")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(170, 190, 210)
    pdf.set_xy(12, 27)
    pdf.cell(
        0,
        4,
        "No LLM in extract. Six specialist Python stages (pbixray). Optional later: NL Q&A agent on top of inventory.",
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

    card(12, 36, 130, 26, "INPUT", "ROLE: Source", [".pbix semantic model only", "pbixray extraction (no row dumps)"], 255, 196, 84)
    card(
        150,
        36,
        135,
        26,
        "ORCHESTRATOR",
        "ROLE: Deterministic control",
        ["Run stages 1-5 then Merger 6", "Never invent objects / no LLM"],
        120,
        210,
        140,
    )

    stages = [
        ("1 SCHEMA", "ROLE: Structure", ["Every table + column", "Types / calc flags", "LocalDate* internals"], 90, 170, 230),
        ("2 RELATIONSHIPS", "ROLE: Graph", ["From/to keys", "Cardinality", "Cross-filter / active"], 32, 178, 166),
        ("3 DAX", "ROLE: Logic", ["Full measure DAX", "Calc columns", "Calc tables"], 255, 120, 90),
        ("4 POWER QUERY M", "ROLE: Prep", ["Verbatim M", "04_m_raw/*.m", "SQL/seed tags"], 255, 196, 84),
        ("5 TM EXTRAS", "ROLE: Metadata", ["Partitions", "Hierarchies / RLS", "Auto dates"], 120, 210, 140),
    ]
    aw = 52
    for i, (t, role, body, r, g, b) in enumerate(stages):
        card(12 + i * (aw + 3), 70, aw, 44, t, role, body, r, g, b)

    card(
        12,
        122,
        273,
        26,
        "6 MERGER",
        "ROLE: Combine + summarize",
        [
            "OBJECT_INVENTORY.md + OBJECT_COUNTS.json + printed summary counts",
            "Then generate DATA_MODEL.md / .pdf / .png",
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
        "MAKE IT AGENTIC: NL conversation on top (future)",
        "ROLE: Answer questions about the CURRENT PBIX only",
        [
            "After each upload, inventory is replaced for that PBIX. Enable NL/LLM chat over that inventory.",
            "Users can ask any question about the updated model. Extract stays deterministic; Q&A is the agentic layer.",
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
        "Hard rules: Never invent | Preserve full DAX/M | Empty=[] | Capture internals | No LookML/warehouse/sample data | No LLM in extract",
    )

    pdf.add_page()
    pdf.set_fill_color(18, 32, 48)
    pdf.rect(0, 0, 297, 210, style="F")
    pdf.set_text_color(240, 245, 250)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(12, 12)
    pdf.cell(0, 8, "What each extract stage does")

    detail = [
        ("1 Schema", "Deterministic structure extract: tables, columns, types, calc-table flags, internal auto-date tables."),
        ("2 Relationships", "Deterministic join-graph extract: cardinality, cross-filter, active/inactive."),
        ("3 DAX", "Deterministic logic extract: full measure / calc column / calc table expressions (no rewrite)."),
        ("4 Power Query M", "Deterministic prep extract: verbatim M to 04_m_raw + SQL/seed/union tags."),
        ("5 TM Extras", "Deterministic metadata extract: partitions, hierarchies, RLS/OLS, annotations, auto dates."),
        ("6 Merger", "Deterministic merge: OBJECT_INVENTORY.md + OBJECT_COUNTS.json + summary for UI/PDF."),
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
    pdf.cell(0, 6, "Make it agentic: natural-language conversation on top")
    pdf.set_xy(12, y + 12)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(210, 220, 230)
    pdf.multi_cell(
        273,
        4,
        "By enabling natural-language conversation on top of this deterministic extract, the system becomes agentic: "
        "users can ask any question about the PBIX that was just uploaded/updated. The agent reads only the current "
        "inventory (replaced each run). Extract itself never uses an LLM and never invents objects.",
    )

    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def make_md():
    MD_OUT.write_text(
        """# Deterministic Extraction Architecture — Phase 1

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf** (filenames kept for links).

## Important

Phase 1 is a **deterministic** Python + `pbixray` pipeline — **not** an LLM / agentic system.  
The six “stages” are specialist extract modules (fixed code). Same PBIX → same inventory.

## Extract stages

| Stage | Role | Does |
|-------|------|------|
| 1 Schema | Structure | Tables, columns, types, LocalDate* internals, calc tables |
| 2 Relationships | Graph / joins | From/to, cardinality, cross-filter, active |
| 3 DAX | Business logic | Full measures + calc columns/tables DAX |
| 4 Power Query M | Data prep | Verbatim M + `04_m_raw/*.m` + SQL/seed tags |
| 5 TM Extras | Metadata | Partitions, hierarchies, RLS, auto dates |
| 6 Merger | Combine + summarize | `OBJECT_INVENTORY.md` + `OBJECT_COUNTS.json` |

Flow: **PBIX → Orchestrator → Stages 1–5 → Merger → DATA_MODEL**

## Make it agentic (optional)

**By enabling natural-language conversation on top of this extract, the system becomes agentic.**  
Users can ask any question about the **current** PBIX (the one just uploaded — inventory is replaced each run).  

- Extract = deterministic (no LLM, no invent)  
- NL layer = agentic Q&A over that PBIX’s inventory only  
""",
        encoding="utf-8",
    )
    print("Wrote", MD_OUT)


def main():
    make_png()
    make_pdf()
    make_md()


if __name__ == "__main__":
    main()
