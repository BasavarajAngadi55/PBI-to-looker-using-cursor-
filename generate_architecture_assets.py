#!/usr/bin/env python3
"""Generate 3-phase architecture diagram with every agent named + role (parallel Phase 1)."""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "AGENTIC_ARCHITECTURE.pdf"
PNG_OUT = ROOT / "AGENTIC_ARCHITECTURE.png"
MD_OUT = ROOT / "AGENTIC_ARCHITECTURE.md"


def L(s: str) -> str:
    for a, b in {
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u2192": "->", "—": "-", "–": "-", "→": "->", "·": "-",
    }.items():
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, L("PBIX to Looker - Agentic Architecture (all agents named)"), align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            8,
            L(f"Page {self.page_no()}/{{nb}} | github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-"),
            align="C",
        )

    def h1(self, t):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 8, L(t))
        self.ln(1)

    def h2(self, t):
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 60, 110)
        self.multi_cell(0, 6, L(t))
        self.ln(1)

    def body(self, t):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 4.8, L(t))
        self.ln(1)

    def box(self, x, y, w, h, title, lines, fill, border, title_size=7, body_size=5.5):
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.35)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 1.2, y + 1.2)
        self.set_font("Helvetica", "B", title_size)
        self.set_text_color(20, 40, 80)
        self.cell(w - 2.4, 4, L(title)[:55])
        self.set_font("Helvetica", "", body_size)
        self.set_text_color(35, 35, 35)
        ty = y + 5.5
        for line in lines:
            self.set_xy(x + 1.2, ty)
            self.cell(w - 2.4, 3.1, L(line)[:70])
            ty += 3.1

    def arrow_v(self, x, y1, y2):
        self.set_draw_color(70, 70, 70)
        self.set_line_width(0.45)
        self.line(x, y1, x, y2)
        self.line(x, y2, x - 2, y2 - 3)
        self.line(x, y2, x + 2, y2 - 3)


def page1_diagram(pdf: PDF):
    pdf.add_page()  # landscape set by caller
    pdf.h1("Agentic Architecture - Every Agent & Role")
    pdf.body(
        "Phase 1 runs 5 specialist agents in PARALLEL, then Merger. "
        "Phase 2 uses a different agent set for mapping only. "
        "Phase 3 uses implementation subagents. Reports/visuals out of scope."
    )

    left = pdf.l_margin
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    cx = left + usable / 2
    y = pdf.get_y() + 1

    # INPUT
    pdf.box(
        left + usable * 0.2,
        y,
        usable * 0.6,
        12,
        "INPUT",
        ["Human Resources Sample .pbix  |  pbixray  |  never invent objects"],
        (255, 245, 230),
        (180, 100, 40),
        8,
        6,
    )
    pdf.arrow_v(cx, y + 12, y + 17)
    y += 19

    # ORCHESTRATOR
    pdf.box(
        left,
        y,
        usable,
        11,
        "ORCHESTRATOR (Cursor) - coordinates phases; validates outputs before next phase",
        ["Creates folders | launches agents | checks files exist | enforces PASS gates"],
        (230, 245, 235),
        (40, 120, 70),
        7,
        5.5,
    )
    pdf.arrow_v(cx, y + 11, y + 16)
    y += 18

    # PHASE 1 banner
    pdf.box(
        left,
        y,
        usable,
        8,
        "PHASE 1 - INVENTORY  |  5 specialists run in PARALLEL  ->  then Agent 6 Merger",
        [],
        (220, 240, 220),
        (40, 120, 70),
        8,
        5,
    )
    y += 10

    # 5 parallel agents
    gap = 2.2
    aw = (usable - 4 * gap) / 5
    agents1 = [
        ("1. Schema Agent", ["Role: tabular schema", "tables, columns, types", "calc tables, internal", "OUT: 01_tables_columns.json"]),
        ("2. Relationships", ["Role: all joins", "from/to, cardinality", "cross-filter, active", "OUT: 03_relationships.json"]),
        ("3. DAX Agent", ["Role: all DAX logic", "measures (full text)", "calc cols/tables", "OUT: 02_dax_objects.json"]),
        ("4. Power Query M", ["Role: all M code", "SQL/seeds/unions", "04_m_raw/<Table>.m", "OUT: 04_power_query_m.json"]),
        ("5. TM Extras", ["Role: model extras", "partitions, hierarchies", "RLS/OLS, auto dates", "OUT: 05_tmschema_extras.json"]),
    ]
    fills = [
        (232, 240, 254),
        (236, 245, 255),
        (240, 236, 255),
        (255, 240, 245),
        (240, 250, 245),
    ]
    for i, (title, lines) in enumerate(agents1):
        pdf.box(left + i * (aw + gap), y, aw, 22, title, lines, fills[i], (50, 80, 130), 6.5, 5)
    # parallel label
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(40, 100, 60)
    pdf.set_xy(left, y + 22.5)
    pdf.cell(usable, 4, L("^^^^  PARALLEL  ^^^^"))
    pdf.arrow_v(cx, y + 26, y + 31)
    y += 33

    # Merger 6
    pdf.box(
        left,
        y,
        usable,
        16,
        "6. Merger Agent (runs AFTER 1-5 complete)",
        [
            "Role: merge specialist JSON + .m files into authoritative inventory",
            "OUT: OBJECT_INVENTORY.md | ACTION_MATRIX.csv | COMPLETENESS_GATE.json",
            "Gate PASS required before Phase 2  |  Script: inventory/run_phase1_six_agents.py",
        ],
        (255, 248, 220),
        (160, 120, 40),
        7,
        5.5,
    )
    pdf.arrow_v(cx, y + 16, y + 21)
    y += 23

    # PHASE 2
    pdf.box(
        left,
        y,
        usable,
        8,
        "PHASE 2 - MAPPING ASSESSMENT  |  different agents  |  NO LookML / NO SQL generation",
        [],
        (220, 230, 250),
        (40, 80, 140),
        8,
        5,
    )
    y += 10
    gap2 = 2.5
    bw = (usable - 3 * gap2) / 4
    agents2 = [
        ("A. Tables/Columns", ["Role: map tables->views", "map columns->dimensions", "incl. internal tables", "OUT: phase2_agents/01_*.md"]),
        ("B. DAX Mapping", ["Role: map measures", "calc columns/tables", "flag COMPLEX DAX", "OUT: phase2_agents/02_*.md"]),
        ("C. Rel / M / TM", ["Role: joins, Power Query", "hierarchies, RLS, dates", "partitions, annotations", "OUT: phase2_agents/03_*.md"]),
        ("D. Mapping Merger", ["Role: merge A+B+C", "16-section assessment", "PDF for review", "OUT: LOOKML_MAPPING_ASSESSMENT"]),
    ]
    for i, (title, lines) in enumerate(agents2):
        pdf.box(left + i * (bw + gap2), y, bw, 20, title, lines, (232, 240, 254), (40, 80, 140), 6.5, 5)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(40, 80, 140)
    pdf.set_xy(left, y + 20.5)
    pdf.cell(usable, 4, L("A/B/C parallel  ->  D Merger  |  PHASE2_MERGE_GATE PASS"))
    pdf.arrow_v(cx, y + 24, y + 29)
    y += 31

    # PHASE 3
    pdf.box(
        left,
        y,
        usable,
        8,
        "PHASE 3 - IMPLEMENTATION  |  subagents  |  outputs in phase3/",
        [],
        (255, 245, 220),
        (160, 100, 40),
        8,
        5,
    )
    y += 10
    gap3 = 3
    cw = (usable - 2 * gap3) / 3
    agents3 = [
        ("W. Warehouse Gaps", ["Role: only M/DAX gaps", "base tables ASSUMED", "seeds/calc add-ons", "OUT: phase3_agents/01 + warehouse_sql/"]),
        ("L. LookML Builder", ["Role: views, measures", "joins, explore model", "TODO for complex DAX", "OUT: phase3/views + models/"]),
        ("C. Coverage / Docs", ["Role: accountability", "migration summary", "developer guide", "OUT: COVERAGE + guides"]),
    ]
    for i, (title, lines) in enumerate(agents3):
        pdf.box(left + i * (cw + gap3), y, cw, 20, title, lines, (255, 248, 230), (160, 100, 40), 6.5, 5)
    pdf.arrow_v(cx, y + 21, y + 26)
    y += 28

    half = (usable - 3) / 2
    pdf.box(
        left,
        y,
        half,
        14,
        "DONE = accountable objects",
        ["IMPLEMENTED / PARTIAL / TODO / SKIP", "KPI parity = separate validation"],
        (220, 245, 220),
        (40, 130, 60),
        7,
        5.5,
    )
    pdf.box(
        left + half + 3,
        y,
        half,
        14,
        "NOT forced conversion",
        ["Complex DAX stays TODO (SPLY, EmpCount, TO% Norm)", "Never silently drop a PBIX object"],
        (255, 230, 230),
        (160, 50, 50),
        7,
        5.5,
    )


def page2_roles(pdf: PDF):
    pdf.add_page()
    pdf.h2("Phase 1 - six agents (detail)")
    rows = [
        ("1 Schema", "Extract every table/column including LocalDateTable_* / DateTableTemplate_*", "inventory/01_tables_columns.json"),
        ("2 Relationships", "Extract every relationship (cardinality, cross-filter, active)", "inventory/03_relationships.json"),
        ("3 DAX", "Extract all measures, calc columns, calc tables with FULL expressions", "inventory/02_dax_objects.json"),
        ("4 Power Query M", "Extract verbatim M; write one .m file per query", "04_power_query_m.json + 04_m_raw/"),
        ("5 TM Extras", "Partitions, hierarchies, RLS/OLS, annotations, auto dates (empty=[])", "inventory/05_tmschema_extras.json"),
        ("6 Merger", "Merge 1-5; ACTION_MATRIX; COMPLETENESS_GATE PASS/FAIL", "OBJECT_INVENTORY + GATE"),
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(30, 60, 110)
    pdf.set_text_color(255, 255, 255)
    w = [28, 110, 70]
    for i, h in enumerate(["Agent", "Role", "Output"]):
        pdf.cell(w[i], 6, h, border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(30, 30, 30)
    for a, role, out in rows:
        pdf.cell(w[0], 8, L(a), border=1)
        pdf.cell(w[1], 8, L(role)[:70], border=1)
        pdf.cell(w[2], 8, L(out)[:42], border=1)
        pdf.ln()

    pdf.h2("Phase 2 - four agents (detail)")
    rows2 = [
        ("A Tables/Columns", "Map tables->LookML views; columns->dimensions", "phase2_agents/01_*.md"),
        ("B DAX Mapping", "Map measures/calc; mark COMPLEX (SPLY, ALL, MAX period)", "phase2_agents/02_*.md"),
        ("C Rel/M/TM", "Map joins, M destinations, RLS, hierarchies, auto dates", "phase2_agents/03_*.md"),
        ("D Mapping Merger", "Build LOOKML_MAPPING_ASSESSMENT.md + PDF; merge gate", "LOOKML_MAPPING_ASSESSMENT.*"),
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(40, 80, 140)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(["Agent", "Role", "Output"]):
        pdf.cell(w[i], 6, h, border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(30, 30, 30)
    for a, role, out in rows2:
        pdf.cell(w[0], 8, L(a), border=1)
        pdf.cell(w[1], 8, L(role)[:70], border=1)
        pdf.cell(w[2], 8, L(out)[:42], border=1)
        pdf.ln()

    pdf.h2("Phase 3 - three subagents (detail)")
    rows3 = [
        ("W Warehouse Gaps", "Only capture M/DAX gaps; base tables assumed present", "phase3_agents/01 + warehouse_sql/"),
        ("L LookML Builder", "Implement views, measures, joins; TODO complex DAX", "phase3/views + models/"),
        ("C Coverage/Docs", "IMPLEMENTATION_COVERAGE + guides + migration summary", "phase3/* guides"),
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(160, 100, 40)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(["Agent", "Role", "Output"]):
        pdf.cell(w[i], 6, h, border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(30, 30, 30)
    for a, role, out in rows3:
        pdf.cell(w[0], 8, L(a), border=1)
        pdf.cell(w[1], 8, L(role)[:70], border=1)
        pdf.cell(w[2], 8, L(out)[:42], border=1)
        pdf.ln()

    pdf.h2("Flow summary")
    pdf.set_font("Courier", "", 8)
    pdf.set_fill_color(245, 245, 245)
    pdf.multi_cell(
        0,
        4.2,
        L(
            "PBIX\n"
            "  -> Orchestrator\n"
            "       -> Phase1: Agents 1-5 PARALLEL -> Agent 6 Merger -> GATE PASS\n"
            "       -> Phase2: Agents A-C PARALLEL -> Agent D Merger -> MAPPING PASS\n"
            "       -> Phase3: Agents W + L + C -> phase3/ LookML + gap SQL + docs\n"
            "       -> KPI Parity (manual / later) - NOT automatic"
        ),
        fill=True,
    )


def write_md():
    MD_OUT.write_text(
        """# Agentic Architecture — All Agents Named

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png**.

## Orchestrator

Coordinates phases, validates outputs, enforces gates. Does not invent PBIX objects.

---

## Phase 1 — Inventory (6 agents)

**Agents 1–5 run in PARALLEL**, then **Agent 6 Merger**.

| # | Agent | Role | Output |
|---|--------|------|--------|
| 1 | **Schema Agent** | Extract tables, columns, types, calc tables, internal auto-date tables | `inventory/01_tables_columns.json` |
| 2 | **Relationships Agent** | Extract all relationships (cardinality, cross-filter, active) | `inventory/03_relationships.json` |
| 3 | **DAX Agent** | Extract all measures, calculated columns/tables (full expressions) | `inventory/02_dax_objects.json` |
| 4 | **Power Query M Agent** | Extract verbatim M; one `.m` per query | `04_power_query_m.json` + `04_m_raw/` |
| 5 | **TM Extras Agent** | Partitions, hierarchies, RLS/OLS, annotations, auto dates (`[]` if empty) | `inventory/05_tmschema_extras.json` |
| 6 | **Merger Agent** | Merge 1–5; action matrix; completeness gate | `OBJECT_INVENTORY.md`, `ACTION_MATRIX.csv`, `COMPLETENESS_GATE.json` |

**Gate:** Phase 2 starts only if `COMPLETENESS_GATE = PASS`.

Script: `inventory/run_phase1_six_agents.py`

---

## Phase 2 — Mapping (4 agents — different from Phase 1)

**Agents A–C run in PARALLEL**, then **Agent D Merger**.  
**No LookML / no warehouse SQL** in this phase.

| # | Agent | Role | Output |
|---|--------|------|--------|
| A | **Tables/Columns Mapping** | Map tables → views; columns → dimensions (incl. internal) | `phase2_agents/01_tables_columns_mapping.md` |
| B | **DAX Mapping** | Map measures & calc objects; flag COMPLEX DAX | `phase2_agents/02_dax_mapping.md` |
| C | **Rel / M / TM Mapping** | Map joins, Power Query destinations, RLS, hierarchies, auto dates | `phase2_agents/03_rels_m_tm_mapping.md` |
| D | **Mapping Merger** | Build full assessment + PDF; merge gate | `LOOKML_MAPPING_ASSESSMENT.md` / `.pdf` |

**Gate:** `phase2_agents/PHASE2_MERGE_GATE.json = PASS`

---

## Phase 3 — Implementation (3 subagents)

| # | Agent | Role | Output |
|---|--------|------|--------|
| W | **Warehouse Gaps** | Only M/DAX gaps; **base tables assumed present** | `phase3_agents/01_warehouse_gaps.md` + `phase3/warehouse_sql/` |
| L | **LookML Builder** | Views, measures, joins, model; TODO for complex DAX | `phase3/views/`, `phase3/models/` |
| C | **Coverage / Docs** | Accountability matrix + developer/migration guides | `phase3/IMPLEMENTATION_COVERAGE.md`, guides |

Folder: `phase3/` + `phase3_agents/`

---

## Thesis

Capture everything → Map with specialists → Implement with accountability → Validate KPIs later.  
**Never silently drop objects. Never fake complex DAX equivalence.**
""",
        encoding="utf-8",
    )


def render_png():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("skip png")
        return

    W, H = 1800, 2400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        fb = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
        f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        fs = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except Exception:
        fb = f = fs = ImageFont.load_default()

    def box(xy, fill, outline, title, lines, tfont=f):
        d.rounded_rectangle(xy, radius=10, fill=fill, outline=outline, width=2)
        x1, y1, x2, y2 = xy
        d.text((x1 + 10, y1 + 8), title, fill=(20, 40, 80), font=tfont)
        ty = y1 + 34
        for line in lines:
            d.text((x1 + 10, ty), line, fill=(40, 40, 40), font=fs)
            ty += 16

    def arrow(x, y1, y2):
        d.line((x, y1, x, y2), fill=(70, 70, 70), width=3)
        d.polygon([(x, y2), (x - 7, y2 - 11), (x + 7, y2 - 11)], fill=(70, 70, 70))

    m = 50
    d.text((m, 25), "PBIX -> Looker: Agentic Architecture (all agents)", fill=(20, 40, 80), font=fb)
    d.text((m, 58), "Phase1: 6 agents (1-5 parallel) | Phase2: 4 mapping agents | Phase3: 3 implementation subagents", fill=(80, 80, 80), font=fs)

    y = 95
    box((500, y, 1300, y + 70), (255, 245, 230), (180, 100, 40), "INPUT: .pbix", ["Semantic model only | pbixray | never invent"])
    arrow(900, y + 70, y + 95)
    y += 105

    box((m, y, W - m, y + 70), (230, 245, 235), (40, 120, 70), "ORCHESTRATOR", ["Launch agents | validate files | enforce PASS gates"])
    arrow(900, y + 70, y + 95)
    y += 105

    # Phase 1
    d.text((m, y), "PHASE 1 INVENTORY — Agents 1-5 PARALLEL, then Agent 6", fill=(40, 100, 60), font=f)
    y += 28
    aw = (W - 2 * m - 40) // 5
    p1 = [
        ("1 Schema", ["tables/cols", "internal dates", "01_tables.json"]),
        ("2 Relationships", ["M:1 joins", "cardinality", "03_rel.json"]),
        ("3 DAX", ["measures", "calc cols", "02_dax.json"]),
        ("4 Power Query M", ["full M", "04_m_raw/", "04_pq.json"]),
        ("5 TM Extras", ["RLS/hier", "partitions", "05_tm.json"]),
    ]
    for i, (t, lines) in enumerate(p1):
        x = m + i * (aw + 8)
        box((x, y, x + aw, y + 110), (232, 240, 254), (50, 80, 130), t, lines, fs)
    d.text((m, y + 115), "^^^^^ PARALLEL ^^^^^", fill=(40, 120, 70), font=f)
    arrow(900, y + 135, y + 155)
    y += 165
    box((m, y, W - m, y + 90), (255, 248, 220), (160, 120, 40), "6 Merger Agent (AFTER 1-5)", [
        "OBJECT_INVENTORY.md | ACTION_MATRIX.csv | COMPLETENESS_GATE.json",
        "PASS required before Phase 2",
    ])
    arrow(900, y + 90, y + 115)
    y += 125

    # Phase 2
    d.text((m, y), "PHASE 2 MAPPING — Agents A-C PARALLEL, then Agent D (no LookML)", fill=(40, 80, 140), font=f)
    y += 28
    bw = (W - 2 * m - 30) // 4
    p2 = [
        ("A Tables/Columns", ["views mapping", "dimensions", "phase2_agents/01"]),
        ("B DAX Mapping", ["measures", "COMPLEX flags", "phase2_agents/02"]),
        ("C Rel/M/TM", ["joins + M", "RLS/dates", "phase2_agents/03"]),
        ("D Mapping Merger", ["full assessment", "PDF review", "LOOKML_MAPPING_*"]),
    ]
    for i, (t, lines) in enumerate(p2):
        x = m + i * (bw + 8)
        box((x, y, x + bw, y + 110), (232, 240, 254), (40, 80, 140), t, lines, fs)
    arrow(900, y + 120, y + 140)
    y += 150

    # Phase 3
    d.text((m, y), "PHASE 3 IMPLEMENTATION — subagents (outputs in phase3/)", fill=(160, 100, 40), font=f)
    y += 28
    cw = (W - 2 * m - 20) // 3
    p3 = [
        ("W Warehouse Gaps", ["base tables assumed", "M/DAX gaps only", "warehouse_sql templates"]),
        ("L LookML Builder", ["views + measures", "joins + model", "TODO complex DAX"]),
        ("C Coverage/Docs", ["accountability", "dev guide", "migration summary"]),
    ]
    for i, (t, lines) in enumerate(p3):
        x = m + i * (cw + 8)
        box((x, y, x + cw, y + 110), (255, 248, 230), (160, 100, 40), t, lines, fs)
    arrow(900, y + 120, y + 140)
    y += 150

    mid = W // 2
    box((m, y, mid - 10, y + 90), (220, 245, 220), (40, 130, 60), "Accountable", ["Every object statused", "KPI parity later"])
    box((mid + 10, y, W - m, y + 90), (255, 230, 230), (160, 50, 50), "Not fake-complete", ["SPLY/EmpCount/TO%Norm = TODO", "Never drop PBIX objects"])

    d.text((m, H - 40), "github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-", fill=(80, 80, 80), font=fs)
    img.save(PNG_OUT)
    print("Wrote", PNG_OUT)


def main():
    write_md()
    pdf = PDF(orientation="L", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(10, 10, 10)
    page1_diagram(pdf)
    page2_roles(pdf)
    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)
    render_png()


if __name__ == "__main__":
    main()
