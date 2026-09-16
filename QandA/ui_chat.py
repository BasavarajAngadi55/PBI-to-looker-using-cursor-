"""Streamlit QandA — only after PBIX upload + migrate in this session."""
from __future__ import annotations

import sys
import uuid
from pathlib import Path

import streamlit as st

QANDA_ROOT = Path(__file__).resolve().parent
if str(QANDA_ROOT) not in sys.path:
    sys.path.insert(0, str(QANDA_ROOT))

NO_UPLOAD_REPLY = (
    "Please **upload a PBIX and run migration first**.\n\n"
    "1. Sidebar → **Migrate PBIX → Looker**\n"
    "2. Upload your `.pbix`\n"
    "3. Click **Run full migration**\n"
    "4. Return here to ask about **that** file only\n\n"
    "I do not answer from leftover files on disk."
)

GREETING_NO_PBIX = (
    "Hi — I’m your **PBIX → Looker migration accelerator**.\n\n"
    "I don’t have an active PBIX in this session yet.\n"
    "Please upload a file under **Migrate PBIX → Looker**, run migration, "
    "then come back and ask me about it.\n\n"
    "How can I help once your PBIX is loaded?"
)

MISMATCH_REPLY = (
    "The inventory on disk does **not** match the PBIX you migrated in this session.\n"
    "Please re-run **Migrate PBIX → Looker** for your uploaded file."
)


def _session_pbix_ready() -> tuple[bool, str | None, str | None]:
    active = st.session_state.get("active_pbix_name")
    ready = bool(st.session_state.get("qanda_ready")) and bool(active)
    if not ready:
        return False, None, NO_UPLOAD_REPLY

    from tools.pbix_context import get_current_pbix_meta

    meta = get_current_pbix_meta()
    disk_name = meta.get("pbix_name")
    if not disk_name or disk_name != active:
        return False, active, MISMATCH_REPLY
    return True, active, None


def render_qanda_chat() -> None:
    from config import OLLAMA_MODEL
    from tools.lookml_web_advice import is_expression_conversion_request
    from tools.scope import OUT_OF_SCOPE_REPLY, is_greeting, is_help, is_in_scope

    ready, active_pbix, gate_error = _session_pbix_ready()

    st.markdown("### QandA assistant")

    # No default suggestions / no leftover chat when nothing is uploaded
    if not ready:
        st.session_state["qanda_messages"] = []
        st.warning("Upload a PBIX first — QandA stays empty until migration completes in this session.")
        st.info(NO_UPLOAD_REPLY)
        st.caption(f"Model ready: `{OLLAMA_MODEL}` (waiting for your PBIX)")
        # Still allow a simple hi — but never inventory facts
        prompt = st.chat_input("Upload a PBIX first — or say hi…")
        if not prompt:
            return
        prompt = prompt.strip()
        st.session_state["qanda_messages"] = [
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": GREETING_NO_PBIX
                if (is_greeting(prompt) or is_help(prompt))
                else (OUT_OF_SCOPE_REPLY if not is_in_scope(prompt) and not is_expression_conversion_request(prompt) else NO_UPLOAD_REPLY),
            },
        ]
        # Expression conversion without PBIX: general advice only
        if is_expression_conversion_request(prompt) and not (is_greeting(prompt) or is_help(prompt)):
            with st.spinner("Looking up LookML best practices…"):
                try:
                    import runner as runner_mod

                    runner_mod._SERVICE = None
                    q = (
                        "[NO_ACTIVE_PBIX_IN_SESSION] Expression→LookML advice only. "
                        "Do not invent inventory facts. "
                        + prompt
                    )
                    result = runner_mod.ask(q, session_id=f"nopf_{uuid.uuid4().hex[:8]}")
                    ans = result.get("answer") or NO_UPLOAD_REPLY
                    st.session_state["qanda_messages"][-1] = {
                        "role": "assistant",
                        "content": "_No PBIX uploaded — general LookML guidance only._\n\n" + ans,
                    }
                except Exception as e:
                    st.session_state["qanda_messages"][-1] = {
                        "role": "assistant",
                        "content": f"⚠️ {e}\n\n{NO_UPLOAD_REPLY}",
                    }
        for msg in st.session_state["qanda_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        return

    st.success(f"Active PBIX (this session): **{active_pbix}**")
    st.caption(f"Model: `{OLLAMA_MODEL}` · Answers only for this uploaded file.")

    if "qanda_messages" not in st.session_state:
        st.session_state["qanda_messages"] = []
    if "qanda_session_id" not in st.session_state:
        st.session_state["qanda_session_id"] = f"ui_{uuid.uuid4().hex[:10]}"

    _, c2 = st.columns([6, 1])
    with c2:
        if st.button("Clear", use_container_width=True, key="qanda_clear"):
            st.session_state["qanda_messages"] = []
            st.session_state["qanda_session_id"] = f"ui_{uuid.uuid4().hex[:10]}"
            st.rerun()

    for msg in st.session_state["qanda_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about your uploaded PBIX…")
    if not prompt:
        return

    prompt = prompt.strip()
    if not prompt:
        return

    st.session_state["qanda_messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    from tools.scope import GREETING_REPLY

    if is_greeting(prompt) or is_help(prompt):
        answer = GREETING_REPLY
    elif not is_in_scope(prompt):
        answer = OUT_OF_SCOPE_REPLY
    else:
        with st.chat_message("assistant"):
            with st.spinner(f"Thinking about **{active_pbix}**…"):
                try:
                    import runner as runner_mod

                    runner_mod._SERVICE = None
                    result = runner_mod.ask(
                        prompt, session_id=st.session_state["qanda_session_id"]
                    )
                    answer = result.get("answer") or "(empty response)"
                    if not result.get("ok"):
                        answer = f"⚠️ {answer}"
                except Exception as e:
                    answer = f"⚠️ QandA error: {e}"
            st.markdown(answer)
        st.session_state["qanda_messages"].append({"role": "assistant", "content": answer})
        return

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state["qanda_messages"].append({"role": "assistant", "content": answer})
