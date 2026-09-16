"""Safe loaders bound to the CURRENT PBIX workspace only."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import MAX_TOOL_CHARS, PHASE1, PHASE2, PHASE3, REPO_ROOT, VALIDATION


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"Failed to parse {path.name}: {e}"}


def _read_text(path: Path, limit: int = 8000) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > limit:
        return text[:limit] + f"\n... [truncated {len(text) - limit} chars]"
    return text


def truncate_payload(obj: Any, max_chars: int = MAX_TOOL_CHARS) -> Any:
    raw = json.dumps(obj, ensure_ascii=False, default=str)
    if len(raw) <= max_chars:
        return obj
    return {
        "truncated": True,
        "original_chars": len(raw),
        "preview": raw[:max_chars],
        "note": "Payload truncated for model context. Ask a more specific question.",
    }


def get_current_pbix_meta() -> dict:
    meta = _read_json(PHASE1 / "CURRENT_PBIX.json") or {}
    if not meta:
        meta = _read_json(PHASE1 / "inventory" / "CURRENT_PBIX.json") or {}
    return {
        "pbix_name": meta.get("pbix_name"),
        "pbix_path": meta.get("pbix_path"),
        "size_bytes": meta.get("size_bytes"),
        "exists": bool(meta.get("pbix_name")),
        "inventory_dir": str(PHASE1 / "inventory"),
    }


def load_phase1_inventory(name: str) -> Any:
    return _read_json(PHASE1 / "inventory" / name)


def load_phase2_json(name: str) -> Any:
    return _read_json(PHASE2 / name)


def load_phase3_inventory(name: str) -> Any:
    return _read_json(PHASE3 / "inventory" / name)


def load_phase3_json(name: str) -> Any:
    return _read_json(PHASE3 / name)


def load_validation_json(name: str) -> Any:
    return _read_json(VALIDATION / name)


def read_repo_text(rel_from_repo: str, limit: int = 6000) -> dict:
    path = REPO_ROOT / rel_from_repo
    text = _read_text(path, limit=limit)
    if text is None:
        return {"found": False, "path": rel_from_repo}
    return {"found": True, "path": rel_from_repo, "content": text}
