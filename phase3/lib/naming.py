"""Shared naming helpers for Phase 3 (aligned with Phase 2)."""
from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^a-zA-Z0-9]+")
_MULTI_US = re.compile(r"_+")


def snake_case(name: str) -> str:
    s = str(name).strip().replace("%", "pct").replace("&", "and")
    s = _NON_ALNUM.sub("_", s)
    s = _MULTI_US.sub("_", s).strip("_").lower()
    if not s:
        s = "unnamed"
    if s[0].isdigit():
        s = f"n_{s}"
    return s


def lookml_view_name(table_name: str) -> str:
    return snake_case(table_name)


def lookml_field_name(column_name: str) -> str:
    return snake_case(column_name)


def lookml_field_ref(table: str, field: str, measure_host_view: str | None = None) -> str:
    """Build explore field ref view.field. Measure Table maps onto fact host view."""
    t = table or ""
    if t.lower().replace(" ", "") in {"measuretable", "measures"} and measure_host_view:
        view = measure_host_view
    else:
        view = lookml_view_name(t)
    return f"{view}.{lookml_field_name(field)}"
