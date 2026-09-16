#!/usr/bin/env python3
"""Generate a thorough Looker Developer Guide (MD + PDF) for Phase 2.

Audience: Looker developers implementing the migrated semantic model.
Content: step-by-step build instructions, what to check, gaps, best practices.
Driven deterministically from Phase 1 inventory + Phase 2 OBJECT_MAPPING.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from fpdf import FPDF

from lib.mapping import OBJECT_EQUIVALENCE, is_internal_table, lookml_field_type
from lib.naming import lookml_view_name, snake_case

ROOT = Path(__file__).resolve().parent
PHASE1_INV = ROOT.parent / "phase1" / "inventory"
MD_OUT = ROOT / "LOOKER_DEVELOPER_GUIDE.md"
PDF_OUT = ROOT / "LOOKER_DEVELOPER_GUIDE.pdf"
MAPPING_JSON = ROOT / "OBJECT_MAPPING.json"
SUMMARY_JSON = ROOT / "PHASE2_SUMMARY.json"
M_REC_JSON = ROOT / "lookml" / "m_migration" / "M_QUERY_RECOMMENDATIONS.json"


def latin1(s: str) -> str:
    return (
        str(s)
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2192", "->")
        .replace("\u2022", "*")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_inventory(inv: Path) -> dict:
    def j(name: str) -> dict:
        p = inv / name
        return json.loads(p.read_text()) if p.exists() else {}

    return {
        "a1": j("01_tables_columns.json"),
        "a2": j("02_dax_objects.json"),
        "a3": j("03_relationships.json"),
        "a4": j("04_power_query_m.json"),
        "a5": j("05_tmschema_extras.json"),
        "counts": j("OBJECT_COUNTS.json"),
    }


def analyze(inv: dict, mapping: dict, summary: dict) -> dict:
    """Build structured guide content + gap list from inventory."""
    a1, a2, a3, a4, a5 = inv["a1"], inv["a2"], inv["a3"], inv["a4"], inv["a5"]
    counts = inv.get("counts") or {}
    src = Path(
        mapping.get("source_pbix")
        or counts.get("source_pbix")
        or a1.get("source_pbix")
        or "PBIX"
    ).name
    model = mapping.get("model_name") or summary.get("model_name") or snake_case(Path(src).stem)
    fact = summary.get("fact_table")

    biz_tables = [
        t
        for t in (a1.get("tables") or [])
        if t.get("table_name") and not is_internal_table(t["table_name"]) and t.get("is_business", True)
    ]
    cols_by: dict[str, list] = defaultdict(list)
    for c in a1.get("columns") or []:
        if not is_internal_table(c.get("table_name") or ""):
            cols_by[c["table_name"]].append(c)

    calc_biz = [
        c
        for c in (a2.get("calculated_columns") or [])
        if not is_internal_table(c.get("table") or c.get("table_name") or "")
    ]
    measures = a2.get("measures") or []
    rels = a3.get("relationships") or []
    queries = a4.get("queries") or []
    rls = a5.get("rls") or []
    hierarchies = [
        h
        for h in (a5.get("hierarchies") or [])
        if not is_internal_table(h.get("table") or "")
    ]

    gen = mapping.get("generated_objects") or []
    measure_plans = [g for g in gen if g.get("kind") == "measure"]
    todo_measures = [g for g in measure_plans if g.get("status") == "todo"]
    inactive_joins = [g for g in gen if g.get("status") == "inactive_alias"]

    gaps: list[dict] = []

    # Placeholder connection / dataset
    gaps.append(
        {
            "severity": "HIGH",
            "area": "Connection & warehouse",
            "gap": "LookML still uses placeholders YOUR_LOOKER_CONNECTION and YOUR_PROJECT.YOUR_DATASET.",
            "action": "Set the real Looker connection name and point every sql_table_name at existing warehouse tables before validating.",
        }
    )

    # Power Query -> warehouse / Looker pattern
    if queries:
        m_rec = load_json(M_REC_JSON)
        pattern_counts = m_rec.get("pattern_counts") or {}
        gaps.append(
            {
                "severity": "HIGH",
                "area": "Power Query / ETL",
                "gap": (
                    f"{len(queries)} Power Query queries need warehouse/Looker equivalents. "
                    f"Pattern mix: {pattern_counts or 'see m_migration stubs'}."
                ),
                "action": (
                    "Open LOOKML_PROJECT.zip → lookml/m_migration/. "
                    "For each query follow M_QUERY_RECOMMENDATIONS.md, implement sql/<query>.sql "
                    "in the warehouse, then update the straight LookML view sql_table_name. "
                    "Use LookML SDT only when the recommendation allows a temporary bridge."
                ),
            }
        )

    # No measures
    if not measures:
        gaps.append(
            {
                "severity": "MEDIUM",
                "area": "Measures",
                "gap": "This PBIX has 0 DAX measures. Generated views only include a default count measure.",
                "action": (
                    "Confirm with stakeholders which KPIs Power BI used (often implicit aggregates on columns). "
                    "Add explicit LookML measures (sum/average/count_distinct) for numeric facts users expect."
                ),
            }
        )
    elif todo_measures:
        gaps.append(
            {
                "severity": "HIGH",
                "area": "Complex DAX",
                "gap": f"{len(todo_measures)} of {len(measures)} measures are TODO stubs (CALCULATE/time-intel/iterators).",
                "action": "Implement each TODO using LookML filters, period-over-period patterns, or warehouse logic. Keep original DAX in the field description until KPI parity passes.",
            }
        )

    # Calculated columns
    if calc_biz:
        gaps.append(
            {
                "severity": "HIGH",
                "area": "Calculated columns",
                "gap": f"{len(calc_biz)} business calculated columns must be materialized (prefer warehouse), not left as DAX.",
                "action": "Create warehouse columns for: "
                + "; ".join(
                    f"{c.get('table')}.{c.get('column_name')}" for c in calc_biz[:20]
                )
                + (" ..." if len(calc_biz) > 20 else ""),
            }
        )

    # Inactive / many-to-many relationships
    for r in rels:
        card = (r.get("cardinality") or "").upper()
        active = r.get("active", True)
        label = f"{r.get('from_table')}[{r.get('from_column')}] -> {r.get('to_table')}[{r.get('to_column')}]"
        if not active:
            gaps.append(
                {
                    "severity": "MEDIUM",
                    "area": "Inactive relationship",
                    "gap": f"Inactive in Power BI: {label} ({card}).",
                    "action": "Looker has no inactive join. Keep as a separate aliased join (from:) and only expose when a measure needs USERELATIONSHIP-style behavior. Hide fields until needed.",
                }
            )
        if "M:M" in card.replace(" ", "") or card in {"MANY:MANY", "MANYTOMANY"}:
            gaps.append(
                {
                    "severity": "HIGH",
                    "area": "Many-to-many join",
                    "gap": f"M:M relationship: {label}. Risk of fan-out and wrong aggregates.",
                    "action": "Prefer a bridge table in the warehouse, or redesign to M:1. If kept, set relationship: many_to_many and verify symmetric aggregates / primary keys.",
                }
            )

    # RLS
    if rls:
        gaps.append(
            {
                "severity": "HIGH",
                "area": "Row-level security",
                "gap": f"{len(rls)} RLS role(s) in PBIX are not auto-translated to Looker access_filter.",
                "action": "Map each role to Looker user attributes + access_filter / access_grant before production.",
            }
        )
    else:
        gaps.append(
            {
                "severity": "LOW",
                "area": "Row-level security",
                "gap": "No RLS roles in this PBIX inventory.",
                "action": "Still confirm with security owners whether Looker needs access_filter by region/org.",
            }
        )

    # Internal auto-date
    internal = [t["table_name"] for t in (a1.get("tables") or []) if is_internal_table(t.get("table_name") or "")]
    if internal:
        gaps.append(
            {
                "severity": "LOW",
                "area": "Auto date tables",
                "gap": f"{len(internal)} LocalDateTable_/DateTableTemplate_ tables skipped (correct).",
                "action": "Use business date columns with dimension_group timeframes. Do not migrate auto-date tables.",
            }
        )

    # Naming quality
    ugly = [t["table_name"] for t in biz_tables if " " in t["table_name"] or t["table_name"].lower().startswith("sheet")]
    if ugly:
        gaps.append(
            {
                "severity": "MEDIUM",
                "area": "Naming",
                "gap": "Source table names are Excel-like / spaced: " + ", ".join(ugly),
                "action": "Keep labels user-friendly; prefer warehouse rename to clear names (e.g. restaurants, countries). Update sql_table_name accordingly.",
            }
        )

    # Duplicate grain risk (Sheet1 vs cuisines copy)
    names_l = [t["table_name"].lower() for t in biz_tables]
    if any("cuisine" in n for n in names_l) and any("sheet1" in n for n in names_l):
        gaps.append(
            {
                "severity": "MEDIUM",
                "area": "Model grain",
                "gap": "Both Sheet1 and cuisines copy exist — possible duplicate restaurant grain.",
                "action": "Confirm which table is the true fact. Prefer one explore base. Document why the second table exists (filter/bridge/copy).",
            }
        )

    view_build = []
    for t in biz_tables:
        tname = t["table_name"]
        cols = cols_by.get(tname, [])
        pk_guess = next(
            (c["column_name"] for c in cols if str(c["column_name"]).endswith("PK") or str(c["column_name"]).endswith("ID")),
            cols[0]["column_name"] if cols else None,
        )
        date_cols = [
            c["column_name"]
            for c in cols
            if lookml_field_type(c.get("data_type"), c.get("pandas_dtype")) == "time"
        ]
        view_build.append(
            {
                "pbi_table": tname,
                "lookml_view": lookml_view_name(tname),
                "file": f"views/{lookml_view_name(tname)}.view.lkml",
                "columns": len(cols),
                "pk_guess": pk_guess,
                "date_columns": date_cols,
                "is_calculated_table": bool(t.get("is_calculated_table")),
                "table_type": t.get("table_type"),
            }
        )

    join_build = []
    for r in rels:
        join_build.append(
            {
                "from": f"{r.get('from_table')}[{r.get('from_column')}]",
                "to": f"{r.get('to_table')}[{r.get('to_column')}]",
                "cardinality": r.get("cardinality"),
                "cross_filter": r.get("cross_filter"),
                "active": r.get("active", True),
                "looker": f"join {lookml_view_name(r.get('to_table') or '')} relationship from PBI {r.get('cardinality')}",
            }
        )

    return {
        "source": src,
        "model": model,
        "fact": fact,
        "counts": counts.get("counts") or counts,
        "biz_tables": biz_tables,
        "view_build": view_build,
        "join_build": join_build,
        "measures": measures,
        "measure_plans": measure_plans,
        "todo_measures": todo_measures,
        "calc_biz": calc_biz,
        "queries": queries,
        "rls": rls,
        "hierarchies": hierarchies,
        "gaps": gaps,
        "gen": gen,
        "inactive_joins": inactive_joins,
        "m_recommendations": load_json(M_REC_JSON),
    }


def soft_wrap(text: str, width: int = 92) -> str:
    """Wrap long lines so FPDF never clips mid-token at the page edge."""
    out = []
    for para in str(text).splitlines() or [""]:
        if not para.strip():
            out.append("")
            continue
        words = para.replace("\t", " ").split(" ")
        line = ""
        for w in words:
            piece = w
            while len(piece) > width:
                out.append(piece[:width])
                piece = piece[width:]
            trial = (line + " " + piece).strip() if line else piece
            if len(trial) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = piece
        if line:
            out.append(line)
    return "\n".join(out)


def build_markdown(ctx: dict) -> str:
    c = ctx
    lines: list[str] = [
        "# Looker Developer Guide — Power BI → LookML (Phase 2)",
        "",
        f"**Source PBIX:** `{c['source']}`  ",
        f"**LookML model:** `lookml/models/{c['model']}.model.lkml`  ",
        f"**Primary explore (fact):** `{c['fact']}`  ",
        "**Audience:** Looker developers implementing and validating this migration.",
        "",
        "This is a **build playbook**: full instructions, checks, suggestions, examples, and gaps.",
        "",
        "References: [LookML concepts](https://cloud.google.com/looker/docs/lookml-terms-and-concepts) · "
        "[looker-skills](https://github.com/looker-open-source/looker-skills)",
        "",
        "---",
        "",
        "## 1. How to use this guide",
        "",
        "1. Read **Best practices** (mandatory).",
        "2. Complete **Prerequisites**.",
        "3. Study **Object equivalence** — each object has What / Build / Check / Suggestions / Example.",
        "4. Execute **Build plan** for THIS PBIX.",
        "5. Close **Gaps** (HIGH first).",
        "6. Sign off with **Validation & acceptance**.",
        "",
        "## 2. Best practices (mandatory)",
        "",
        "| Rule | Why |",
        "|---|---|",
        "| Every view has `primary_key: yes` | Symmetric aggregates; prevents fan-out |",
        "| Always set join `relationship:` | Correct SQL / aggregate behavior |",
        "| Prefer `${dimension}` in measure sql | Single source of truth |",
        "| Granular `include:` paths | Faster compile, fewer collisions |",
        "| Explore `label` + `description` | Discoverability |",
        "| Rebuild Power Query in warehouse | LookML is semantic, not ETL |",
        "| No KPI claims without side-by-side tests | Complex DAX is not auto-translated |",
        "| Review inactive / M:M joins | Avoid silent wrong numbers |",
        "",
        "## 3. Prerequisites checklist",
        "",
        "- [ ] Looker project + Git branch ready",
        "- [ ] Database connection created in Looker Admin",
        "- [ ] Warehouse tables exist (or tickets filed)",
        "- [ ] Phase 1 inventory matches this PBIX",
        "- [ ] `LOOKML_PROJECT.zip` imported",
        "- [ ] SQL dialect known (BigQuery vs Snowflake)",
        "",
        "## 4. Object equivalence — full developer instructions",
        "",
        "For each Power BI object: follow **How to build**, verify **What to check**, apply **Suggestions**.",
        "",
    ]

    for i, row in enumerate(OBJECT_EQUIVALENCE, 1):
        lines += [
            f"### 4.{i} {row['power_bi']} → **{row['looker']}**",
            "",
            f"**What it means:** {row.get('summary') or row['how_to_create']}",
            "",
            "**How to build (step-by-step):**",
            "",
        ]
        for n, step in enumerate(row.get("build_steps") or [row["how_to_create"]], 1):
            lines.append(f"{n}. {step}")
        lines += ["", "**What to check:**", ""]
        for chk in row.get("checks") or [
            "Present in Phase 1 inventory",
            "LookML validator clean",
            "Explore sample matches expected grain",
        ]:
            lines.append(f"- [ ] {chk}")
        lines += ["", "**Suggestions / best practice:**", ""]
        for s in row.get("suggestions") or []:
            lines.append(f"- {s}")
        if row.get("example"):
            lines += ["", "**Example:**", "", "```lookml", row["example"], "```", ""]
        if row.get("refs"):
            lines.append("Docs: " + " · ".join(row["refs"]))
            lines.append("")

    lines += [
        "## 5. Build plan (this PBIX)",
        "",
        "### Step A — Import LookML",
        "1. Unzip `LOOKML_PROJECT.zip`.",
        "2. Place `manifest.lkml`, `models/`, `views/` in the Looker project.",
        "3. Set `connection:` in the model file.",
        "",
        "### Step B — Point views at warehouse",
        "",
        "| PBI table | LookML view | File | Cols | PK guess | Date cols |",
        "|---|---|---|---|---|---|",
    ]
    for v in c["view_build"]:
        dates = ", ".join(v["date_columns"][:4]) or "-"
        lines.append(
            f"| `{v['pbi_table']}` | `{v['lookml_view']}` | `{v['file']}` | {v['columns']} | `{v['pk_guess']}` | {dates} |"
        )

    lines += [
        "",
        "### Step C — Explores and joins",
        f"Primary explore fact: **`{c['fact']}`**.",
        "",
        "| From (FK) | To (PK) | Card | Active | Looker action |",
        "|---|---|---|---|---|",
    ]
    for j in c["join_build"]:
        lines.append(
            f"| `{j['from']}` | `{j['to']}` | {j['cardinality']} | {j['active']} | {j['looker']} |"
        )

    lines += ["", "### Step D — Measures", ""]
    if not c["measures"]:
        lines.append(
            "**GAP:** 0 DAX measures. Add explicit LookML measures for KPIs users expect "
            "(count, count_distinct on keys, averages on numeric columns)."
        )
    else:
        lines.append(
            f"Mapped {len(c['measure_plans'])} measures; **{len(c['todo_measures'])} TODO**."
        )
        lines += ["", "| Power BI measure | Strategy / status |", "|---|---|"]
        for m in c["measure_plans"]:
            lines.append(f"| `{m.get('power_bi')}` | {m.get('strategy')} / {m.get('status')} |")

    lines += ["", "### Step E — Calculated columns (warehouse)", ""]
    if not c["calc_biz"]:
        lines.append("No business calculated columns.")
    else:
        lines += ["| Table | Column | DAX (truncated) | Action |", "|---|---|---|---|"]
        for cc in c["calc_biz"]:
            expr = (cc.get("expression") or "").replace("\n", " ")[:90]
            lines.append(
                f"| `{cc.get('table')}` | `{cc.get('column_name')}` | `{expr}` | Materialize; expose as dimension |"
            )

    lines += ["", "### Step F — Power Query M (recommended Looker / warehouse equivalent)", ""]
    lines += [
        "Decision order (best practice):",
        "",
        "1. **Warehouse table/view + straight LookML view** (`sql_table_name`) — preferred",
        "2. **LookML SQL derived table (SDT)** — temporary bridge for light SQL only",
        "3. **Native derived table (NDT)** — rarely a Power Query replacement",
        "4. Never encode heavy M merges/appends only in LookML",
        "",
        "Stubs are inside the ZIP: `lookml/m_migration/` "
        "(`M_QUERY_RECOMMENDATIONS.md`, `sql/*.sql`, `lookml_stubs/*.lkml`).",
        "",
    ]
    mrec = c.get("m_recommendations") or {}
    rec_rows = mrec.get("recommendations") or []
    if rec_rows:
        lines += [
            "| M query | Recommended pattern | Looker object | Build in |",
            "|---|---|---|---|",
        ]
        for r in rec_rows:
            lines.append(
                f"| `{r.get('query_name')}` | `{r.get('recommended_pattern')}` | "
                f"{r.get('looker_object')} | `{r.get('build_in')}` |"
            )
        lines.append("")
        for r in rec_rows:
            lines += [
                f"#### `{r.get('query_name')}`",
                "",
                f"**Why:** {r.get('rationale')}",
                "",
                "**Build steps:**",
                "",
            ]
            for i, s in enumerate(r.get("steps") or [], 1):
                lines.append(f"{i}. {s}")
            lines += [
                "",
                f"- SQL stub: `m_migration/sql/{snake_case(r.get('query_name'))}.sql`",
                f"- LookML stub: `m_migration/lookml_stubs/{snake_case(r.get('query_name'))}_recommended.lkml`",
                "",
            ]
    elif c["queries"]:
        for q in c["queries"]:
            qn = q.get("query_name") or q.get("name")
            lines.append(
                f"- `{qn}` — source_type=`{q.get('source_type')}` → run generate_m_migration.py for stubs"
            )
    else:
        lines.append("- No queries listed.")

    lines += ["", "## 6. Gaps (must resolve)", ""]
    by_sev = {"HIGH": [], "MEDIUM": [], "LOW": []}
    for g in c["gaps"]:
        by_sev.get(g["severity"], by_sev["LOW"]).append(g)
    for sev in ("HIGH", "MEDIUM", "LOW"):
        lines += [f"### Severity: {sev}", ""]
        if not by_sev[sev]:
            lines += ["_None_", ""]
            continue
        for g in by_sev[sev]:
            lines += [
                f"**[{sev}] {g['area']}**",
                f"- Gap: {g['gap']}",
                f"- Action: {g['action']}",
                "",
            ]

    lines += [
        "## 7. What to check (validation checklist)",
        "",
        "### LookML / compile",
        "- [ ] Validator: 0 errors",
        "- [ ] One `primary_key: yes` per view",
        "- [ ] Every join has `relationship:` + `sql_on:`",
        "- [ ] Dialect-correct SQL",
        "",
        "### Data grain",
        "- [ ] Fact row count ≈ Power BI (same filters)",
        "- [ ] No unexpected fan-out (count vs count_distinct on PK)",
        "- [ ] Orphan FK rate understood for left_outer",
        "",
        "### Business logic",
        "- [ ] All HIGH gaps closed or signed off",
        "- [ ] Calculated columns available",
        "- [ ] Required measures implemented and spot-checked",
        "- [ ] Inactive / M:M joins reviewed",
        "",
        "### Security & ops",
        "- [ ] RLS / access_filter decision recorded",
        "- [ ] Caching / datagroup set",
        "- [ ] QA explores hidden from end users",
        "",
        "## 8. Acceptance criteria",
        "",
        "1. Validator clean on target connection.",
        "2. HIGH gaps closed or formally accepted.",
        "3. At least 5 Power BI business questions reproduce in Looker within agreed tolerance.",
        "4. Remaining MEDIUM/LOW gaps have owners and dates.",
        "",
        "**KPI parity is NOT automatic.**",
        "",
        "## 9. Inventory snapshot",
        "",
    ]
    counts = c.get("counts") or {}
    if isinstance(counts, dict):
        for k, v in counts.items():
            if isinstance(v, (int, float, str)):
                lines.append(f"- {k}: **{v}**")
    lines += [
        "",
        "## 10. Out of scope",
        "",
        "- Power BI report pages, visuals, bookmarks, themes",
        "- Automatic warehouse DDL generation",
        "- Automatic KPI certification",
        "",
        "---",
        "",
        f"_Generated by phase2/generate_developer_guide.py for `{c['source']}`._",
        "",
    ]
    return "\n".join(lines)


class GuidePDF(FPDF):
    def footer(self):
        self.set_y(-11)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, latin1(f"Looker Developer Guide  |  Page {self.page_no()}"), align="C")


def _ensure_space(pdf: GuidePDF, need: float = 28) -> None:
    if pdf.get_y() > 297 - 14 - need:
        pdf.add_page()


def _reset_x(pdf: GuidePDF, margin: float) -> None:
    pdf.set_x(margin)


def _h1(pdf: GuidePDF, margin: float, w: float, text: str) -> None:
    _ensure_space(pdf, 20)
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(18, 70, 120)
    pdf.multi_cell(w, 8, latin1(text))
    pdf.set_text_color(35, 35, 35)
    pdf.ln(1)
    _reset_x(pdf, margin)


def _h2(pdf: GuidePDF, margin: float, w: float, text: str) -> None:
    _ensure_space(pdf, 16)
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 90, 140)
    pdf.multi_cell(w, 6.5, latin1(soft_wrap(text, 95)))
    pdf.set_text_color(35, 35, 35)
    _reset_x(pdf, margin)


def _p(pdf: GuidePDF, margin: float, w: float, text: str, size: int = 10) -> None:
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(w, 5.1, latin1(soft_wrap(text, 100)))
    _reset_x(pdf, margin)


def _label(pdf: GuidePDF, margin: float, w: float, text: str) -> None:
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(w, 5.2, latin1(text))
    pdf.set_text_color(35, 35, 35)
    _reset_x(pdf, margin)


def _bullet(pdf: GuidePDF, margin: float, w: float, text: str, size: int = 10) -> None:
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(w, 5.0, latin1(soft_wrap(f"* {text}", 98)))
    _reset_x(pdf, margin)


def _code(pdf: GuidePDF, margin: float, w: float, text: str) -> None:
    _ensure_space(pdf, 24)
    _reset_x(pdf, margin)
    pdf.set_fill_color(245, 247, 250)
    pdf.set_font("Courier", "", 8)
    for line in soft_wrap(text, 88).splitlines() or [""]:
        _ensure_space(pdf, 8)
        _reset_x(pdf, margin)
        pdf.multi_cell(w, 4.2, latin1(line), fill=True)
    pdf.ln(1)
    _reset_x(pdf, margin)


def _gap_box(pdf: GuidePDF, margin: float, w: float, g: dict) -> None:
    _ensure_space(pdf, 32)
    sev = g["severity"]
    colors = {"HIGH": (160, 40, 40), "MEDIUM": (160, 100, 20), "LOW": (60, 100, 60)}
    r, g_, b = colors.get(sev, (80, 80, 80))
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(r, g_, b)
    pdf.multi_cell(w, 5.5, latin1(f"GAP [{sev}] — {g['area']}"))
    pdf.set_text_color(35, 35, 35)
    _p(pdf, margin, w, f"What is missing: {g['gap']}", 9)
    _label(pdf, margin, w, "What to do:")
    _p(pdf, margin, w, g["action"], 9)
    pdf.ln(2)


def _render_object_card(pdf: GuidePDF, margin: float, w: float, idx: int, row: dict) -> None:
    """Full-width object mapping card — never side-by-side clipped text."""
    pdf.add_page()
    _h1(pdf, margin, w, f"4.{idx} Object equivalence")
    _h2(pdf, margin, w, f"{row['power_bi']}  ->  {row['looker']}")
    _label(pdf, margin, w, "What it means")
    _p(pdf, margin, w, row.get("summary") or row["how_to_create"], 10)

    _label(pdf, margin, w, "How to build (follow these steps)")
    for n, step in enumerate(row.get("build_steps") or [row["how_to_create"]], 1):
        _bullet(pdf, margin, w, f"{n}. {step}", 9)

    _label(pdf, margin, w, "What to check")
    for chk in row.get("checks") or []:
        _bullet(pdf, margin, w, f"[ ] {chk}", 9)

    _label(pdf, margin, w, "Suggestions / best practice")
    for s in row.get("suggestions") or []:
        _bullet(pdf, margin, w, s, 9)

    if row.get("example"):
        _label(pdf, margin, w, "Example LookML")
        _code(pdf, margin, w, row["example"])

    if row.get("refs"):
        _label(pdf, margin, w, "References")
        for u in row["refs"]:
            _bullet(pdf, margin, w, u, 8)


def make_pdf(ctx: dict) -> None:
    pdf = GuidePDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, 14)
    margin = 14.0
    w = 210.0 - 2 * margin

    # Cover
    pdf.add_page()
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(18, 70, 120)
    pdf.multi_cell(w, 10, latin1("Looker Developer Guide"))
    _reset_x(pdf, margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(w, 7, latin1("Power BI -> LookML build playbook for developers"))
    pdf.ln(3)
    for line in [
        f"Source PBIX: {ctx['source']}",
        f"LookML model: {ctx['model']}",
        f"Primary fact / explore: {ctx['fact']}",
        "Approach: deterministic Phase 2 (inventory-driven)",
        "This PDF: full instructions, checks, suggestions, examples, and gaps",
    ]:
        _p(pdf, margin, w, line, 11)
    pdf.ln(3)
    _label(pdf, margin, w, "Inside this guide")
    for b in [
        "Section 4: every PBI object type with step-by-step build instructions (one topic per page)",
        "Section 5: concrete build plan for THIS PBIX (views, joins, measures, M)",
        "Section 6: prioritized GAP list with actions",
        "Sections 7-8: validation checklist and acceptance criteria",
    ]:
        _bullet(pdf, margin, w, b)

    # How to use + best practices
    pdf.add_page()
    _h1(pdf, margin, w, "1. How to use this guide")
    for b in [
        "Read Best practices first — mandatory.",
        "Complete Prerequisites before editing LookML.",
        "Read each Object equivalence page fully (Build + Check + Suggestions + Example).",
        "Execute Build plan for this PBIX.",
        "Close HIGH gaps (or get written sign-off).",
        "Sign off using Validation and acceptance.",
    ]:
        _bullet(pdf, margin, w, b)

    _h1(pdf, margin, w, "2. Best practices (mandatory)")
    practices = [
        ("Primary key on every view", "Put primary_key: yes on the unique key. Required for symmetric aggregates."),
        ("Explicit join relationship", "Always set relationship: many_to_one (or the correct cardinality). Never omit it."),
        ("Measures reference dimensions", "Prefer sql: ${dimension} over raw ${TABLE}.col when the dimension exists."),
        ("Warehouse owns ETL", "Power Query M is NOT LookML. Rebuild transforms in dbt/Dataform/SQL first."),
        ("Granular includes", "Prefer include per view file (looker-skills modeling guidelines)."),
        ("Explore descriptions", "Every explore needs label + description."),
        ("No silent M:M / inactive joins", "Review fan-out risk; use bridge tables or aliased joins intentionally."),
        ("No KPI claims without tests", "Complex DAX TODOs are unfinished until side-by-side parity passes."),
    ]
    for title, body in practices:
        _h2(pdf, margin, w, title)
        _p(pdf, margin, w, body, 9)

    pdf.add_page()
    _h1(pdf, margin, w, "3. Prerequisites checklist")
    for b in [
        "[ ] Looker project + Git branch ready",
        "[ ] Admin connection created",
        "[ ] Warehouse tables exist (or creation tickets filed)",
        "[ ] Phase 1 inventory is for THIS PBIX",
        "[ ] LOOKML_PROJECT.zip imported",
        "[ ] SQL dialect known (BigQuery SAFE_DIVIDE vs Snowflake DIV0)",
    ]:
        _bullet(pdf, margin, w, b)
    _p(
        pdf,
        margin,
        w,
        "Do not start LookML polish until connection and warehouse tables are real. "
        "Placeholder YOUR_LOOKER_CONNECTION / YOUR_PROJECT.YOUR_DATASET will fail validation.",
        10,
    )

    # One full page per object equivalence entry — fixes clipped side text
    for idx, row in enumerate(OBJECT_EQUIVALENCE, 1):
        _render_object_card(pdf, margin, w, idx, row)

    # Build plan
    pdf.add_page()
    _h1(pdf, margin, w, "5. Build plan for this PBIX")
    _h2(pdf, margin, w, "Step A — Import LookML ZIP")
    for b in [
        "Unzip LOOKML_PROJECT.zip into the Looker project.",
        "Open models/<model>.model.lkml and set connection.",
        "Run LookML Validator (expect table errors until Step B).",
    ]:
        _bullet(pdf, margin, w, b)

    _h2(pdf, margin, w, "Step B — Point each view at the warehouse")
    _p(pdf, margin, w, "For each view: set sql_table_name, confirm PK and columns exist.", 9)
    for v in ctx["view_build"]:
        _ensure_space(pdf, 22)
        _label(pdf, margin, w, f"View `{v['lookml_view']}` (Power BI: {v['pbi_table']})")
        _p(
            pdf,
            margin,
            w,
            f"File: {v['file']} | columns: {v['columns']} | PK guess: {v['pk_guess']} | "
            f"date cols: {', '.join(v['date_columns']) or 'none'}",
            9,
        )
        _bullet(pdf, margin, w, "Confirm primary_key matches warehouse uniqueness.", 9)
        _bullet(pdf, margin, w, "Map dates to dimension_group timeframes.", 9)
        if v.get("is_calculated_table"):
            _bullet(pdf, margin, w, "GAP: calculated table — ensure warehouse materialization exists.", 9)

    _h2(pdf, margin, w, "Step C — Explores and joins")
    _p(pdf, margin, w, f"Primary explore base: {ctx['fact']}. Set type + relationship + sql_on on every join.", 9)
    for j in ctx["join_build"]:
        active = "ACTIVE" if j["active"] else "INACTIVE"
        _label(pdf, margin, w, f"{j['from']} -> {j['to']} [{j['cardinality']}, {active}]")
        _p(pdf, margin, w, f"Looker action: {j['looker']}", 9)
        if not j["active"]:
            _bullet(pdf, margin, w, "Keep aliased; do not use as default path until a measure needs it.", 9)
        if "M:M" in str(j["cardinality"]).upper().replace(" ", ""):
            _bullet(pdf, margin, w, "HIGH GAP: many-to-many — prefer bridge table; verify aggregates.", 9)

    pdf.add_page()
    _h2(pdf, margin, w, "Step D — Measures")
    if not ctx["measures"]:
        _p(
            pdf,
            margin,
            w,
            "GAP: This PBIX has 0 DAX measures. Add explicit LookML measures on the fact view "
            "for KPIs users expect (count, count_distinct on keys, averages on numeric columns).",
            10,
        )
    else:
        _p(pdf, margin, w, f"Mapped measures: {len(ctx['measure_plans'])}. TODOs: {len(ctx['todo_measures'])}.", 10)
        for m in ctx["measure_plans"][:50]:
            flag = "TODO" if m.get("status") == "todo" else "OK"
            _bullet(pdf, margin, w, f"[{flag}] {m.get('power_bi')} — strategy={m.get('strategy')}", 8)

    _h2(pdf, margin, w, "Step E — Calculated columns (build in warehouse)")
    if not ctx["calc_biz"]:
        _p(pdf, margin, w, "No business calculated columns.", 10)
    else:
        _p(pdf, margin, w, f"{len(ctx['calc_biz'])} calculated columns — materialize then expose as dimensions.", 10)
        for cc in ctx["calc_biz"]:
            expr = (cc.get("expression") or "").replace("\n", " ")[:110]
            _bullet(pdf, margin, w, f"{cc.get('table')}.{cc.get('column_name')}: {expr}", 8)

    _h2(pdf, margin, w, "Step F — Power Query M (Looker / warehouse equivalent)")
    _p(
        pdf,
        margin,
        w,
        "Best practice: warehouse table/view + straight LookML view. "
        "SDT only as temporary bridge. Heavy M stays in ETL. "
        "Full stubs are in LOOKML_PROJECT.zip under lookml/m_migration/.",
        9,
    )
    mrec = ctx.get("m_recommendations") or {}
    rec_rows = mrec.get("recommendations") or []
    if not rec_rows:
        for q in ctx["queries"]:
            qn = q.get("query_name") or q.get("name")
            _bullet(
                pdf,
                margin,
                w,
                f"Rebuild query `{qn}` (source_type={q.get('source_type')}) using m_migration stubs.",
                9,
            )
    else:
        for r in rec_rows:
            _ensure_space(pdf, 28)
            _label(
                pdf,
                margin,
                w,
                f"{r.get('query_name')} -> {r.get('recommended_pattern')}",
            )
            _p(pdf, margin, w, f"Looker object: {r.get('looker_object')}", 9)
            _p(pdf, margin, w, f"Why: {r.get('rationale')}", 8)
            for i, s in enumerate((r.get("steps") or [])[:4], 1):
                _bullet(pdf, margin, w, f"{i}. {s}", 8)
            _bullet(
                pdf,
                margin,
                w,
                f"Files: m_migration/sql/{snake_case(r.get('query_name') or '')}.sql and "
                f"lookml_stubs/{snake_case(r.get('query_name') or '')}_recommended.lkml",
                8,
            )

    # Gaps
    pdf.add_page()
    _h1(pdf, margin, w, "6. Gaps — prioritize and close")
    _p(pdf, margin, w, "Each gap blocks production readiness until resolved or formally accepted.", 10)
    for sev in ("HIGH", "MEDIUM", "LOW"):
        items = [g for g in ctx["gaps"] if g["severity"] == sev]
        if not items:
            continue
        _h2(pdf, margin, w, f"Severity {sev} ({len(items)})")
        for g in items:
            _gap_box(pdf, margin, w, g)

    # Validation
    pdf.add_page()
    _h1(pdf, margin, w, "7. What to check (validation)")
    _h2(pdf, margin, w, "LookML compile")
    for b in ["[ ] Validator: 0 errors", "[ ] One primary_key per view", "[ ] Every join has relationship + sql_on", "[ ] Dialect-correct SQL"]:
        _bullet(pdf, margin, w, b)
    _h2(pdf, margin, w, "Grain and joins")
    for b in ["[ ] Fact row count matches Power BI (same filters)", "[ ] count vs count_distinct(PK) shows no unexpected fan-out", "[ ] Orphan FK rate understood for left_outer joins"]:
        _bullet(pdf, margin, w, b)
    _h2(pdf, margin, w, "Business logic")
    for b in ["[ ] All HIGH gaps closed or signed off", "[ ] Calculated columns available", "[ ] Required measures implemented and spot-checked vs Power BI", "[ ] Inactive / M:M joins reviewed"]:
        _bullet(pdf, margin, w, b)
    _h2(pdf, margin, w, "Security and ops")
    for b in ["[ ] RLS / access_filter decision recorded", "[ ] Caching / datagroup set", "[ ] QA explores hidden from end users"]:
        _bullet(pdf, margin, w, b)

    _h1(pdf, margin, w, "8. Acceptance criteria")
    for b in [
        "Validator clean on target connection",
        "HIGH gaps closed or formally accepted",
        "At least 5 Power BI business questions reproduce in Looker within agreed tolerance",
        "Remaining MEDIUM/LOW gaps have owners and dates",
        "Do NOT publish claiming full KPI parity while DAX TODOs remain",
    ]:
        _bullet(pdf, margin, w, b)

    pdf.add_page()
    _h1(pdf, margin, w, "9. Inventory snapshot")
    counts = ctx.get("counts") or {}
    if isinstance(counts, dict):
        for k, v in counts.items():
            if isinstance(v, (int, float, str)):
                _bullet(pdf, margin, w, f"{k}: {v}", 10)

    _h1(pdf, margin, w, "10. Out of scope")
    for b in [
        "Power BI report pages, visuals, bookmarks, themes",
        "Automatic warehouse DDL generation",
        "Automatic KPI certification",
    ]:
        _bullet(pdf, margin, w, b)

    pdf.ln(4)
    _p(pdf, margin, w, f"Generated by phase2/generate_developer_guide.py for {ctx['source']}.", 8)
    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def generate(
    mapping_path: Path | None = None,
    inv_dir: Path | None = None,
) -> dict:
    mapping = load_json(mapping_path or MAPPING_JSON)
    summary = load_json(SUMMARY_JSON)
    inv = load_inventory(inv_dir or PHASE1_INV)
    ctx = analyze(inv, mapping, summary)
    md = build_markdown(ctx)
    MD_OUT.write_text(md)
    print("Wrote", MD_OUT)
    make_pdf(ctx)
    (ROOT / "GAPS.json").write_text(json.dumps(ctx["gaps"], indent=2))
    return {"md": str(MD_OUT), "pdf": str(PDF_OUT), "gaps": len(ctx["gaps"])}


if __name__ == "__main__":
    info = generate()
    print(json.dumps(info, indent=2))
