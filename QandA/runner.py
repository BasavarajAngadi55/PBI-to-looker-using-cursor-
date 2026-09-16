#!/usr/bin/env python3
"""Sync Q&A interface for Streamlit / CLI over ADK + Ollama Gemma."""
from __future__ import annotations

import asyncio
import sys
import uuid
from pathlib import Path
from typing import Any

# Ensure QandA package root is importable
QANDA_ROOT = Path(__file__).resolve().parent
if str(QANDA_ROOT) not in sys.path:
    sys.path.insert(0, str(QANDA_ROOT))

from google.genai import types as genai_types

from config import APP_NAME, DEFAULT_SESSION_ID, OLLAMA_MODEL, USER_ID


class QandAService:
    """Lazy-init ADK runner so Streamlit import stays light."""

    def __init__(self) -> None:
        self._runner = None
        self._session_service = None
        self._ready_error: str | None = None

    def _ensure(self) -> None:
        if self._runner is not None or self._ready_error:
            return
        try:
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService

            from agents.root_agent import root_agent

            self._session_service = InMemorySessionService()
            self._runner = Runner(
                agent=root_agent,
                app_name=APP_NAME,
                session_service=self._session_service,
            )
        except Exception as e:
            self._ready_error = str(e)

    async def _ensure_session(self, session_id: str) -> None:
        assert self._session_service is not None
        existing = await self._session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
        if existing is None:
            await self._session_service.create_session(
                app_name=APP_NAME, user_id=USER_ID, session_id=session_id
            )

    async def ask_async(self, question: str, session_id: str | None = None) -> dict[str, Any]:
        self._ensure()
        if self._ready_error:
            return {
                "ok": False,
                "answer": (
                    f"QandA agent failed to start: {self._ready_error}. "
                    "Install deps: pip install -r QandA/requirements.txt "
                    f"and ensure Ollama is running with model `{OLLAMA_MODEL}`."
                ),
                "model": OLLAMA_MODEL,
            }
        sid = session_id or DEFAULT_SESSION_ID
        await self._ensure_session(sid)
        assert self._runner is not None

        from tools.context_builder import build_grounding_context

        grounded = build_grounding_context(question)
        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=grounded)],
        )
        final_text_parts: list[str] = []
        try:
            async for event in self._runner.run_async(
                user_id=USER_ID,
                session_id=sid,
                new_message=content,
            ):
                # Prefer final response events only (avoid chain-of-thought / tool chatter)
                is_final = False
                if hasattr(event, "is_final_response") and callable(event.is_final_response):
                    try:
                        is_final = bool(event.is_final_response())
                    except Exception:
                        is_final = False
                if not is_final and getattr(event, "partial", None):
                    continue
                if not is_final:
                    # Keep last non-empty model text as fallback
                    pass

                if getattr(event, "content", None) and event.content.parts:
                    chunk = []
                    for part in event.content.parts:
                        # Skip function-call / thought-only parts when possible
                        if getattr(part, "function_call", None):
                            continue
                        if getattr(part, "function_response", None):
                            continue
                        text = getattr(part, "text", None)
                        if text and text.strip():
                            chunk.append(text.strip())
                    if chunk:
                        joined = "\n".join(chunk)
                        if is_final:
                            final_text_parts = [joined]
                        else:
                            # Keep overwriting with latest substantive text
                            final_text_parts = [joined]
        except Exception as e:
            return {
                "ok": False,
                "answer": (
                    f"QandA run error: {e}. "
                    f"Check `ollama serve` and `ollama pull {OLLAMA_MODEL}`."
                ),
                "model": OLLAMA_MODEL,
            }

        answer = "\n".join(final_text_parts).strip()
        answer = _clean_answer(answer)
        if not answer:
            answer = (
                "No text response from the agent. "
                "Try a more specific question, or verify Ollama/Gemma is running."
            )
        return {"ok": True, "answer": answer, "model": OLLAMA_MODEL, "session_id": sid}

    def ask(self, question: str, session_id: str | None = None) -> dict[str, Any]:
        return asyncio.run(self.ask_async(question, session_id=session_id))


def _clean_answer(text: str) -> str:
    """Drop obvious chain-of-thought prefixes from local models when present."""
    if not text:
        return text
    markers = (
        "\n**Facts**",
        "\nFacts",
        "\nThe current PBIX",
        "\nCurrent PBIX",
        "\n**Fact**",
        "\nFact:",
    )
    # If model emitted a clear Facts section, keep from there
    lower = text
    for m in markers:
        idx = lower.find(m)
        if idx >= 0:
            return text[idx:].lstrip("\n ").strip()
    # If it looks like planning prose, take the last paragraph block
    bad_starts = (
        "the user asked",
        "i need to",
        "i will call",
        "plan:",
        "let's start",
        "from the previous",
    )
    lines = text.splitlines()
    if lines and any(lines[0].strip().lower().startswith(b) for b in bad_starts):
        # Find last non-empty contiguous block that looks factual
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith(("**", "-", "*", "Current", "OBJECT", "Tables", "PBIX")):
                return "\n".join(lines[i:]).strip()
        # fallback: last 8 lines
        return "\n".join(lines[-8:]).strip()
    return text


_SERVICE: QandAService | None = None


def get_service() -> QandAService:
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = QandAService()
    return _SERVICE


def ask(question: str, session_id: str | None = None) -> dict[str, Any]:
    return get_service().ask(question, session_id=session_id)


def main() -> None:
    q = " ".join(sys.argv[1:]).strip() or "What is the current PBIX and object counts?"
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Q: {q}\n")
    result = ask(q, session_id=f"cli_{uuid.uuid4().hex[:8]}")
    print(result.get("answer"))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
