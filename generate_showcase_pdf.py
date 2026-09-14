#!/usr/bin/env python3
"""Generate audience showcase PDF for PBIX -> Looker inventory methodology."""
from pathlib import Path
from fpdf import FPDF

OUT = Path("/Users/Basavaraj_Angadi/Desktop/data eng /PBIX_to_Looker_Inventory_Showcase.pdf")
MD_OUT = Path("/Users/Basavaraj_Angadi/Desktop/data eng /PBIX_to_Looker_Inventory_Showcase.md")


class ShowcasePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Power BI to Looker - Semantic Inventory Showcase", align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Confidential methodology showcase", align="C")

    def h1(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(20, 40, 80)
        self.multi_cell(0, 10, text)
        self.ln(2)

    def h2(self, text):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 110)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def h3(self, text):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 70, 100)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=8):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, f"- {text}")

    def callout(self, title, text):
        self.set_x(self.l_margin)
        usable = self.w - self.l_margin - self.r_margin
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

    def code_block(self, text):
        self.set_x(self.l_margin)
        usable = self.w - self.l_margin - self.r_margin
        self.set_font("Courier", "", 8)
        self.set_text_color(20, 20, 20)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(usable, 4.2, text, fill=True)
        self.ln(2)

    def table(self, headers, rows, col_widths=None):
        self.set_x(self.l_margin)
        if col_widths is None:
            usable = self.w - self.l_margin - self.r_margin
            col_widths = [usable / len(headers)] * len(headers)
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(30, 60, 110)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            self.set_x(self.l_margin)
            if self.get_y() > 270:
                self.add_page()
                self.set_x(self.l_margin)
                self.set_font("Helvetica", "B", 8)
                self.set_fill_color(30, 60, 110)
                self.set_text_color(255, 255, 255)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=1, fill=True)
                self.ln()
                self.set_font("Helvetica", "", 8)
                self.set_text_color(30, 30, 30)
            self.set_fill_color(248, 248, 248)
            line_hs = []
            for i, cell in enumerate(row):
                lines = self.multi_cell(
                    col_widths[i], 4.5, str(cell), dry_run=True, output="LINES"
                )
                line_hs.append(max(len(lines), 1) * 4.5)
            rh = max(line_hs + [6])
            x0, y0 = self.l_margin, self.get_y()
            for i, cell in enumerate(row):
                self.set_xy(x0 + sum(col_widths[:i]), y0)
                self.rect(x0 + sum(col_widths[:i]), y0, col_widths[i], rh)
                self.multi_cell(col_widths[i], 4.5, str(cell), fill=fill)
            self.set_y(y0 + rh)
            fill = not fill
        self.ln(2)


def build_markdown() -> str:
    return """# Power BI to Looker Semantic Inventory Showcase

## Executive summary

This showcase documents a complete, inventory-first methodology for migrating a Power BI semantic model (PBIX) to Google Looker (LookML), using the Microsoft / obviEnce **Human Resources Sample PBIX** as the working example.

**What we proved:** Every semantic-model object can be extracted, catalogued, action-tagged, and linked to blockers (especially Power Query M dependencies) before any LookML is treated as "done."

**Out of scope (by design):** Report pages, visuals, dashboards, bookmarks, themes.

**Not using dbt:** Warehouse SQL / Looker PDTs / LookML dimension SQL instead.

---

## Why an agentic architecture is needed

A PBIX is not one artifact - it is several tightly coupled layers:

1. Tabular schema (tables, columns, types)
2. Relationships (cardinality, cross-filter)
3. DAX (measures, calculated columns, calculated tables)
4. Power Query M (source SQL, unions, seeds, transforms)
5. TM extras (partitions, hierarchies, RLS, annotations, auto date tables)

A single "convert to LookML" pass misses M dependencies, stubs complex DAX silently, and cannot prove completeness.

### Agentic design (specialist roles + merger)

```
PBIX
 +- Agent Schema        -> 01_tables_columns.json
 +- Agent DAX           -> 02_dax_objects.json
 +- Agent Relationships -> 03_relationships.json
 +- Agent M / Power Query -> 04_power_query_m.json + 04_m_raw/*.m
 +- Agent TM Extras     -> 05_tmschema_extras.json
 +- Merger + Gate       -> OBJECT_INVENTORY.md + ACTION_MATRIX.csv + COMPLETENESS_GATE.json
```

**Why specialists:**
- Parallelism and focus (each role has one contract)
- Less hallucination / skipped categories
- Empty categories must be listed as empty (NONE_IN_SOURCE), not omitted
- Merger enforces a hard completeness gate before LookML is trusted

**Implementation note for this engagement:** Roles ran as one orchestrated extractor (`inventory/capture_pbix_inventory.py`) with the same contracts - logical multi-agent architecture, single process for consistency.

---

## Source and workspace

| Item | Value |
|------|-------|
| PBIX | Human Resources Sample PBIX.pbix |
| Path | /Users/.../Downloads/Human Resources Sample PBIX.pbix |
| Engine | pbixray (XPress9 DataModel decompress) |
| Workspace | Desktop/data eng / |
| Reports/dashboards | Excluded |
| dbt | Not used |

---

## What we captured (completeness gate PASSED)

| Object class | Count | Artifact |
|--------------|------:|----------|
| Tables (all) | 15 | 01_tables_columns.json |
| Columns | 87 | 01_tables_columns.json |
| DAX measures (full text) | 30 | 02_dax_objects.json |
| Calculated columns (full text) | 43 | 02_dax_objects.json |
| Calculated tables (full text) | 6 | 02_dax_objects.json |
| Relationships | 8 | 03_relationships.json |
| Power Query queries + .m files | 9 | 04_m_raw/*.m |
| Empty TM categories listed | 29 | 05_tmschema_extras.json |
| Action matrix rows | 237 | ACTION_MATRIX.csv |

Gate rules: table count match, every column listed, full DAX text, all relationships, all M files on disk, empty TM categories explicit.

---

## Tables in the PBIX

### Business tables (9) - Power Query M

Employee (fact), Date, BU, AgeGroup, Ethnicity, FP, Gender, PayType, SeparationReason

### Internal auto date tables (6) - ALSO CAPTURED

DateTableTemplate_*, LocalDateTable_* (x5)

These were fully inventoried (columns + Calendar DAX + 36 calc columns). Tagged SKIP_PBI_INTERNAL for default Looker migration - **capture ≠ skip extraction**.

---

## Action tagging (what to do next)

| Tag | Meaning |
|-----|---------|
| LOOKML_VIEW_DIM / FACT | Build LookML views |
| LOOKML_MEASURE | Straight measure mapping |
| LOOKML_JOIN | Explore joins from relationships |
| LOOKML_TODO_COMPLEX | SPLY, EmpCount max period, TO % Norm |
| WAREHOUSE_SQL / (was DBT_SQL) | Rebuild M/SQL in warehouse or PDT |
| WAREHOUSE_SEED | Embedded M seed tables |
| SKIP_PBI_INTERNAL | Auto date tables - captured, optional LookML |
| NONE_IN_SOURCE | Confirmed empty (e.g. RLS) |

---

## Blocked items - clear M -> KPI chains

Example:

```
BLOCKED: New Hires YoY % Change
  +-- needs New Hires SPLY     (SAMEPERIODLASTYEAR - LookML complex)
        +-- needs New Hires    (SUM isNewHire)
              +-- needs isNewHire (DAX calc column)
                    +-- needs hr.employee from Employee.m  <- M DEPENDENCY
```

Primary blockers:
1. Employee.m not loaded to warehouse -> almost all KPIs blocked
2. Dim M/SQL (Date, BU, FP, ...) missing -> slices blocked
3. Seed M (AgeGroup, Gender, Ethnicity) missing -> diversity KPIs blocked
4. Calc columns (isNewHire, BadHires, tenure, ...) -> named KPI dependencies
5. SPLY / EmpCount / TO % Norm -> LookML complex
6. KPI parity tests not yet run

Full detail: BLOCKERS_AND_DEPENDENCIES.md

---

## LookML produced (draft)

views/*.view.lkml (9 business views), models/human_resources.model.lkml (star explore + 8 joins).

Honest conversion estimate:
- Inventory/mapping: ~95-100%
- Runnable Looker without warehouse: ~40-50%
- After warehouse + simple measures: ~70%
- True 80%+ parity needs SPLY/EmpCount/TO% Norm + KPI checks

---

## Audience takeaways

1. Inventory before LookML - never skip M and calc columns
2. Agentic roles + completeness gate prevent silent gaps
3. Internal auto date tables must be captured even if not migrated
4. Blockers must name the .m file and KPIs above it
5. No dbt required - warehouse SQL / PDT / LookML SQL
6. KPI parity is a separate phase - files ≠ correct numbers

---

## Artifact index

inventory/01-05 JSON, 04_m_raw/*.m, OBJECT_INVENTORY.md, ACTION_MATRIX.csv, COMPLETENESS_GATE.json, views/, models/, BLOCKERS_AND_DEPENDENCIES.md, MIGRATION_SUMMARY.md, capture_pbix_inventory.py
"""


def main():
    MD_OUT.write_text(build_markdown())

    pdf = ShowcasePDF(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Cover
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(20, 40, 80)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 12, "Power BI to Looker", align="C")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 9, "Semantic Model Inventory & Migration Showcase", align="C")
    pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(
        0,
        6,
        "A detailed walkthrough of how every PBIX semantic object was captured,\n"
        "why an agentic architecture is required, what remains blocked\n"
        "(especially Power Query M dependencies), and how to unblock KPIs\n"
        "without dbt and without migrating reports/dashboards.",
        align="C",
    )
    pdf.ln(10)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        0,
        6,
        "Case study: Microsoft / obviEnce Human Resources Sample PBIX\n"
        "Scope: Semantic model only  |  Warehouse SQL (no dbt)  |  LookML drafts\n"
        "Completeness gate: PASSED",
        align="C",
    )
    pdf.ln(16)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "Audience deliverable - methodology + evidence from a real PBIX extraction",
        align="C",
    )

    # 1
    pdf.add_page()
    pdf.h1("1. Executive summary")
    pdf.body(
        "This engagement demonstrated an inventory-first Power BI to Looker migration "
        "method. Instead of jumping straight to LookML, we decompressed the PBIX DataModel, "
        "extracted every semantic-model object, tagged each object with a clear next action, "
        "and documented blockers as explicit dependency chains (M code -> table -> KPI)."
    )
    pdf.body(
        "Reports and dashboards were intentionally excluded. The goal was a trustworthy "
        "semantic inventory and an honest statement of what Looker can and cannot do until "
        "warehouse tables and complex DAX patterns are implemented."
    )
    pdf.callout(
        "Key result",
        "Completeness gate PASSED: 15 tables, 87 columns, 30 measures, 43 calculated columns, "
        "6 calculated tables, 8 relationships, 9 Power Query scripts (verbatim .m files), "
        "29 empty TM categories explicitly listed, 237 action-matrix rows.",
    )

    # 2
    pdf.h1("2. Why agentic architecture is needed")
    pdf.body(
        "A PBIX file is a compressed package. The analytical brain sits in a binary Analysis "
        "Services backup (often XPress9-compressed). Inside that model live multiple object "
        "families that do not convert 1:1 to LookML."
    )
    pdf.h3("What a single-pass converter typically misses")
    pdf.bullet("Power Query M SQL unions and seed tables (data cannot appear in Looker until rebuilt)")
    pdf.bullet("Calculated columns that KPIs depend on (e.g. isNewHire -> New Hires)")
    pdf.bullet("Time intelligence DAX (SAMEPERIODLASTYEAR) stubbed as NULL without disclosure")
    pdf.bullet("Hidden auto date tables silently dropped (capture incomplete)")
    pdf.bullet("Empty categories (RLS, KPIs) omitted instead of confirmed NONE_IN_SOURCE")

    pdf.h3("Specialist agent roles")
    pdf.body(
        "We used five specialist extractor roles plus a merger. Each role has one output "
        "contract. The merger fails the run unless completeness gates pass."
    )
    w = [38, 75, 77]
    pdf.table(
        ["Agent role", "Captures", "Output"],
        [
            ["Schema", "Tables, columns, types, stats", "01_tables_columns.json"],
            ["DAX", "Measures, calc columns/tables (full text)", "02_dax_objects.json"],
            ["Relationships", "M:1 joins, cross-filter, active", "03_relationships.json"],
            ["M / Power Query", "Verbatim M + embedded SQL + tags", "04_*.json + 04_m_raw/*.m"],
            ["TM extras", "Partitions, hierarchies, RLS, etc.", "05_tmschema_extras.json"],
            ["Merger + Gate", "Inventory + action tags + pass/fail", "OBJECT_INVENTORY + MATRIX"],
        ],
        w,
    )
    pdf.code_block(
        "PBIX\n"
        "  -> Agent Schema\n"
        "  -> Agent DAX\n"
        "  -> Agent Relationships\n"
        "  -> Agent M / Power Query\n"
        "  -> Agent TM Extras\n"
        "       \\-> Merger + Completeness Gate\n"
        "             -> OBJECT_INVENTORY.md\n"
        "             -> ACTION_MATRIX.csv\n"
        "             -> COMPLETENESS_GATE.json"
    )
    pdf.callout(
        "Why this matters for audiences / auditors",
        "Agentic separation creates evidence: every object class has a file, every empty "
        "class is listed, and LookML is not declared complete until the gate passes. "
        "In this project, roles ran inside one orchestrator script with identical contracts "
        "(logical multi-agent; single process for consistency).",
    )

    # 3
    pdf.h1("3. End-to-end journey (what we did)")
    pdf.h3("Step A - Locate and open the PBIX")
    pdf.body(
        "Source: Human Resources Sample PBIX (obviEnce / Microsoft sample). "
        "PBIX is a ZIP; DataModel uses XPress9 compression. We used pbixray on Python 3.12 "
        "to decompress and read the tabular model and mashup."
    )
    pdf.h3("Step B - Extract inventory (Phase 1)")
    pdf.body(
        "Ran capture_pbix_inventory.py to produce inventory artifacts and enforce the gate. "
        "Business tables and internal auto date tables were both captured."
    )
    pdf.h3("Step C - Action matrix")
    pdf.body(
        "Every object received exactly one primary action tag (LookML view/measure/join, "
        "warehouse SQL/seed, skip internal, or none-in-source). This becomes the backlog "
        "for conversion work."
    )
    pdf.h3("Step D - Draft LookML (not final KPI parity)")
    pdf.body(
        "Generated views/ and models/human_resources.model.lkml for the 9 business tables "
        "and 8 joins. Complex DAX left as TODO stubs with original expressions referenced."
    )
    pdf.h3("Step E - Blockers document (honest gaps)")
    pdf.body(
        "Wrote BLOCKERS_AND_DEPENDENCIES.md so every blocked KPI names its M-file or DAX "
        "dependency. No silent gaps."
    )

    # 4
    pdf.h1("4. Inventory evidence - tables")
    pdf.h3("Business tables created via Power Query (M)")
    pdf.table(
        ["Table", "Role", "Cols", "Origin"],
        [
            ["Employee", "Fact (monthly snapshot)", "16", "M + SQL Server union"],
            ["Date", "Calendar dimension", "12", "M + SQL HR.Date"],
            ["BU", "Business unit / region", "4", "M + SQL"],
            ["AgeGroup", "Age bands", "2", "M embedded seed"],
            ["Ethnicity", "Ethnicity lookup", "2", "M embedded seed"],
            ["FP", "Full / Part time", "2", "M + SQL"],
            ["Gender", "Gender lookup", "3", "M embedded seed"],
            ["PayType", "Hourly / Salaried", "2", "M + SQL"],
            ["SeparationReason", "Vol / Invol", "2", "M + SQL"],
        ],
        [40, 50, 18, 72],
    )
    pdf.h3("Internal auto date tables - captured, not ignored")
    pdf.body(
        "Power BI auto-generated 6 LocalDateTable_* / DateTableTemplate_* tables for time "
        "intelligence. We captured: all columns, Calendar(...) DAX, and 36 calculated "
        "columns (Year, MonthNo, Month, Quarter, Day). Tagged SKIP_PBI_INTERNAL for default "
        "Looker migration - meaning optional to implement as LookML views, NOT meaning "
        "skipped in inventory."
    )
    pdf.callout(
        "Audience clarification",
        "Capture everything first. Decide migration priority second. Internal tables prove "
        "the inventory is complete even when Looker will use dimension_group on Date instead.",
    )

    # 5
    pdf.h1("5. Inventory evidence - DAX, relationships, M")
    pdf.h3("Relationships (8) - all M:1")
    pdf.body(
        "Employee.date -> Date.Date; Employee.BU -> BU.BU; Employee.AgeGroupID -> AgeGroup; "
        "Employee.EthnicGroup -> Ethnicity; Employee.FP -> FP; Employee.Gender -> Gender.ID; "
        "Employee.PayTypeID -> PayType; Employee.TermReason -> SeparationReason. "
        "Mapped to Looker left_outer + many_to_one joins."
    )
    pdf.h3("Measures (30) - examples")
    pdf.table(
        ["Measure", "Pattern", "Action tag"],
        [
            ["New Hires", "SUM(isNewHire)", "LOOKML_MEASURE"],
            ["Actives / Seps", "Filtered counts", "LOOKML_MEASURE"],
            ["New Hires SPLY", "SAMEPERIODLASTYEAR", "LOOKML_TODO_COMPLEX"],
            ["EmpCount", "MAX(PeriodNumber) filter", "LOOKML_TODO_COMPLEX"],
            ["TO % Norm", "ALL(Gender/Ethnicity)", "LOOKML_TODO_COMPLEX"],
            ["BadHire%ofActives", "DIVIDE", "LOOKML_MEASURE"],
        ],
        [50, 70, 60],
    )
    pdf.h3("Power Query M - verbatim capture")
    pdf.body(
        "All 9 queries written to inventory/04_m_raw/*.m. Employee.m is the critical blocker: "
        "SQL Server query with UNION ALL of actives and separations, date shift +1 year, "
        "gender remap, EmplID%2 filter, month-grain snapshots."
    )

    # 6
    pdf.h1("6. When something is blocked - how we document it")
    pdf.body(
        "Blocked does not mean forgotten. For every blocker we record: status, why, "
        "dependency artifact (.m / DAX), KPIs unlocked only after fix, and how to achieve "
        "without dbt."
    )
    pdf.h3("Worked example - New Hires YoY %")
    pdf.code_block(
        "BLOCKED: New Hires YoY % Change\n"
        "  +-- needs: New Hires YoY Var\n"
        "        +-- needs: New Hires SPLY     <- LookML (SAMEPERIODLASTYEAR)\n"
        "              +-- needs: New Hires    <- SUM(isNewHire)\n"
        "                    +-- needs: isNewHire  <- DAX calculated column\n"
        "                          +-- needs: hr.employee from Employee.m\n"
        "                                <- M CODE DEPENDENCY (warehouse/PDT)"
    )
    pdf.h3("Blocker map (summary)")
    pdf.table(
        ["Blocker", "Type", "Impact"],
        [
            ["Employee.m not in warehouse", "M dependency", "Almost all KPIs"],
            ["Dim M/SQL missing", "M dependency", "Region/time/pay slices"],
            ["Seed dims missing", "M dependency", "Age/Gender/Ethnicity"],
            ["Calc columns", "DAX->SQL/LookML", "New Hires, Bad Hires, Tenure"],
            ["SPLY / YoY chain", "LookML complex", "All SPLY & YoY KPIs"],
            ["EmpCount max period", "LookML complex", "EmpCount (+ Actives parity)"],
            ["TO % Norm", "LookML complex", "TO % Norm / Var"],
            ["KPI parity not run", "Validation", "Confidence, not build"],
        ],
        [55, 40, 85],
    )
    pdf.body(
        "Suggestion for delivery teams: never say 'not supported in Looker' alone. "
        "Say 'blocked on Employee.m warehouse load' or 'blocked on SAMEPERIODLASTYEAR "
        "pattern' and list the KPI names above that blocker."
    )

    # 7
    pdf.h1("7. Conversion honesty - are we at 70-80%?")
    pdf.table(
        ["Layer", "Progress", "Meaning"],
        [
            ["Object capture / inventory", "~95-100%", "Gate passed"],
            ["Dim/fact + join design", "~80%", "LookML drafts exist"],
            ["Simple measures", "~70%", "Need real tables behind them"],
            ["Complex measures", "~15-25%", "Stubs / SPLY chain"],
            ["Warehouse tables (no dbt)", "~0-10%", "M extracted, not loaded"],
            ["KPI parity vs Power BI", "~0%", "Not validated yet"],
        ],
        [60, 35, 85],
    )
    pdf.body(
        "Interpretation: ~70-80% of understanding/mapping is done. Runnable Looker "
        "replacement is lower until warehouse tables exist. After warehouse + simple "
        "measures, usable conversion can approach ~70%; 80%+ true parity needs complex "
        "DAX and KPI checks."
    )

    # 8
    pdf.h1("8. Recommended next steps (no dbt, no dashboards)")
    pdf.bullet("Build warehouse views/tables (or Looker PDTs) from 04_m_raw/*.m")
    pdf.bullet("Materialize or Keep LookML SQL for isNewHire, BadHires, tenure, AgeGroupID, Region")
    pdf.bullet("Wire LookML sql_table_name / connection to those tables")
    pdf.bullet("Implement SPLY, EmpCount, TO % Norm; then YoY measures unlock")
    pdf.bullet("Run KPI parity checklist against Power BI for 10-15 core metrics")
    pdf.bullet("Optionally generate LookML for internal date tables if product requires them")

    # 9
    pdf.h1("9. Artifact index for the showcase folder")
    pdf.table(
        ["Path", "Purpose"],
        [
            ["inventory/01_tables_columns.json", "Full schema capture"],
            ["inventory/02_dax_objects.json", "Full DAX text"],
            ["inventory/03_relationships.json", "Joins"],
            ["inventory/04_power_query_m.json", "M metadata"],
            ["inventory/04_m_raw/*.m", "Verbatim Power Query"],
            ["inventory/05_tmschema_extras.json", "TM extras + empties"],
            ["inventory/OBJECT_INVENTORY.md", "Human-readable inventory"],
            ["inventory/ACTION_MATRIX.csv", "Object -> action backlog"],
            ["inventory/COMPLETENESS_GATE.json", "Pass/fail evidence"],
            ["views/ + models/", "Draft LookML"],
            ["BLOCKERS_AND_DEPENDENCIES.md", "M->KPI blocker chains"],
            ["MIGRATION_SUMMARY.md", "Earlier migration notes"],
            ["capture_pbix_inventory.py", "Repeatable extractor"],
        ],
        [75, 105],
    )

    # 10
    pdf.h1("10. Closing message for the audience")
    pdf.body(
        "Successful PBIX to Looker migration is not 'generate LookML and hope.' It is an "
        "evidence-based pipeline: specialist extraction, completeness gates, action tags, "
        "and explicit blocker chains from Power Query M up to business KPIs."
    )
    pdf.body(
        "If something cannot be converted yet, we say so clearly: here is the M dependency, "
        "here are the KPIs calculated from it, and here is how to achieve it in the warehouse "
        "or LookML - without hiding gaps behind a green 'migrated' status."
    )
    pdf.callout(
        "One-line thesis",
        "Capture everything. Tag everything. Block with names. Then build LookML.",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")
    print(f"Wrote {MD_OUT}")


if __name__ == "__main__":
    main()
