"""Deterministic Power BI visual type → Looker dashboard element mapping.

Sources:
- https://cloud.google.com/looker/docs/reference/param-lookml-dashboard-type
- https://cloud.google.com/looker/docs/building-lookml-dashboards
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class VisualMap:
    pbi_type: str
    looker_type: str | None
    status: str  # mapped | partial | gap | skip
    coverage_weight: float  # 1.0 mapped, 0.5 partial, 0.0 gap/skip
    notes: str
    looker_object: str


# Fixed deterministic table
VISUAL_EQUIVALENCE: dict[str, VisualMap] = {
    "card": VisualMap("card", "single_value", "mapped", 1.0, "KPI card → single_value tile", "single_value"),
    "kpi": VisualMap("kpi", "single_value", "partial", 0.7, "KPI with goal/trend → single_value (goal/trend not fully mirrored)", "single_value"),
    "columnChart": VisualMap("columnChart", "looker_column", "mapped", 1.0, "Column chart → looker_column", "looker_column"),
    "clusteredColumnChart": VisualMap("clusteredColumnChart", "looker_column", "mapped", 1.0, "Clustered columns → looker_column", "looker_column"),
    "clusteredBarChart": VisualMap("clusteredBarChart", "looker_bar", "mapped", 1.0, "Bar chart → looker_bar", "looker_bar"),
    "barChart": VisualMap("barChart", "looker_bar", "mapped", 1.0, "Bar chart → looker_bar", "looker_bar"),
    "lineChart": VisualMap("lineChart", "looker_line", "mapped", 1.0, "Line chart → looker_line", "looker_line"),
    "areaChart": VisualMap("areaChart", "looker_area", "mapped", 1.0, "Area chart → looker_area", "looker_area"),
    "stackedAreaChart": VisualMap("stackedAreaChart", "looker_area", "partial", 0.7, "Stacked area → looker_area (stacking may differ)", "looker_area"),
    "pieChart": VisualMap("pieChart", "looker_pie", "mapped", 1.0, "Pie → looker_pie", "looker_pie"),
    "donutChart": VisualMap("donutChart", "looker_pie", "partial", 0.8, "Donut → looker_pie (donut style limited)", "looker_pie"),
    "pivotTable": VisualMap("pivotTable", "looker_grid", "mapped", 1.0, "Matrix/pivot → looker_grid", "looker_grid"),
    "tableEx": VisualMap("tableEx", "looker_grid", "mapped", 1.0, "Table → looker_grid", "looker_grid"),
    "table": VisualMap("table", "looker_grid", "mapped", 1.0, "Table → looker_grid", "looker_grid"),
    "slicer": VisualMap("slicer", None, "mapped", 1.0, "Slicer → dashboard filter (not a tile)", "dashboard filter"),
    "textbox": VisualMap("textbox", "text", "partial", 0.6, "Text box → text tile (rich formatting limited)", "text"),
    "shape": VisualMap("shape", None, "skip", 0.0, "Decorative shape — no Looker equivalent (skip)", "skip"),
    "image": VisualMap("image", None, "gap", 0.2, "Image tile — not auto-ported; add manually or as text note", "manual"),
    "actionButton": VisualMap("actionButton", "button", "gap", 0.3, "Action button — Looker button needs explicit URL; stub as note", "button/gap"),
    "map": VisualMap("map", "looker_map", "partial", 0.5, "Map → looker_map if geo fields exist; else gap", "looker_map"),
    "filledMap": VisualMap("filledMap", "looker_google_map", "partial", 0.5, "Filled map → google map / choropleth if supported", "looker_google_map"),
    "treemap": VisualMap("treemap", "looker_pie", "partial", 0.5, "Treemap has no direct Looker twin → pie/column substitute", "looker_pie (substitute)"),
    "lineStackedColumnComboChart": VisualMap(
        "lineStackedColumnComboChart",
        "looker_column",
        "partial",
        0.55,
        "Combo chart → looker_column or looker_line (combo not 1:1)",
        "looker_column (partial)",
    ),
    "waterfallChart": VisualMap("waterfallChart", "looker_waterfall", "mapped", 1.0, "Waterfall → looker_waterfall", "looker_waterfall"),
    "funnel": VisualMap("funnel", "looker_funnel", "mapped", 1.0, "Funnel → looker_funnel", "looker_funnel"),
    "scatterChart": VisualMap("scatterChart", "looker_scatter", "mapped", 1.0, "Scatter → looker_scatter", "looker_scatter"),
}


def map_visual_type(pbi_type: str) -> VisualMap:
    t = (pbi_type or "unknown").strip()
    if t in VISUAL_EQUIVALENCE:
        return VISUAL_EQUIVALENCE[t]
    return VisualMap(
        pbi_type=t,
        looker_type=None,
        status="gap",
        coverage_weight=0.0,
        notes=f"Unknown/unsupported visual type `{t}` — document as GAP",
        looker_object="gap",
    )


def equivalence_table() -> list[dict]:
    rows = []
    for m in VISUAL_EQUIVALENCE.values():
        rows.append(asdict(m))
    return rows
