"""QandA config — Ollama Gemma via ADK LiteLLM."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QANDA_ROOT = Path(__file__).resolve().parent

PHASE1 = REPO_ROOT / "phase1"
PHASE2 = REPO_ROOT / "phase2"
PHASE3 = REPO_ROOT / "phase3"
VALIDATION = REPO_ROOT / "validation"


def _ollama_tags() -> set[str]:
    try:
        out = subprocess.check_output(["ollama", "list"], text=True, timeout=10)
    except Exception:
        return set()
    names = set()
    for line in out.splitlines()[1:]:
        parts = line.split()
        if parts:
            names.add(parts[0])
    return names


def resolve_ollama_model() -> str:
    """Prefer env override, then newest Gemma available locally.

    Note: gemma3 via Ollama does not support native tool-calling; QandA uses
    grounded context (no LLM tools), so gemma3 is fine.
    """
    env = os.environ.get("QANDA_OLLAMA_MODEL", "").strip()
    if env:
        return env
    tags = _ollama_tags()
    for candidate in (
        "gemma3:latest",
        "gemma3:4b",
        "gemma3:12b",
        "gemma4:e2b",
        "gemma2:9b",
        "gemma2:2b",
        "gemma:2b",
    ):
        if candidate in tags:
            return candidate
    return "gemma3:latest"


OLLAMA_MODEL = resolve_ollama_model()
OLLAMA_LITELLM_MODEL = f"ollama_chat/{OLLAMA_MODEL}"

APP_NAME = "qanda_pbix"
USER_ID = "local_user"
DEFAULT_SESSION_ID = "streamlit_chat"

MAX_TOOL_CHARS = int(os.environ.get("QANDA_MAX_TOOL_CHARS", "12000"))
MAX_LIST_ITEMS = int(os.environ.get("QANDA_MAX_LIST_ITEMS", "40"))
