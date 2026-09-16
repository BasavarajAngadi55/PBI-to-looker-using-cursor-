#!/usr/bin/env python3
"""Generate Phase-3 Dashboard Developer Guide (PDF + MD)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
PDF_OUT = ROOT / "DASHBOARD_DEVELOPER_GUIDE.pdf"
MD_OUT = ROOT / "DASHBOARD_DEVELOPER_GUIDE.md"


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
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def _load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    return json.loads(path.read_text(encoding="utf-8"))


class GuidePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, latin1("PBIX -> Looker | Phase 3 Dashboard Developer Guide"), align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 7, latin1(text))
        self.ln(2)

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
        self.ln(1)

    def bullet(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, latin1(f"  - {text}"))

    def code_block(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("Courier", "", 8)
        self.set_text_color(30, 41, 59)
        self.set_fill_color(241, 245, 249)
        usable = self.w - self.l_margin - self.r_margin
        self.multi_cell(usable, 4.5, latin1(text), fill=True)
        self.ln(2)


def build_markdown(coverage: dict, pages: list) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    weighted = coverage.get("weighted_completion_pct", 0)
    target = coverage.get("target_pct", 70)
    lines = [
        "# Dashboard Developer Guide — Phase 3",
        "",
        f"_Generated {ts}_",
        "",
        "## Purpose",
        "",
        "Convert Power BI report **pages** into Looker **LookML dashboards** using deterministic rules.",
        "This is best-effort functional parity — **not** pixel-perfect recreation.",
        "",
        f"**Weighted completion:** {weighted}% (target ≥ {target}%).",
        "",
        "## What Looker gets",
        "",
        "| Power BI | Looker equivalent | Notes |",
        "|----------|-------------------|-------|",
        "| Report page | `.dashboard.lookml` | One file per page |",
        "| Card / KPI | `single_value` | Primary measure |",
        "| Clustered bar/column | `looker_bar` / `looker_column` | Category + measure |",
        "| Line / area | `looker_line` / `looker_area` | Time/category + measure |",
        "| Pie / donut | `looker_pie` | Category + measure |",
        "| Table / matrix | `looker_grid` | Dimensions + measures |",
        "| Slicer | Dashboard `filters` + `listen` | Cross-tile filtering |",
        "| Text box | `text` tile | Title/subtitle |",
        "| Shape / image / button | Skipped or gap tile | See deficiencies |",
        "",
        "## Prerequisites",
        "",
        "1. Phase 1 inventory exists for the same PBIX.",
        "2. Phase 2 LookML model + explore are generated.",
        "3. Warehouse tables / views behind Phase 2 are deployed (or use SQL runner).",
        "",
        "## Deploy LookML dashboards",
        "",
        "1. Unzip `LOOKML_DASHBOARDS.zip`.",
        "2. Copy `dashboards/*.dashboard.lookml` into your LookML project (same project as Phase 2).",
        "3. Ensure each dashboard `model:` and tile `explore:` match Phase 2 names.",
        "4. Validate in Looker IDE; deploy to a non-prod folder.",
        "5. Open each dashboard; fix any red fields (missing from explore).",
        "",
        "## Page inventory",
        "",
    ]
    for p in pages:
        name = p.get("display_name") or p.get("name") or p.get("slug")
        slug = p.get("slug") or p.get("name")
        n = p.get("visual_count", 0)
        lines.append(f"- **{name}** → `dashboards/{slug}.dashboard.lookml` ({n} visuals)")
    lines += [
        "",
        "## Coverage summary",
        "",
        f"- Mapped / generated: {coverage.get('mapped_visuals', '—')}",
        f"- Partial: {coverage.get('partial_visuals', '—')}",
        f"- Gaps / skipped: {coverage.get('gap_visuals', '—')} gaps; "
        f"{coverage.get('skipped_decorative', '—')} decorative skips",
        f"- Weighted completion: **{weighted}%**",
        "",
        "## Deficiencies (expected)",
        "",
        "- Bookmarks / buttons / page navigation",
        "- Drillthrough / drill-down hierarchies as PBI defines them",
        "- Custom visuals / R / Python visuals",
        "- Exact pixel layout, themes, backgrounds, images",
        "- Combo charts, treemaps, maps (partial or gap tiles)",
        "- Sync slicers across pages (configure manually if needed)",
        "",
        "Each gap appears as a **text tile** on the Looker dashboard so nothing is silently dropped.",
        "",
        "## How to reach ~100%",
        "",
        "1. Replace gap tiles with native Looker viz or extensions.",
        "2. Add missing fields to Phase 2 views / explores.",
        "3. Rebuild complex KPI cards with `single_value` + comparison measures.",
        "4. Recreate navigation with Looker dashboard links / folders.",
        "5. Apply Looker themes / CSS for brand parity (optional).",
        "",
        "## Hard rules",
        "",
        "- Never invent visuals that are not in the PBIX layout.",
        "- Field references must resolve via Phase 2 naming.",
        "- Report weighted coverage honestly — do not claim pixel parity.",
        "",
    ]
    return "\n".join(lines)


def build_pdf(coverage: dict, pages: list):
    pdf = GuidePDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 14, 14)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover band
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 40, style="F")
    pdf.set_text_color(45, 212, 191)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(14, 10)
    pdf.cell(180, 6, latin1("PBIX -> Looker  |  Phase 3"))
    pdf.set_text_color(248, 250, 252)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(14, 18)
    pdf.cell(180, 10, latin1("Dashboard Developer Guide"))
    weighted = coverage.get("weighted_completion_pct", 0)
    target = coverage.get("target_pct", 70)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(14, 30)
    pdf.cell(180, 5, latin1(f"Weighted completion {weighted}%  |  target >= {target}%  |  best-effort Looker parity"))

    pdf.set_y(48)
    pdf.h1("1. What this guide is")
    pdf.body(
        "Deterministic conversion of Power BI report pages into Looker LookML dashboards. "
        "Use PAGE_COMPARISON.md side-by-side with each .dashboard.lookml file. "
        "Pixel-perfect recreation is not claimed; functional analytics tiles are the goal."
    )

    pdf.h1("2. Power BI -> Looker visual map")
    pdf.body(
        "Card/KPI -> single_value. Bar/column -> looker_bar/column. Line/area -> looker_line/area. "
        "Pie/donut -> looker_pie. Table/matrix -> looker_grid. Slicer -> dashboard filters + listen. "
        "Text -> text tile. Shapes/images/buttons skipped or marked as gaps."
    )

    pdf.h1("3. Pages in this PBIX")
    for p in pages:
        name = p.get("display_name") or p.get("name") or "Page"
        slug = p.get("slug") or p.get("name") or "page"
        n = p.get("visual_count", 0)
        pdf.bullet(f"{name}  =>  dashboards/{slug}.dashboard.lookml  ({n} visuals)")

    pdf.h1("4. Deploy steps")
    for step in [
        "Unzip LOOKML_DASHBOARDS.zip into the LookML project that already has Phase 2 model/views.",
        "Confirm model: and explore: names match Phase 2 output.",
        "Push to Looker (dev mode). Open each dashboard and resolve any missing fields.",
        "Wire filters: slicers become dashboard filters; tiles already listen where mapped.",
        "Use comparison/PAGE_COMPARISON.md as the acceptance checklist per page.",
    ]:
        pdf.bullet(step)

    pdf.h1("5. Coverage and deficiencies")
    pdf.body(
        f"Weighted completion is {weighted}% against a {target}% target. "
        "Gaps include bookmarks, drillthrough, custom visuals, themes, exact layout, "
        "and partial support for combo/treemap/map. Gap tiles remain on the dashboard so deficiencies are visible."
    )
    pdf.body(
        f"Mapped: {coverage.get('mapped_visuals', 'n/a')}  |  "
        f"Partial: {coverage.get('partial_visuals', 'n/a')}  |  "
        f"Gaps: {coverage.get('gap_visuals', 'n/a')}"
    )

    pdf.h1("6. How to finish remaining work")
    for tip in [
        "Add missing dimensions/measures in Phase 2 views, then re-run Phase 3 field bind.",
        "Replace gap text tiles with Looker native viz or marketplace visualizations.",
        "Recreate navigation with Looker links / board folders instead of PBI bookmarks.",
        "Apply Looker themes for brand; do not expect identical PBI theme JSON.",
    ]:
        pdf.bullet(tip)

    pdf.h1("7. Hard rules")
    pdf.code_block(
        "Never invent visuals not present in PBIX Layout.\n"
        "Field refs must come from Phase 1/2 inventory naming.\n"
        "Report coverage honestly - do not claim 100% pixel parity.\n"
        "No LLM in Phase 3 extract/map/emit path."
    )

    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def main():
    coverage = _load_json(INV / "COVERAGE.json", {})
    mapping = _load_json(INV / "03_dashboard_mapping.json", {})
    pages_doc = _load_json(INV / "01_report_pages.json", {})
    pages = pages_doc.get("pages") if isinstance(pages_doc, dict) else pages_doc
    if not isinstance(pages, list):
        pages = mapping.get("pages") or []

    md = build_markdown(coverage, pages)
    MD_OUT.write_text(md, encoding="utf-8")
    print("Wrote", MD_OUT)
    build_pdf(coverage, pages)


if __name__ == "__main__":
    main()
