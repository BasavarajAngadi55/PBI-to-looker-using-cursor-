#!/usr/bin/env python3
"""Phase-3 deterministic dashboard migration architecture (PDF + PNG + MD).

Look-and-feel matches Phase 1 / Phase 2 architecture diagrams.
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
    d.text((70, 76), "Deterministic Dashboard Migration  |  Phase 3", fill=INK, font=font(28, True))
    d.text(
        (70, 118),
        "No LLM  ·  Report/Layout extract  ·  visual mapping rules  ·  LookML dashboards  ·  ~70% target",
        fill=MUTED,
        font=font(14),
    )
    d.text(
        (70, 140),
        "Depends on Phase 1 inventory + Phase 2 explores/views  ·  pixel-perfect is NOT claimed",
        fill=GOLD,
        font=font(13),
    )

    rounded(d, (40, 190, 520, 310), fill=CARD, outline=GOLD, width=3, radius=16)
    d.text((60, 208), "INPUT", fill=GOLD, font=font(14, True))
    d.text((60, 234), "PBIX Report/Layout + Phase 2", fill=INK, font=font(20, True))
    d.text((60, 266), "Pages · visuals · fields · slicers", fill=MUTED, font=font(13))
    d.text((60, 286), "Model/explore from Phase 2 LookML", fill=MUTED, font=font(13))

    rounded(d, (560, 190, W - 40, 310), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((580, 208), "ORCHESTRATOR (deterministic)", fill=LIME, font=font(14, True))
    d.text((580, 234), "Runs the 6-stage dashboard pipeline", fill=INK, font=font(20, True))
    d.text((580, 266), "Extract -> Map -> Bind -> Emit -> Cover -> Package", fill=MUTED, font=font(13))
    d.text((580, 286), "Fixed rules · never invent visuals · no LLM", fill=MUTED, font=font(13))

    d.line((280, 310, 280, 350), fill=MUTED, width=3)
    d.line((1080, 310, 1080, 350), fill=MUTED, width=3)
    d.line((280, 350, 1080, 350), fill=MUTED, width=3)
    d.line((800, 350, 800, 380), fill=MUTED, width=3)
    d.polygon([(790, 380), (810, 380), (800, 395)], fill=TEAL)

    d.text((460, 405), "DASHBOARD STAGES 1-5  ·  DETERMINISTIC (same PBIX = same dashboards)", fill=TEAL, font=font(14, True))

    stages = [
        (1, "Extract", "ROLE: Report layout", ["Unzip Report/Layout", "Pages + visuals", "prototypeQuery fields", "Positions x/y/w/h"], SKY),
        (2, "Equivalence", "ROLE: Visual map", ["card->single_value", "charts->looker_*", "slicer->filter", "shape skip / gaps"], TEAL),
        (3, "Bind fields", "ROLE: Explore fields", ["Table.Col -> view.field", "Measures on fact", "Flag missing fields", "Phase 2 names"], CORAL),
        (4, "Emit LookML", "ROLE: Dashboards", ["One .dashboard.lookml/page", "newspaper layout", "filters + listen", "text gap tiles"], GOLD),
        (5, "Coverage", "ROLE: Score", ["Weighted completion", "Target >= 70%", "PAGE_COMPARISON", "COVERAGE.json"], LIME),
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
    d.text((145, my + 52), "ROLE: Guide + ZIP + architecture", fill=CORAL, font=font(14, True))
    d.text(
        (145, my + 78),
        "DASHBOARD_DEVELOPER_GUIDE.pdf  ·  LOOKML_DASHBOARDS.zip  ·  comparison + coverage",
        fill=MUTED,
        font=font(13),
    )
    d.text((145, my + 98), "UI download hooks  ·  honest gap reporting  ·  no LLM", fill=MUTED, font=font(13))

    oy = my + 145
    rounded(d, (40, oy, 760, oy + 140), fill=CARD, outline=SKY, width=3, radius=16)
    d.text((60, oy + 14), "OUTPUTS", fill=SKY, font=font(14, True))
    for i, line in enumerate(
        [
            "inventory/01_report_pages.json",
            "inventory/02_visuals.json",
            "inventory/03_dashboard_mapping.json",
            "inventory/COVERAGE.json",
            "lookml_dashboards/dashboards/*.dashboard.lookml",
            "comparison/PAGE_COMPARISON.md",
        ]
    ):
        d.text((60, oy + 42 + i * 15), f"- {line}", fill=MUTED, font=font(12))

    rounded(d, (800, oy, W - 40, oy + 140), fill=CARD, outline=LIME, width=3, radius=16)
    d.text((820, oy + 14), "FINAL DELIVERABLES", fill=LIME, font=font(14, True))
    d.text((820, oy + 48), "DASHBOARD ZIP", fill=INK, font=font(22, True))
    d.text((820, oy + 80), "+ Developer Guide PDF", fill=INK, font=font(18, True))
    d.text((820, oy + 108), "Best-effort Looker parity (~70%)", fill=MUTED, font=font(13))

    fy = oy + 160
    rounded(d, (40, fy, W - 40, fy + 120), fill=CARD, outline=VIOLET, width=3, radius=16)
    d.text((60, fy + 16), "NOT AUTOMATED / KNOWN GAPS", fill=VIOLET, font=font(14, True))
    d.text((60, fy + 44), "Pixel layout, bookmarks, drillthrough, custom visuals, themes", fill=INK, font=font(18, True))
    d.text(
        (60, fy + 74),
        "Combo/treemap/map/image/button are partial or gap - listed in comparison + gap tiles",
        fill=MUTED,
        font=font(13),
    )
    d.text(
        (60, fy + 94),
        "Optional later: NL agentic Q&A over inventory - extract stays deterministic",
        fill=MUTED,
        font=font(13),
    )

    d.text(
        (40, H - 36),
        "Hard rules: never invent visuals  |  inventory-backed fields only  |  Phase 2 explore required  |  no LLM in Phase 3",
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
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(12, 16)
    pdf.cell(0, 9, "Deterministic Dashboard Migration Architecture | Phase 3")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(170, 190, 210)
    pdf.set_xy(12, 27)
    pdf.cell(0, 4, "No LLM. Report/Layout extract + fixed visual mapping. LookML dashboards. Honest ~70% coverage target.")

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

    card(12, 36, 130, 26, "INPUT", "ROLE: Report + Phase 2", ["PBIX Report/Layout JSON", "Phase 2 model/explore"], 255, 196, 84)
    card(150, 36, 135, 26, "ORCHESTRATOR", "ROLE: Deterministic", ["6 stages then package", "Never invent / no LLM"], 120, 210, 140)
    stages = [
        ("1 EXTRACT", "ROLE: Layout", ["Pages/visuals", "Fields", "Positions"], 90, 170, 230),
        ("2 EQUIVALENCE", "ROLE: Map", ["PBI->Looker type", "Skip shapes", "Gap flags"], 32, 178, 166),
        ("3 BIND", "ROLE: Fields", ["view.field refs", "Measures", "Missing=gap"], 255, 120, 90),
        ("4 EMIT", "ROLE: LookML", ["dashboard.lookml", "filters", "listen"], 255, 196, 84),
        ("5 COVER", "ROLE: Score", ["Weighted %", "Comparison", "COVERAGE"], 120, 210, 140),
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
        "ROLE: Guide + ZIP",
        ["DASHBOARD_DEVELOPER_GUIDE.pdf + LOOKML_DASHBOARDS.zip + architecture assets", "UI downloads for ZIP and guide"],
        255,
        120,
        90,
    )
    card(
        12,
        154,
        273,
        28,
        "GAPS (expected)",
        "ROLE: Honest deficiency reporting",
        [
            "Bookmarks, drillthrough, custom visuals, themes, exact pixel layout not automated.",
            "Partial: donut/combo/treemap/map/kpi trend. Generate what we can; list the rest.",
        ],
        140,
        160,
        220,
    )
    pdf.set_xy(12, 190)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(170, 190, 210)
    pdf.multi_cell(273, 4, "Hard rules: Never invent | Field refs from inventory only | Requires Phase 2 explore | No LLM in Phase 3")
    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def make_md():
    MD_OUT.write_text(
        """# Deterministic Dashboard Migration Architecture — Phase 3

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf**.

## Important

Phase 3 is **deterministic** Python — not LLM/agentic.  
It reads PBIX `Report/Layout` + Phase 2 model/explore and emits LookML dashboards with coverage scoring.

## Stages

| Stage | Role | Does |
|-------|------|------|
| 1 Extract | Report layout | Pages, visuals, fields, positions from PBIX |
| 2 Equivalence | Visual map | Fixed PBI visual → Looker element rules |
| 3 Bind | Fields | Map to Phase 2 `view.field` / measures |
| 4 Emit | LookML | One `.dashboard.lookml` per page |
| 5 Coverage | Score | Weighted completion vs 70% target |
| 6 Packager | Deliver | Guide PDF + ZIP + comparison |

Flow: **PBIX Layout → Orchestrator → Stages 1–5 → Packager → LookML dashboards**

## Optional agentic later

NL Q&A over Phase 3 inventory/comparison — extract/mapping stays deterministic.
"""
    )
    print("Wrote", MD_OUT)


def main():
    make_png()
    make_pdf()
    make_md()


if __name__ == "__main__":
    main()
