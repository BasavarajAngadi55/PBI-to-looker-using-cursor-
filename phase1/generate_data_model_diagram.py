#!/usr/bin/env python3
"""Generate a clear full data-model diagram for ANY PBIX (business + internal)."""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
INV = ROOT / "inventory"
PDF_OUT = ROOT / "DATA_MODEL.pdf"
PNG_OUT = ROOT / "DATA_MODEL.png"
ER_PNG_OUT = ROOT / "DATA_MODEL_ER.png"
MD_OUT = ROOT / "DATA_MODEL.md"

a1: dict = {}
a2: dict = {}
a3: dict = {}
a5: dict = {}

BG = (248, 250, 252)
INK = (20, 30, 45)
MUTED = (90, 105, 125)
FACT = (20, 90, 140)
DIM = (25, 120, 100)
BRIDGE = (90, 70, 140)
INTERNAL = (140, 70, 90)
LINE = (70, 95, 120)
CARD_BG = (255, 255, 255)
NOTE_BG = (255, 248, 235)
NOTE_BD = (200, 140, 50)
ROW_ALT = (240, 245, 250)
INACTIVE = (160, 90, 90)


def load_inventory() -> None:
    global a1, a2, a3, a5
    a1 = json.loads((INV / "01_tables_columns.json").read_text())
    a2 = json.loads((INV / "03_relationships.json").read_text())
    a3 = json.loads((INV / "02_dax_objects.json").read_text())
    a5 = json.loads((INV / "05_tmschema_extras.json").read_text())


def source_pbix_name() -> str:
    try:
        meta = json.loads((INV / "OBJECT_COUNTS.json").read_text())
        return Path(meta.get("source_pbix") or "PBIX").name
    except Exception:
        return "PBIX"


def latin1(s: str) -> str:
    return (
        str(s)
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2192", "->")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def is_internal(n: str) -> bool:
    return n.startswith("LocalDateTable_") or n.startswith("DateTableTemplate_")


def font(size: int, bold: bool = False):
    path = "/System/Library/Fonts/Helvetica.ttc"
    try:
        return ImageFont.truetype(path, size, index=1 if bold else 0)
    except Exception:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()


def text_w(draw: ImageDraw.ImageDraw, text: str, fnt) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def cols_for(table: str) -> list[dict]:
    return [c for c in a1["columns"] if c["table_name"] == table]


def short_guid(name: str) -> str:
    if name.startswith("LocalDateTable_"):
        return "LocalDateTable_" + name.split("_", 1)[1][:8] + "..."
    if name.startswith("DateTableTemplate_"):
        return "DateTableTemplate_" + name.split("_", 1)[1][:8] + "..."
    return name


def internal_usage() -> dict[str, str]:
    out: dict[str, str] = {}
    for t in a3.get("calculated_tables", []):
        name = t["table_name"]
        expr = t.get("expression") or ""
        m = re.search(r"'([^']+)'\[([^\]]+)\]", expr)
        if m:
            out[name] = f"{m.group(1)}[{m.group(2)}]"
        elif "DateTableTemplate" in name:
            out[name] = "PBI auto-date TEMPLATE (not tied to a business column)"
        else:
            out[name] = "auto-date calendar"
    return out


def pk_guess(table: str) -> set[str]:
    pks: set[str] = set()
    for c in cols_for(table):
        if c.get("is_key"):
            pks.add(c["column_name"])
    for r in a2.get("relationships", []):
        if r.get("to_table") == table:
            pks.add(r["to_column"])
    return pks


def fk_guess(table: str) -> set[str]:
    return {r["from_column"] for r in a2.get("relationships", []) if r.get("from_table") == table}


def business_names() -> list[str]:
    return [t["table_name"] for t in a1["tables"] if not is_internal(t["table_name"])]


def classify_roles() -> dict[str, str]:
    """fact / bridge / dim for coloring only."""
    biz = set(business_names())
    rels = [r for r in a2.get("relationships", []) if r.get("from_table") in biz and r.get("to_table") in biz]
    from_c = Counter(r["from_table"] for r in rels)
    to_c = Counter(r["to_table"] for r in rels)
    roles: dict[str, str] = {}
    for t in biz:
        fout, tin = from_c.get(t, 0), to_c.get(t, 0)
        if fout >= 2 and tin >= 1:
            roles[t] = "bridge"
        elif fout >= tin and fout > 0:
            roles[t] = "fact"
        elif tin > 0:
            roles[t] = "dim"
        else:
            roles[t] = "other"
    return roles


def accent_for(role: str) -> tuple[int, int, int]:
    return {"fact": FACT, "bridge": BRIDGE, "dim": DIM}.get(role, (80, 90, 120))


def layout_layers(biz: list[str], rels: list[dict]) -> list[list[str]]:
    """
    Layer tables left→right by dependency depth.
    Pure dimensions (only referenced) on the left; highly connected / from-side on the right.
    """
    biz_set = set(biz)
    children: dict[str, set[str]] = defaultdict(set)  # to -> from (many side points at one)
    parents: dict[str, set[str]] = defaultdict(set)  # from -> to
    for r in rels:
        f, t = r["from_table"], r["to_table"]
        if f in biz_set and t in biz_set:
            parents[f].add(t)
            children[t].add(f)

    # depth = longest path from a root dim (no outgoing to another business table that isn't cyclic)
    # Use: tables with zero parents (never on from side) = depth 0... actually pure dims are only on to side
    only_to = [t for t in biz if t not in parents and t in children]
    only_from = [t for t in biz if t in parents and t not in children]
    both = [t for t in biz if t in parents and t in children]
    isolated = [t for t in biz if t not in parents and t not in children]

    # BFS depth from pure dims along reverse edges (dim -> bridge -> fact)
    depth: dict[str, int] = {t: 0 for t in only_to}
    q = deque(only_to)
    while q:
        cur = q.popleft()
        for nxt in children.get(cur, []):
            nd = depth[cur] + 1
            if nd > depth.get(nxt, -1):
                depth[nxt] = nd
                q.append(nxt)

    for t in both + only_from:
        if t not in depth:
            depth[t] = max((depth.get(p, 0) + 1 for p in parents.get(t, [])), default=1)
    for t in isolated:
        depth[t] = 0

    max_d = max(depth.values(), default=0)
    layers: list[list[str]] = [[] for _ in range(max_d + 1)]
    for t, d in sorted(depth.items(), key=lambda x: (x[1], x[0])):
        layers[d].append(t)
    # drop empty
    layers = [layer for layer in layers if layer]
    if not layers:
        layers = [sorted(biz)]
    return layers


def draw_rounded_label(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    accent: tuple[int, int, int],
    pad_x: int = 14,
    pad_y: int = 10,
) -> tuple[int, int, int, int]:
    fnt = font(13, True)
    tw = text_w(draw, text, fnt)
    w = tw + pad_x * 2
    h = 28 + pad_y
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=CARD_BG, outline=accent, width=2)
    draw.rectangle((x, y, x + 6, y + h), fill=accent)
    draw.text((x + pad_x, y + (h - 16) // 2), text, fill=INK, font=fnt)
    return (x, y, x + w, y + h)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    p1: tuple[int, int],
    p2: tuple[int, int],
    color: tuple[int, int, int],
    width: int = 2,
) -> None:
    draw.line([p1, p2], fill=color, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    size = 8
    for da in (0.4, -0.4):
        ax = p2[0] - size * math.cos(ang + da)
        ay = p2[1] - size * math.sin(ang + da)
        draw.line([p2, (ax, ay)], fill=color, width=width)


def draw_table_card(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    title: str,
    subtitle: str,
    columns: list[dict],
    accent: tuple[int, int, int],
    pk_names: set[str] | None = None,
    fk_names: set[str] | None = None,
    max_cols: int | None = None,
) -> int:
    pk_names = pk_names or set()
    fk_names = fk_names or set()
    show = columns if max_cols is None else columns[:max_cols]
    truncated = len(columns) - len(show)
    header_h = 40
    row_h = 16
    pad = 8
    extra = 16 if truncated > 0 else 0
    body_h = max(len(show), 1) * row_h + pad + extra
    h = header_h + body_h + 6

    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=CARD_BG, outline=accent, width=2)
    draw.rounded_rectangle((x, y, x + w, y + header_h), radius=8, fill=accent, outline=accent, width=2)
    draw.rectangle((x, y + header_h - 8, x + w, y + header_h), fill=accent)
    draw.text((x + 10, y + 5), title[:42], fill=(255, 255, 255), font=font(13, True))
    draw.text((x + 10, y + 22), subtitle[:55], fill=(220, 235, 245), font=font(10))

    yy = y + header_h + 5
    for c in show:
        cn = c["column_name"]
        marks = []
        if cn in pk_names or c.get("is_key"):
            marks.append("PK")
        if cn in fk_names:
            marks.append("FK")
        if c.get("is_calculated_column"):
            marks.append("CALC")
        mark = f" [{','.join(marks)}]" if marks else ""
        dtype = str(c.get("pandas_dtype") or c.get("data_type") or "")
        dtype = dtype.replace("datetime64[ns]", "datetime").replace("string", "text")
        draw.text((x + 10, yy), f"{cn}{mark}"[:36], fill=INK, font=font(10))
        draw.text((x + w - 72, yy), dtype[:11], fill=MUTED, font=font(9))
        yy += row_h
    if truncated > 0:
        draw.text((x + 10, yy), f"... +{truncated} more", fill=MUTED, font=font(10))
    return y + h


def relationship_chains(biz: list[str], rels: list[dict]) -> list[list[str]]:
    """
    Build readable left→right chains for the schema map.
    Each chain is a path of table names; overlapping tables may appear in multiple chains.
    """
    biz_set = set(biz)
    # adjacency: many(from) -> one(to)
    edges = [(r["from_table"], r["to_table"], r) for r in rels if r["from_table"] in biz_set and r["to_table"] in biz_set]
    # Find connected components (undirected)
    und: dict[str, set[str]] = defaultdict(set)
    for f, t, _ in edges:
        und[f].add(t)
        und[t].add(f)
        und[f].add(f)
        und[t].add(t)
    seen: set[str] = set()
    components: list[list[str]] = []
    for n in biz:
        if n in seen or n not in und:
            continue
        comp: list[str] = []
        q = deque([n])
        seen.add(n)
        while q:
            cur = q.popleft()
            comp.append(cur)
            for nxt in und[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        components.append(sorted(comp))
    for n in biz:
        if n not in seen:
            components.append([n])
    return components

def chain_layers_for_component(nodes: list[str], rels: list[dict]) -> list[list[str]]:
    return layout_layers(nodes, [r for r in rels if r["from_table"] in nodes and r["to_table"] in nodes])


def er_key_columns(table: str) -> list[tuple[str, str]]:
    """Ordered key rows for ER entity: (column_name, PK|FK|PK/FK)."""
    pks, fks = pk_guess(table), fk_guess(table)
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for cn in sorted(pks):
        tag = "PK/FK" if cn in fks else "PK"
        rows.append((cn, tag))
        seen.add(cn)
    for cn in sorted(fks):
        if cn in seen:
            continue
        rows.append((cn, "FK"))
        seen.add(cn)
    if not rows:
        for c in cols_for(table)[:4]:
            rows.append((c["column_name"], ""))
    return rows


def er_entity_size(table: str, min_w: int = 200, large: bool = False) -> tuple[int, int]:
    keys = er_key_columns(table)
    header_h = 36 if large else 28
    row_h = 20 if large else 16
    h = header_h + 10 + max(len(keys), 1) * row_h + 10
    longest = max([len(table)] + [len(k[0]) + 10 for k in keys], default=10)
    base = 14 if large else 12
    w = max(min_w if not large else 260, min(320 if large else 260, base * longest + 36))
    return w, h


def draw_er_entity(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    table: str,
    accent: tuple[int, int, int],
    large: bool = False,
) -> tuple[int, int, int, int]:
    w, h = er_entity_size(table, large=large)
    keys = er_key_columns(table)
    header_h = 36 if large else 28
    title_font = font(16, True) if large else font(12, True)
    key_font = font(13) if large else font(10)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=CARD_BG, outline=accent, width=3 if large else 2)
    draw.rounded_rectangle((x, y, x + w, y + header_h), radius=8, fill=accent, outline=accent, width=3 if large else 2)
    draw.rectangle((x, y + header_h - 10, x + w, y + header_h), fill=accent)
    draw.text((x + 12, y + 8), table[:30], fill=(255, 255, 255), font=title_font)
    yy = y + header_h + 8
    for cn, tag in keys:
        label = f"{cn}" + (f"  <<{tag}>>" if tag else "")
        draw.text((x + 12, yy), label[:36], fill=INK, font=key_font)
        yy += 20 if large else 16
    return (x, y, x + w, y + h)


def curated_er_positions(biz: list[str]) -> dict[str, tuple[int, int]] | None:
    """
    Neat domain layout for the classic movie-rental / Sakila-style PBIX
    (table name `rentat` as in this model). Coordinates are top-left of each entity.
    """
    needed = {
        "actor",
        "film_actor",
        "film",
        "language",
        "film_category",
        "category",
        "film_text",
        "inventory",
        "rentat",
        "payment",
        "staff",
        "store",
        "customer",
        "address",
        "city",
        "country",
    }
    if set(biz) != needed:
        return None
    return {
        "actor": (70, 70),
        "film_actor": (320, 70),
        "film": (600, 50),
        "film_category": (920, 70),
        "category": (1220, 70),
        "language": (600, 280),
        "film_text": (920, 280),
        "inventory": (600, 480),
        "rentat": (920, 480),
        "payment": (1220, 480),
        "store": (1520, 280),
        "staff": (1520, 480),
        "country": (70, 740),
        "city": (320, 740),
        "address": (600, 740),
        "customer": (920, 740),
    }


def layered_er_positions(
    biz: list[str],
    rels: list[dict],
    origin: tuple[int, int] = (70, 70),
    large: bool = False,
) -> dict[str, tuple[int, int]]:
    """Generic neat left→right layered placement for any PBIX."""
    layers = layout_layers(biz, rels)
    parents: dict[str, set[str]] = defaultdict(set)
    children: dict[str, set[str]] = defaultdict(set)
    for r in rels:
        if r["from_table"] in biz and r["to_table"] in biz:
            parents[r["from_table"]].add(r["to_table"])
            children[r["to_table"]].add(r["from_table"])

    for _ in range(4):
        for li in range(1, len(layers)):
            prev = {n: i for i, n in enumerate(layers[li - 1])}

            def score(n: str, pref: dict[str, int] = prev) -> float:
                linked = [pref[p] for p in parents.get(n, []) if p in pref]
                linked += [pref[c] for c in children.get(n, []) if c in pref]
                return sum(linked) / len(linked) if linked else 0.0

            layers[li] = sorted(layers[li], key=score)

    ox, oy = origin
    gap_x = 380 if large else 300
    gap_y = 40 if large else 28
    pos: dict[str, tuple[int, int]] = {}
    for li, layer in enumerate(layers):
        x = ox + li * gap_x
        y = oy
        for name in layer:
            pos[name] = (x, y)
            _, h = er_entity_size(name, large=large)
            y += h + gap_y
    return pos


def box_port(box: tuple[int, int, int, int], toward: tuple[float, float]) -> tuple[int, int]:
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    tx, ty = toward
    dx, dy = tx - cx, ty - cy
    if abs(dx) >= abs(dy):
        return (x2, int(cy)) if dx >= 0 else (x1, int(cy))
    return (int(cx), y2) if dy >= 0 else (int(cx), y1)


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    p1: tuple[int, int],
    p2: tuple[int, int],
    color: tuple[int, int, int],
    width: int = 2,
    dash: int = 7,
    gap: int = 5,
) -> None:
    x1, y1 = p1
    x2, y2 = p2
    dist = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / dist, (y2 - y1) / dist
    t = 0.0
    while t < dist:
        t2 = min(t + dash, dist)
        draw.line(
            [(int(x1 + ux * t), int(y1 + uy * t)), (int(x1 + ux * t2), int(y1 + uy * t2))],
            fill=color,
            width=width,
        )
        t = t2 + gap


def draw_cardinality_marker(
    draw: ImageDraw.ImageDraw,
    pt: tuple[int, int],
    other: tuple[int, int],
    symbol: str,
    color: tuple[int, int, int],
) -> None:
    ox = 1 if other[0] >= pt[0] else -1
    tx = pt[0] + ox * 12
    ty = pt[1] - 8
    draw.text((tx - 4, ty), symbol, fill=color, font=font(14, True))


def draw_er_diagram(
    draw: ImageDraw.ImageDraw,
    origin_y: int,
    canvas_w: int,
    biz_names: list[str],
    rels: list[dict],
    roles: dict[str, str],
    large: bool = False,
) -> int:
    """
    Neat ER diagram from exact inventory relationships.
    Power BI convention: From = Many (*), To = One (1).
    """
    title_y = origin_y
    title_f = font(28, True) if large else font(20, True)
    sub_f = font(16) if large else font(12)
    note_f = font(14) if large else font(11)
    label_f = font(13) if large else font(10)
    line_w = 3 if large else 2

    draw.text((70, title_y), "ER diagram (business tables)", fill=FACT, font=title_f)
    draw.text(
        (70, title_y + (34 if large else 28)),
        "Exact joins from the PBIX model.  * = many (FK side)   1 = one (lookup / PK side)   "
        "Dashed red = inactive relationship",
        fill=MUTED,
        font=sub_f,
    )

    curated = curated_er_positions(biz_names)
    if curated is not None:
        shift = title_y + (80 if large else 60)
        # scale curated coords when large
        scale = 1.25 if large else 1.0
        pos = {k: (int(x * scale) + 40, int(y * scale) + shift) for k, (x, y) in curated.items()}
        layout_note = "Layout: domain swimlanes (Film / Operations / Geography) - matches this PBIX"
    else:
        pos = layered_er_positions(biz_names, rels, origin=(70, title_y + (90 if large else 70)), large=large)
        layout_note = "Layout: dependency layers (lookup left -> FK / transactional right)"

    draw.text((70, title_y + (58 if large else 48)), layout_note, fill=MUTED, font=note_f)

    boxes: dict[str, tuple[int, int, int, int]] = {}
    for name, (x, y) in pos.items():
        w, h = er_entity_size(name, large=large)
        boxes[name] = (x, y, x + w, y + h)

    if boxes:
        min_x = min(b[0] for b in boxes.values()) - 24
        min_y = min(b[1] for b in boxes.values()) - 24
        max_x = max(max(b[2] for b in boxes.values()) + 24, min(canvas_w - 50, max(b[2] for b in boxes.values()) + 80))
        max_y = max(b[3] for b in boxes.values()) + 24
        draw.rounded_rectangle((min_x, min_y, max_x, max_y), radius=12, fill=(255, 255, 255), outline=LINE, width=2)

    expected = [r for r in rels if r["from_table"] in boxes and r["to_table"] in boxes]
    drawn = 0
    for idx, r in enumerate(rels):
        f, t = r["from_table"], r["to_table"]
        if f not in boxes or t not in boxes:
            continue
        a, b = boxes[f], boxes[t]
        ac = ((a[0] + a[2]) / 2, (a[1] + a[3]) / 2)
        bc = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        p1 = box_port(a, bc)
        p2 = box_port(b, ac)
        active = bool(r.get("active", True))
        color = LINE if active else INACTIVE
        mid_x = int((p1[0] + p2[0]) / 2) + ((idx % 7) - 3) * 8
        path = [p1, (mid_x, p1[1]), (mid_x, p2[1]), p2]
        if active:
            for i in range(len(path) - 1):
                draw.line([path[i], path[i + 1]], fill=color, width=line_w)
        else:
            for i in range(len(path) - 1):
                draw_dashed_line(draw, path[i], path[i + 1], color, width=line_w)
        draw_arrow(draw, path[-2], path[-1], color, line_w)
        draw_cardinality_marker(draw, p1, p2, "*", color)
        draw_cardinality_marker(draw, p2, p1, "1", color)
        fc, tc = r["from_column"], r["to_column"]
        label = fc if fc == tc else f"{fc}={tc}"
        if not active:
            label += " (inactive)"
        lw = text_w(draw, label, label_f)
        lx = mid_x - lw // 2
        ly = int((p1[1] + p2[1]) / 2) - 8
        draw.rectangle((lx - 4, ly - 2, lx + lw + 4, ly + 16), fill=(255, 255, 255))
        draw.text((lx, ly), label, fill=color, font=label_f)
        drawn += 1

    for name, (x, y, _, _) in boxes.items():
        draw_er_entity(draw, x, y, name, accent_for(roles.get(name, "other")), large=large)

    if curated is not None and boxes and "actor" in boxes:
        draw.text((70, boxes["actor"][1] - 22), "Film domain", fill=MUTED, font=note_f)
        if "inventory" in boxes:
            draw.text((70, boxes["inventory"][1] - 22), "Rental / operations", fill=MUTED, font=note_f)
        if "country" in boxes:
            draw.text((70, boxes["country"][1] - 22), "Geography / customer", fill=MUTED, font=note_f)

    footer_y = (max(b[3] for b in boxes.values()) + 24) if boxes else title_y + 80
    draw.text(
        (70, footer_y),
        f"ER accuracy: {drawn}/{len(expected)} model relationships drawn  |  "
        f"{len(biz_names)} business entities  |  From=Many (*), To=One (1)",
        fill=MUTED,
        font=note_f,
    )
    if drawn != len(expected):
        raise RuntimeError("ER diagram missed a business relationship — refusing inaccurate output")

    ly = footer_y + 32
    draw.text((70, ly), "Entity colors:", fill=INK, font=font(14, True) if large else font(12, True))
    for i, (label, color) in enumerate(
        [("Fact / FK-heavy", FACT), ("Bridge", BRIDGE), ("Dimension / lookup", DIM), ("Other", (80, 90, 120))]
    ):
        x = 220 + i * 280
        draw.rounded_rectangle((x, ly, x + 18, ly + 18), radius=3, fill=color)
        draw.text((x + 24, ly), label, fill=MUTED, font=note_f)
    return ly + 50


def render_er_only_image(biz_names: list[str], rels: list[dict], roles: dict[str, str]) -> Path:
    """Large, readable ER-only image for embedding in the PDF (no clipping of content)."""
    W = 2400
    H = 3200
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 24, W - 40, 110), radius=12, fill=(18, 36, 58), outline=FACT, width=2)
    d.text((70, 40), "ER diagram", fill=(90, 200, 220), font=font(18, True))
    d.text((70, 68), source_pbix_name(), fill=(255, 255, 255), font=font(24, True))

    bottom = draw_er_diagram(d, 130, W, biz_names, rels, roles, large=True)
    img = img.crop((0, 0, W, min(H, bottom + 40)))
    img.save(ER_PNG_OUT)
    print("Wrote", ER_PNG_OUT)
    return ER_PNG_OUT


def embed_image_fit_pages(pdf: FPDF, image_path: Path, title: str) -> None:
    """
    Embed an image on landscape pages.
    Prefer fitting the FULL image on one page (no crop). If too tall at readable width,
    paginate by height without overlapping/cutting mid-page black bars.
    """
    img = Image.open(image_path).convert("RGB")
    page_w, page_h = 297.0, 210.0
    margin = 10.0
    header = 8.0
    usable_w = page_w - 2 * margin
    usable_h = page_h - 2 * margin - header

    # Try full-fit on one page
    scale_fit = min(usable_w / img.width, usable_h / img.height)
    # If full-fit keeps image reasonably large (>= 55% of page width), use one page
    if scale_fit * img.width >= usable_w * 0.55:
        pdf.add_page(orientation="L")
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(20, 90, 140)
        pdf.set_xy(margin, 4)
        pdf.cell(0, 5, latin1(title))
        pdf.set_text_color(40, 40, 40)
        draw_w = img.width * scale_fit
        draw_h = img.height * scale_fit
        x = margin + (usable_w - draw_w) / 2
        y = margin + header + (usable_h - draw_h) / 2
        pdf.image(str(image_path), x=x, y=y, w=draw_w, h=draw_h)
        return

    # Multi-page: scale to full usable width, slice height (white background, no black bar)
    scale = usable_w / img.width
    slice_h_px = max(1, int(usable_h / scale))
    total = max(1, (img.height + slice_h_px - 1) // slice_h_px)
    tmp_dir = ROOT / ".dm_pdf_slices"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        for page_i, y0 in enumerate(range(0, img.height, slice_h_px)):
            y1 = min(img.height, y0 + slice_h_px)
            # pad slice to full page height with white so no black gaps
            slice_img = Image.new("RGB", (img.width, slice_h_px), (255, 255, 255))
            crop = img.crop((0, y0, img.width, y1))
            slice_img.paste(crop, (0, 0))
            slice_path = tmp_dir / f"er_{page_i:03d}.png"
            slice_img.save(slice_path, format="PNG")

            pdf.add_page(orientation="L")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(20, 90, 140)
            pdf.set_xy(margin, 4)
            pdf.cell(0, 5, latin1(f"{title}  |  page {page_i + 1}/{total}"))
            pdf.set_text_color(40, 40, 40)
            pdf.image(str(slice_path), x=margin, y=margin + header, w=usable_w, h=usable_h)
    finally:
        for p in tmp_dir.glob("er_*.png"):
            try:
                p.unlink()
            except OSError:
                pass
        try:
            tmp_dir.rmdir()
        except OSError:
            pass


def mermaid_er(rels: list[dict], biz: list[str]) -> str:
    """Mermaid erDiagram — many }o--|| one, matching Power BI From/To."""
    lines = ["```mermaid", "erDiagram"]
    biz_set = set(biz)
    for r in rels:
        if r["from_table"] not in biz_set or r["to_table"] not in biz_set:
            continue
        label = r["from_column"] if r["from_column"] == r["to_column"] else f"{r['from_column']} to {r['to_column']}"
        if not r.get("active", True):
            label += " inactive"
        # sanitize for mermaid
        label = label.replace('"', "")
        lines.append(
            f'    {r["from_table"]} }}o--|| {r["to_table"]} : "{label}"'
        )
    lines.append("```")
    return "\n".join(lines)


def make_png() -> None:
    usage = internal_usage()
    pbix_name = source_pbix_name()
    biz_names = business_names()
    int_names = [t["table_name"] for t in a1["tables"] if is_internal(t["table_name"])]
    roles = classify_roles()
    rels = list(a2.get("relationships", []))
    rels_sorted = sorted(
        rels, key=lambda r: (not r.get("active", True), r["from_table"], r["to_table"], r["from_column"])
    )

    W = 2600
    H = 12000
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((40, 24, W - 40, 130), radius=12, fill=(18, 36, 58), outline=FACT, width=2)
    d.text((70, 40), "Power BI Data Model", fill=(90, 200, 220), font=font(15, True))
    d.text((70, 64), pbix_name, fill=(255, 255, 255), font=font(26, True))
    d.text(
        (70, 100),
        f"Business tables: {len(biz_names)}   |   Relationships: {len(rels)}   |   "
        f"Internal auto-date: {len(int_names)}   |   ER first, then relationship flow",
        fill=(180, 200, 220),
        font=font(13),
    )

    y = 150
    y = draw_er_diagram(d, y, W, biz_names, rels_sorted, roles)
    y += 20

    d.rounded_rectangle((60, y, W - 60, y + 110), radius=10, fill=NOTE_BG, outline=NOTE_BD, width=2)
    d.text((80, y + 10), "How to read this document", fill=NOTE_BD, font=font(14, True))
    guide = [
        "1. ER diagram (above): visual model — boxes are tables; lines are joins from the PBIX.",
        "2. On each line: * sits on the many/FK table, 1 sits on the one/PK (lookup) table — same as Power BI Model view.",
        "3. Edge label is the join column (FK = PK). Red dashed = relationship exists but IsActive=false.",
        "4. Sections below list the same joins as a checklist (flow / join map) so you can validate every relationship.",
        "5. Column catalog lists all fields with PK/FK marks. Internal LocalDateTable_* are auto-date helpers, not business joins.",
    ]
    for i, line in enumerate(guide):
        d.text((80, y + 34 + i * 14), line, fill=INK, font=font(11))
    y += 130

    d.text((70, y), "1) Relationship flow — every join (validation checklist)", fill=FACT, font=font(18, True))
    y += 32

    row_h = 52
    left_margin = 60
    box_w = W - 120
    d.rounded_rectangle((left_margin, y, left_margin + box_w, y + 34), radius=6, fill=(230, 236, 244), outline=LINE)
    d.text((left_margin + 16, y + 8), "#", fill=MUTED, font=font(12, True))
    d.text((left_margin + 50, y + 8), "Many side (from / FK)", fill=MUTED, font=font(12, True))
    d.text((left_margin + 520, y + 8), "Join columns", fill=MUTED, font=font(12, True))
    d.text((left_margin + 900, y + 8), "One side (to / PK)", fill=MUTED, font=font(12, True))
    d.text((left_margin + 1400, y + 8), "Card / Filter / Active", fill=MUTED, font=font(12, True))
    y += 40

    if not rels_sorted:
        d.text((left_margin + 16, y), "No relationships in this PBIX.", fill=INK, font=font(13))
        y += 40

    for i, r in enumerate(rels_sorted, 1):
        active = bool(r.get("active", True))
        fill = CARD_BG if i % 2 else ROW_ALT
        border = LINE if active else INACTIVE
        d.rounded_rectangle(
            (left_margin, y, left_margin + box_w, y + row_h - 6),
            radius=8,
            fill=fill,
            outline=border,
            width=2 if not active else 1,
        )
        from_t, to_t = r["from_table"], r["to_table"]
        fc, tc = r["from_column"], r["to_column"]
        d.text((left_margin + 16, y + 14), str(i), fill=MUTED, font=font(14, True))
        fb = draw_rounded_label(d, left_margin + 50, y + 8, from_t, accent_for(roles.get(from_t, "other")))
        mid_x = left_margin + 520
        d.text((mid_x, y + 8), f"{fc}  ->  {tc}", fill=INK, font=font(13, True))
        d.text((mid_x, y + 28), "FK                    PK", fill=MUTED, font=font(10))
        ax1 = fb[2] + 12
        if mid_x - 16 > ax1:
            draw_arrow(d, (ax1, y + 22), (min(mid_x - 16, ax1 + 90), y + 22), LINE if active else INACTIVE, 2)
        draw_rounded_label(d, left_margin + 900, y + 8, to_t, accent_for(roles.get(to_t, "other")))
        meta = (
            f"{r.get('cardinality', '?')}   |   filter: {r.get('cross_filter', '?')}   |   "
            f"{'ACTIVE' if active else 'INACTIVE'}"
        )
        d.text((left_margin + 1400, y + 16), meta, fill=INK if active else INACTIVE, font=font(12, True))
        y += row_h

    y += 28

    d.text((70, y), "2) Join map (one line per relationship)", fill=FACT, font=font(18, True))
    y += 28
    d.text(
        (70, y),
        "Same joins as the ER and section 1 — strip form, no overlapping lines.",
        fill=MUTED,
        font=font(12),
    )
    y += 28

    strip_h = 44
    for i, r in enumerate(rels_sorted, 1):
        active = bool(r.get("active", True))
        color = LINE if active else INACTIVE
        d.rounded_rectangle(
            (60, y, W - 60, y + strip_h - 4),
            radius=8,
            fill=CARD_BG,
            outline=color if not active else (220, 226, 232),
        )
        d.text((76, y + 12), f"{i:>2}", fill=MUTED, font=font(13, True))
        left = draw_rounded_label(d, 120, y + 6, r["from_table"], accent_for(roles.get(r["from_table"], "other")))
        badge = f"  {r['from_column']}  ->  {r['to_column']}  ({r.get('cardinality')})  "
        bw = text_w(d, badge, font(12, True)) + 20
        bx, by = 520, y + 8
        d.rounded_rectangle((bx, by, bx + bw, by + 28), radius=14, fill=(235, 242, 248), outline=color, width=2)
        d.text((bx + 10, by + 6), badge, fill=INK if active else INACTIVE, font=font(12, True))
        draw_arrow(d, (left[2] + 6, y + 20), (bx - 4, y + 20), color, 2)
        right_x = bx + bw + 16
        rb = draw_rounded_label(d, right_x, y + 6, r["to_table"], accent_for(roles.get(r["to_table"], "other")))
        draw_arrow(d, (bx + bw + 2, y + 20), (rb[0] - 4, y + 20), color, 2)
        status = "ACTIVE" if active else "INACTIVE"
        d.text(
            (rb[2] + 20, y + 14),
            f"{status}  |  filter: {r.get('cross_filter')}",
            fill=MUTED if active else INACTIVE,
            font=font(11),
        )
        y += strip_h

    y += 24

    comps = relationship_chains(biz_names, rels)
    d.text((70, y), "3) Connected groups (schema layers)", fill=FACT, font=font(18, True))
    y += 28
    d.text(
        (70, y),
        "Tables grouped by connectivity. Left = lookup, right = FK / transactional side.",
        fill=MUTED,
        font=font(12),
    )
    y += 28

    for ci, nodes in enumerate(comps, 1):
        sub_rels = [r for r in rels_sorted if r["from_table"] in nodes and r["to_table"] in nodes]
        layers = chain_layers_for_component(nodes, sub_rels)
        layer_gap_x = min(320, max(200, (W - 160) // max(len(layers), 1)))
        node_gap_y = 52
        max_layer_n = max((len(L) for L in layers), default=1)
        map_h = max(max_layer_n * node_gap_y + 50, 90)

        d.rounded_rectangle((50, y, W - 50, y + map_h + 36), radius=10, fill=(255, 255, 255), outline=LINE)
        d.text(
            (70, y + 8),
            f"Group {ci}  ({len(nodes)} tables, {len(sub_rels)} relationships)",
            fill=MUTED,
            font=font(12, True),
        )
        map_top = y + 30
        node_boxes: dict[str, tuple[int, int, int, int]] = {}
        start_x = 80
        for li, layer in enumerate(layers):
            x = start_x + li * layer_gap_x
            total_h = len(layer) * node_gap_y
            y0 = map_top + max(0, (map_h - 20 - total_h) // 2)
            for ti, name in enumerate(layer):
                ny = y0 + ti * node_gap_y
                tw = text_w(d, name, font(13, True)) + 28
                node_boxes[name] = (x, ny, x + max(140, tw), ny + 34)

        for idx, r in enumerate(sub_rels):
            f, t = r["from_table"], r["to_table"]
            if f not in node_boxes or t not in node_boxes:
                continue
            a, b = node_boxes[f], node_boxes[t]
            if a[0] >= b[0]:
                p1 = (a[0], (a[1] + a[3]) // 2)
                p2 = (b[2], (b[1] + b[3]) // 2)
            else:
                p1 = (a[2], (a[1] + a[3]) // 2)
                p2 = (b[0], (b[1] + b[3]) // 2)
            color = LINE if r.get("active", True) else INACTIVE
            mid_x = (p1[0] + p2[0]) // 2 + ((idx % 5) - 2) * 8
            d.line([p1, (mid_x, p1[1]), (mid_x, p2[1]), p2], fill=color, width=2)
            label = r["from_column"]
            lw = text_w(d, label, font(9))
            d.rectangle(
                (
                    mid_x - lw // 2 - 3,
                    (p1[1] + p2[1]) // 2 - 7,
                    mid_x + lw // 2 + 3,
                    (p1[1] + p2[1]) // 2 + 7,
                ),
                fill=(255, 255, 255),
            )
            d.text((mid_x - lw // 2, (p1[1] + p2[1]) // 2 - 6), label, fill=MUTED, font=font(9))
            draw_arrow(d, (mid_x, p2[1]), p2, color, 2)

        for name, box in node_boxes.items():
            draw_rounded_label(d, box[0], box[1], name, accent_for(roles.get(name, "other")))
        y += map_h + 50

    d.text((70, y), "4) Business tables — columns (PK / FK marked)", fill=FACT, font=font(18, True))
    y += 30

    card_w, gap, cols_per_row = 360, 18, 5
    order_rank = {"dim": 0, "other": 1, "bridge": 2, "fact": 3}
    ordered = sorted(biz_names, key=lambda n: (order_rank.get(roles.get(n, "other"), 9), n))

    i = 0
    while i < len(ordered):
        chunk = ordered[i : i + cols_per_row]
        x = 60
        row_bottom = y
        for name in chunk:
            bottom = draw_table_card(
                d,
                x,
                y,
                card_w,
                name,
                f"{roles.get(name, 'table').upper()}  |  {len(cols_for(name))} cols",
                cols_for(name),
                accent_for(roles.get(name, "other")),
                pk_guess(name),
                fk_guess(name),
                max_cols=14,
            )
            row_bottom = max(row_bottom, bottom)
            x += card_w + gap
        y = row_bottom + gap
        i += cols_per_row

    y += 20
    d.text((70, y), "5) Internal auto-date tables (not in business joins)", fill=INTERNAL, font=font(18, True))
    y += 28
    note = (
        "LocalDateTable_* / DateTableTemplate_* support Power BI date hierarchies. "
        "Listed for completeness; business relationships above do not use them."
    )
    d.rounded_rectangle((60, y, W - 60, y + 52), radius=8, fill=NOTE_BG, outline=NOTE_BD, width=2)
    d.text((80, y + 8), "NOTE", fill=NOTE_BD, font=font(12, True))
    d.text((80, y + 28), note[:160], fill=INK, font=font(11))
    y += 70

    if not int_names:
        d.text((70, y), "None in this PBIX.", fill=MUTED, font=font(12))
        y += 24
    else:
        d.rounded_rectangle((60, y, W - 60, y + 28 + 18 * len(int_names)), radius=8, fill=CARD_BG, outline=INTERNAL)
        d.text((80, y + 6), "Internal table", fill=MUTED, font=font(11, True))
        d.text((900, y + 6), "Used for (calendar source)", fill=MUTED, font=font(11, True))
        yy = y + 28
        for name in int_names:
            d.text((80, yy), short_guid(name), fill=INTERNAL, font=font(11))
            d.text((900, yy), usage.get(name, "-")[:80], fill=INK, font=font(11))
            yy += 18
        y = yy + 16

    d.text(
        (70, y + 6),
        f"Content source: Phase 1 extract of {pbix_name}  |  "
        f"{len(biz_names)} business + {len(int_names)} internal  |  {len(rels)} relationships",
        fill=MUTED,
        font=font(12),
    )
    img = img.crop((0, 0, W, y + 40))
    img.save(PNG_OUT)
    print("Wrote", PNG_OUT)


def make_pdf() -> None:
    """
    Primary deliverable: readable PDF with large type and proper page breaks.
    No PNG slicing (that shrank/cut text). Zoom works cleanly on native PDF text.
    """
    usage = internal_usage()
    pbix_name = source_pbix_name()
    roles = classify_roles()
    biz_names = business_names()
    int_names = [t["table_name"] for t in a1["tables"] if is_internal(t["table_name"])]
    rels = sorted(
        a2.get("relationships", []),
        key=lambda r: (not r.get("active", True), r["from_table"], r["to_table"], r["from_column"]),
    )

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, 14)
    margin = 12
    content_w = 210 - 2 * margin
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)

    def ensure_space(needed_mm: float) -> None:
        if pdf.get_y() + needed_mm > 297 - 16:
            pdf.add_page()

    # ---- Cover ----
    pdf.add_page()
    content_w = 210 - 2 * margin
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 20)
    pdf.multi_cell(content_w, 10, latin1("Power BI Data Model"))
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(20, 90, 140)
    pdf.multi_cell(content_w, 8, latin1(pbix_name))
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(
        content_w,
        7,
        latin1(
            f"Business tables: {len(biz_names)}   |   Relationships: {len(rels)}   |   "
            f"Internal auto-date: {len(int_names)}"
        ),
    )
    pdf.ln(3)
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(content_w, 8, "How to read", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for line in [
        "1. Next page(s): visual ER diagram (tables + join lines). Zoom in your PDF reader.",
        "2. * = many / FK side (Power BI From).  1 = one / PK side (To).",
        "3. After the ER diagram: every relationship printed in full (nothing clipped).",
        "4. Later pages list every business column (PK/FK marked) and internal date tables.",
    ]:
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, latin1(line))

    # ---- Visual ER diagram (restored) ----
    er_path = render_er_only_image(biz_names, rels, roles)
    embed_image_fit_pages(pdf, er_path, f"ER diagram - {pbix_name}")

    # ---- ER / relationships (large readable blocks) ----
    pdf.add_page(orientation="P")
    pdf.set_auto_page_break(True, 14)
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(content_w, 9, latin1(f"ER relationships checklist ({len(rels)})"))
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(90, 105, 125)
    pdf.multi_cell(content_w, 6, latin1("Many side (FK)  ->  One side (PK)   |   Card / Filter / Active"))
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)

    if not rels:
        pdf.set_x(margin)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(content_w, 7, "No relationships in this PBIX.")
    for i, r in enumerate(rels, 1):
        active = bool(r.get("active", True))
        ensure_space(30)
        if not active:
            pdf.set_draw_color(160, 90, 90)
            pdf.set_text_color(160, 90, 90)
        else:
            pdf.set_draw_color(120, 140, 160)
            pdf.set_text_color(20, 90, 140)
        pdf.set_line_width(0.5)
        y0 = pdf.get_y()
        pdf.set_xy(margin + 2, y0 + 2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(
            content_w - 4,
            7,
            latin1(
                f"{i}.  {r['from_table']}.{r['from_column']}  ->  {r['to_table']}.{r['to_column']}"
            ),
        )
        pdf.set_text_color(40, 40, 40)
        pdf.set_x(margin + 2)
        pdf.set_font("Helvetica", "", 11)
        status = "ACTIVE" if active else "INACTIVE"
        pdf.multi_cell(
            content_w - 4,
            6,
            latin1(
                f"[*] many = {r['from_table']}     [1] one = {r['to_table']}     |     "
                f"{r.get('cardinality')}     |     filter: {r.get('cross_filter')}     |     {status}"
            ),
        )
        y1 = pdf.get_y() + 2
        pdf.rect(margin, y0, content_w, max(22, y1 - y0))
        pdf.set_y(y1 + 3)

    # Schema layers
    ensure_space(30)
    pdf.ln(2)
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(content_w, 8, "Schema layers (left = lookup, right = FK side)")
    pdf.set_font("Helvetica", "", 11)
    layers = layout_layers(biz_names, rels)
    for li, layer in enumerate(layers):
        labeled = ", ".join(f"{n} ({roles.get(n, '?')})" for n in layer)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, latin1(f"Layer {li}: {labeled}"))

    # ---- Business tables ----
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(content_w, 9, "Business tables (all columns)")
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(content_w, 6, latin1("PK / FK marks come from model relationships and key flags."))
    pdf.ln(1)

    for t in a1["tables"]:
        name = t["table_name"]
        if is_internal(name):
            continue
        cols = cols_for(name)
        pks, fks = pk_guess(name), fk_guess(name)
        ensure_space(18)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(20, 90, 140)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 7, latin1(f"{name}   ({roles.get(name, 'table')}, {len(cols)} cols)"))
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "", 11)
        for c in cols:
            flags = []
            cn = c["column_name"]
            if cn in pks or c.get("is_key"):
                flags.append("PK")
            if cn in fks:
                flags.append("FK")
            if c.get("is_calculated_column"):
                flags.append("CALC")
            fl = f"  [{','.join(flags)}]" if flags else ""
            dtype = str(c.get("pandas_dtype") or c.get("data_type") or "")
            ensure_space(7)
            pdf.set_x(margin + 2)
            pdf.multi_cell(content_w - 2, 6, latin1(f"- {cn}{fl}   ({dtype})"))
        pdf.ln(2)

    # ---- Internal ----
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(140, 70, 90)
    pdf.multi_cell(content_w, 9, "Internal auto-date tables")
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        content_w,
        6,
        latin1(
            "LocalDateTable_* / DateTableTemplate_* support Power BI date hierarchies. "
            "Listed for completeness; business relationships above do not use them."
        ),
    )
    pdf.ln(2)
    if not int_names:
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 7, "None in this PBIX.")
    for name in int_names:
        used = usage.get(name, "-")
        ensure_space(20)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(140, 70, 90)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, latin1(short_guid(name)))
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, latin1(f"Full name: {name}"))
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, latin1(f"Used for: {used}"))
        pdf.ln(2)

    pdf.output(str(PDF_OUT))
    print("Wrote", PDF_OUT)


def build_markdown() -> str:
    usage = internal_usage()
    pbix_name = source_pbix_name()
    roles = classify_roles()
    biz = [t for t in a1["tables"] if not is_internal(t["table_name"])]
    biz_names = [t["table_name"] for t in biz]
    internal = [t for t in a1["tables"] if is_internal(t["table_name"])]
    rels = sorted(
        a2.get("relationships", []),
        key=lambda r: (not r.get("active", True), r["from_table"], r["to_table"], r["from_column"]),
    )

    lines = [
        f"# Power BI Data Model — {pbix_name}",
        "",
        "Content matches the PBIX model (verified against pbixray relationships).",
        "",
        "## Summary",
        "",
        f"- Source PBIX: `{pbix_name}`",
        f"- Business tables: **{len(biz)}**",
        f"- Internal auto-date tables: **{len(internal)}**",
        f"- Relationships: **{len(rels)}**",
        "",
        "## ER diagram",
        "",
        "Visual ER diagram is embedded in **`DATA_MODEL.pdf`** (download and zoom). "
        "Mermaid below uses the same joins (`}o--||` = many-to-one, Power BI From→To).",
        "",
        mermaid_er(rels, biz_names),
        "",
        "## How to read",
        "",
        "1. **ER first** — boxes = tables; lines = PBIX relationships. Prefer **`DATA_MODEL.pdf`** (download and zoom).",
        "2. **`*`** = many / FK side (Power BI *FromTable*). **`1`** = one / PK side (*ToTable*).",
        "3. Edge label = join column(s). **Inactive** = `IsActive=false` in the model.",
        "4. Checklist sections below repeat the same joins for validation.",
        "5. Column catalog marks PK/FK. `LocalDateTable_*` are auto-date helpers, not business joins.",
        "",
        "## 1) Relationship flow",
        "",
        "| # | Many side | FK | → | One side | PK | Card | Filter | Active |",
        "|---|-----------|----|---|----------|----|------|--------|--------|",
    ]
    for i, r in enumerate(rels, 1):
        lines.append(
            f"| {i} | `{r['from_table']}` | `{r['from_column']}` | → | `{r['to_table']}` | "
            f"`{r['to_column']}` | {r.get('cardinality')} | {r.get('cross_filter')} | {r.get('active')} |"
        )
    if not rels:
        lines.append("| — | — | — | — | — | — | — | — | — |")

    lines += ["", "### Flow (plain text)", "", "```"]
    for i, r in enumerate(rels, 1):
        act = "ACTIVE" if r.get("active") else "INACTIVE"
        lines.append(
            f"{i:>2}. {r['from_table']}.{r['from_column']}  -->  {r['to_table']}.{r['to_column']}   "
            f"({r.get('cardinality')}, {r.get('cross_filter')}, {act})"
        )
    lines += ["```", ""]

    layers = layout_layers(biz_names, rels)
    lines += ["## 2) Schema layers (left → right)", ""]
    for i, layer in enumerate(layers):
        labeled = ", ".join(f"`{n}` ({roles.get(n, '?')})" for n in layer)
        lines.append(f"- **Layer {i}:** {labeled}")
    lines.append("")

    lines += [
        "## NOTE — Internal tables",
        "",
        "`LocalDateTable_*` / `DateTableTemplate_*` are Power BI auto date helpers. "
        "Usually **not** in business relationships.",
        "",
        "| Internal table | Used for |",
        "|----------------|----------|",
    ]
    if not internal:
        lines.append("| _(none)_ | — |")
    for t in internal:
        name = t["table_name"]
        lines.append(f"| `{name}` | `{usage.get(name, '-')}` |")

    lines += ["", "## 3) Business tables — columns", ""]
    for t in biz:
        name = t["table_name"]
        cols = cols_for(name)
        pks, fks = pk_guess(name), fk_guess(name)
        lines.append(f"### `{name}` ({roles.get(name, 'table')})")
        lines.append(f"- Columns: {len(cols)}")
        lines.append("")
        for c in cols:
            flags = []
            cn = c["column_name"]
            if cn in pks or c.get("is_key"):
                flags.append("PK")
            if cn in fks:
                flags.append("FK")
            if c.get("is_calculated_column"):
                flags.append("CALC")
            fl = f" _{','.join(flags)}_" if flags else ""
            lines.append(f"- `{cn}`{fl} — {c.get('pandas_dtype') or c.get('data_type')}")
        lines.append("")

    lines += ["", "## 4) Internal tables — columns", ""]
    if not internal:
        lines.append("_None in this PBIX._")
    for t in internal:
        name = t["table_name"]
        cols = cols_for(name)
        lines.append(f"### `{name}`")
        lines.append(f"- **Used for:** `{usage.get(name, '-')}`")
        lines.append("")
        for c in cols:
            fl = " _CALC_" if c.get("is_calculated_column") else ""
            lines.append(f"- `{c['column_name']}`{fl}")
        lines.append("")

    lines.append("See also: `DATA_MODEL.pdf` (primary — download and zoom).")
    return "\n".join(lines) + "\n"


def main() -> None:
    load_inventory()
    MD_OUT.write_text(build_markdown(), encoding="utf-8")
    print("Wrote", MD_OUT)
    make_png()
    make_pdf()


if __name__ == "__main__":
    main()
