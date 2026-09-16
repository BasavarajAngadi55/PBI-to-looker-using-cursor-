"""Deterministic Power BI → LookML naming helpers."""
from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^a-zA-Z0-9]+")
_MULTI_US = re.compile(r"_+")


def snake_case(name: str) -> str:
    s = str(name).strip()
    s = s.replace("%", "pct").replace("&", "and")
    # Preserve common BI acronyms before CamelCase splitting
    for token, repl in (
        ("YoY", "yoy"),
        ("YoY", "yoy"),
        ("SPLY", "sply"),
        ("QoQ", "qoq"),
        ("MoM", "mom"),
        ("YTD", "ytd"),
        ("MTD", "mtd"),
        ("QTD", "qtd"),
    ):
        s = re.sub(re.escape(token), repl, s, flags=re.IGNORECASE)
    # CamelCase / PascalCase → snake (TermDate → Term_Date) before lowercasing
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
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


def lookml_file_stem(view_name: str) -> str:
    return view_name


def quote_sql_ident(col: str) -> str:
    """BigQuery-safe column reference when names have spaces/specials."""
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", col or ""):
        return col
    return f"`{col}`"


def sql_table_placeholder(view_name: str, project: str = "YOUR_PROJECT", dataset: str = "YOUR_DATASET") -> str:
    return f"`{project}.{dataset}.{view_name}`"
