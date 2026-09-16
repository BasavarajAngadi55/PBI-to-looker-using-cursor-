#!/usr/bin/env python3
"""PBIX → Looker UI: migration workspace + grounded QandA chat."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
PHASE2 = ROOT.parent / "phase2"
PHASE3 = ROOT.parent / "phase3"
VALIDATION = ROOT.parent / "validation"
QANDA = ROOT.parent / "QandA"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "inventory"))
sys.path.insert(0, str(PHASE2))
sys.path.insert(0, str(PHASE3))
sys.path.insert(0, str(VALIDATION))
sys.path.insert(0, str(QANDA))

import generate_agent_validation_proof as val_mod
import generate_data_model_diagram as dmd_mod
import generate_summary_pdf as pdf_mod
import run_phase1_six_agents as extract_mod
import workspace as workspace_mod

SUMMARY_PDF = ROOT / "OBJECT_SUMMARY.pdf"
DATA_MODEL_PDF = ROOT / "DATA_MODEL.pdf"
CURRENT_META = ROOT / "CURRENT_PBIX.json"
LOOKML_ZIP = PHASE2 / "LOOKML_PROJECT.zip"
LOOKER_GUIDE_PDF = PHASE2 / "LOOKER_DEVELOPER_GUIDE.pdf"
DASH_ZIP = PHASE3 / "LOOKML_DASHBOARDS.zip"
DASH_GUIDE_PDF = PHASE3 / "DASHBOARD_DEVELOPER_GUIDE.pdf"
VAL_PDF = VALIDATION / "VALIDATION_REPORT.pdf"

PHASE_LABELS = {
    "1": "Extract Power BI model",
    "2": "Build Looker semantic model (LookML)",
    "3": "Convert report pages → Looker dashboards",
    "v": "Migration scorecard & user-input checklist",
}


st.set_page_config(page_title="PBIX → Looker", layout="wide")

# Sidebar nav — NOT tabs. Streamlit chat_input inside tabs breaks multi-turn chat.
st.sidebar.title("PBIX → Looker")
section = st.sidebar.radio(
    "Workspace",
    ["Migrate PBIX → Looker", "QandA assistant"],
    label_visibility="collapsed",
)
st.sidebar.caption(
    "Use **QandA assistant** for chat. "
    "Chat lives outside tabs so you can keep messaging."
)

st.title("PBIX → Looker migration")
if section.startswith("Migrate"):
    st.caption("Deterministic extract → LookML → dashboards → scorecard for one PBIX at a time.")
else:
    st.caption("Ask about the current PBIX. Type a message and press Enter.")

# Only show active PBIX after upload + migrate in THIS session (not leftover disk files)
if st.session_state.get("qanda_ready") and st.session_state.get("active_pbix_name"):
    st.success(f"Active PBIX (this session): **{st.session_state['active_pbix_name']}**")


def _render_disk_downloads() -> None:
    if not (LOOKML_ZIP.exists() or LOOKER_GUIDE_PDF.exists() or DASH_ZIP.exists() or VAL_PDF.exists()):
        return
    st.markdown(f"#### 2 · {PHASE_LABELS['2']} (last run on disk)")
    c_zip, c_guide = st.columns(2)
    with c_zip:
        if LOOKML_ZIP.exists():
            st.download_button(
                "Download LookML project (.zip)",
                data=LOOKML_ZIP.read_bytes(),
                file_name="LOOKML_PROJECT.zip",
                mime="application/zip",
                key="dl_lookml_zip_disk",
            )
    with c_guide:
        if LOOKER_GUIDE_PDF.exists():
            st.download_button(
                "Download Looker developer guide (.pdf)",
                data=LOOKER_GUIDE_PDF.read_bytes(),
                file_name="LOOKER_DEVELOPER_GUIDE.pdf",
                mime="application/pdf",
                key="dl_looker_guide_disk",
            )
    if DASH_ZIP.exists() or DASH_GUIDE_PDF.exists():
        st.markdown(f"#### 3 · {PHASE_LABELS['3']} (last run on disk)")
        c_dz, c_dg = st.columns(2)
        with c_dz:
            if DASH_ZIP.exists():
                st.download_button(
                    "Download LookML dashboards (.zip)",
                    data=DASH_ZIP.read_bytes(),
                    file_name="LOOKML_DASHBOARDS.zip",
                    mime="application/zip",
                    key="dl_dash_zip_disk",
                )
        with c_dg:
            if DASH_GUIDE_PDF.exists():
                st.download_button(
                    "Download dashboard developer guide (.pdf)",
                    data=DASH_GUIDE_PDF.read_bytes(),
                    file_name="DASHBOARD_DEVELOPER_GUIDE.pdf",
                    mime="application/pdf",
                    key="dl_dash_guide_disk",
                )
    if VAL_PDF.exists():
        st.markdown(f"#### ✓ · {PHASE_LABELS['v']} (last run on disk)")
        st.download_button(
            "Download validation report (.pdf)",
            data=VAL_PDF.read_bytes(),
            file_name="VALIDATION_REPORT.pdf",
            mime="application/pdf",
            key="dl_val_pdf_disk",
        )


if section == "Migrate PBIX → Looker":
    st.markdown(
        f"""
**Pipeline (one active PBIX at a time)**

| Step | What it does |
|------|----------------|
| **1 · {PHASE_LABELS['1']}** | Reads the `.pbix` → tables, measures, relationships, Power Query |
| **2 · {PHASE_LABELS['2']}** | Maps inventory → LookML views/explores + developer guide |
| **3 · {PHASE_LABELS['3']}** | Maps report pages/visuals → LookML dashboards + coverage |
| **✓ · {PHASE_LABELS['v']}** | % done / % left + where you must edit LookML |
        """
    )

    uploaded = st.file_uploader("Upload PBIX file", type=["pbix"], key="pbix_uploader")
    st.markdown("**Or** paste a local path:")
    pbix_path_input = st.text_input(
        "Local PBIX path",
        value="",
        placeholder="/Users/you/Downloads/model.pbix",
        label_visibility="collapsed",
        key="pbix_path_input",
    )

    upload_token = ""
    if uploaded is not None:
        upload_token = f"upload:{uploaded.name}:{uploaded.size}"
    elif pbix_path_input.strip():
        upload_token = f"path:{pbix_path_input.strip()}"

    if upload_token and st.session_state.get("last_input_token") != upload_token:
        st.session_state["ok"] = False
        st.session_state["result"] = None
        st.session_state["last_input_token"] = upload_token
        st.session_state["qanda_messages"] = []
        st.session_state["active_pbix_name"] = None
        st.session_state["qanda_ready"] = False

    can_run = uploaded is not None or bool(pbix_path_input.strip())
    run = st.button("Run full migration (1 → 2 → 3 → scorecard)", type="primary", disabled=not can_run)

    if run:
        if uploaded is not None:
            workspace_mod.UPLOADS.mkdir(parents=True, exist_ok=True)
            pbix_path = workspace_mod.UPLOADS / uploaded.name
            pbix_path.write_bytes(uploaded.getbuffer())
        else:
            pbix_path = Path(pbix_path_input.strip()).expanduser()
            if not pbix_path.exists():
                st.error(f"File not found: {pbix_path}")
                st.stop()
            if pbix_path.suffix.lower() != ".pbix":
                st.error("Path must point to a .pbix file")
                st.stop()

        with st.spinner(f"Running migration for {pbix_path.name}…"):
            try:
                extract_mod = importlib.reload(extract_mod)
                dmd_mod = importlib.reload(dmd_mod)
                pdf_mod = importlib.reload(pdf_mod)
                val_mod = importlib.reload(val_mod)
                workspace_mod = importlib.reload(workspace_mod)

                result = extract_mod.run_extraction(pbix_path)

                try:
                    dmd_mod.main()
                except Exception as e:
                    st.warning(f"Data model diagram skipped: {e}")

                try:
                    val_mod.main()
                except Exception as e:
                    st.warning(f"Extract validation proof skipped: {e}")

                pdf_mod.write_summary_pdf(
                    result["summary_text"],
                    Path(result["pbix_path"]).name,
                    SUMMARY_PDF,
                )

                phase2_summary = None
                phase3_summary = None
                validation_summary = None
                try:
                    import run_phase2 as phase2_mod

                    phase2_mod = importlib.reload(phase2_mod)
                    phase2_summary = phase2_mod.run(ROOT / "inventory")
                except Exception as e:
                    st.warning(f"{PHASE_LABELS['2']} skipped: {e}")

                try:
                    import run_phase3 as phase3_mod

                    phase3_mod = importlib.reload(phase3_mod)
                    phase3_summary = phase3_mod.run(Path(result["pbix_path"]))
                except Exception as e:
                    st.warning(f"{PHASE_LABELS['3']} skipped: {e}")

                try:
                    import run_validation as val_run

                    val_run = importlib.reload(val_run)
                    validation_summary = val_run.run()
                except Exception as e:
                    st.warning(f"{PHASE_LABELS['v']} skipped: {e}")

                st.session_state["result"] = result
                st.session_state["phase2"] = phase2_summary
                st.session_state["phase3"] = phase3_summary
                st.session_state["validation"] = validation_summary
                st.session_state["ok"] = True
                st.session_state["active_pbix_name"] = Path(result["pbix_path"]).name
                st.session_state["qanda_ready"] = True
            except Exception as e:
                st.session_state["ok"] = False
                st.session_state["result"] = None
                st.session_state["phase2"] = None
                st.session_state["phase3"] = None
                st.session_state["validation"] = None
                st.session_state["active_pbix_name"] = None
                st.session_state["qanda_ready"] = False
                st.error(str(e))

    if st.session_state.get("ok") and st.session_state.get("result"):
        result = st.session_state["result"]
        c = result["counts"]
        src_name = Path(result["pbix_path"]).name

        st.success(f"Migration complete for **{src_name}**")
        st.caption("All generated files below belong to this PBIX only.")

        st.markdown(f"### 1 · {PHASE_LABELS['1']}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tables", c["tables"])
        m2.metric("Measures", c["measures"])
        m3.metric("Relationships", c["relationships"])
        m4.metric("Power Query", c["power_query"])

        st.subheader("Summary")
        st.text(result["summary_text"])

        st.download_button(
            "Download summary (.txt)",
            data=(result["summary_text"] + "\n").encode("utf-8"),
            file_name="OBJECT_SUMMARY.txt",
            mime="text/plain",
        )
        if SUMMARY_PDF.exists():
            st.download_button(
                "Download summary (.pdf)",
                data=SUMMARY_PDF.read_bytes(),
                file_name="OBJECT_SUMMARY.pdf",
                mime="application/pdf",
            )
        if DATA_MODEL_PDF.exists():
            st.markdown("**Data model diagram**")
            st.download_button(
                "Download data model (.pdf)",
                data=DATA_MODEL_PDF.read_bytes(),
                file_name="DATA_MODEL.pdf",
                mime="application/pdf",
                type="primary",
                key="dl_data_model",
            )

        inv = ROOT / "inventory" / "OBJECT_INVENTORY.md"
        if inv.exists():
            st.download_button(
                "Download full inventory (.md)",
                data=inv.read_bytes(),
                file_name="OBJECT_INVENTORY.md",
                mime="text/markdown",
            )

        st.markdown(f"### 2 · {PHASE_LABELS['2']}")
        p2 = st.session_state.get("phase2") or {}
        if p2:
            st.caption(
                f"LookML: **{p2.get('views', '?')}** views · **{p2.get('measures', '?')}** measures · "
                f"model `{p2.get('model_name', '?')}`"
            )
        c_zip, c_guide = st.columns(2)
        with c_zip:
            if LOOKML_ZIP.exists():
                st.download_button(
                    "Download LookML project (.zip)",
                    data=LOOKML_ZIP.read_bytes(),
                    file_name="LOOKML_PROJECT.zip",
                    mime="application/zip",
                    type="primary",
                    key="dl_lookml_zip",
                )
            else:
                st.warning("LookML ZIP not found — re-run migration.")
        with c_guide:
            if LOOKER_GUIDE_PDF.exists():
                st.download_button(
                    "Download Looker developer guide (.pdf)",
                    data=LOOKER_GUIDE_PDF.read_bytes(),
                    file_name="LOOKER_DEVELOPER_GUIDE.pdf",
                    mime="application/pdf",
                    type="primary",
                    key="dl_looker_guide",
                )
            else:
                st.warning("Developer guide PDF not found — re-run migration.")

        st.markdown(f"### 3 · {PHASE_LABELS['3']}")
        p3 = st.session_state.get("phase3") or {}
        if p3:
            pct = p3.get("weighted_completion_pct", "?")
            meets = "meets" if p3.get("meets_target") else "below"
            st.caption(
                f"Pages: **{p3.get('pages', '?')}** · visuals: **{p3.get('visuals', '?')}** · "
                f"dashboards: **{p3.get('dashboards', '?')}** · "
                f"weighted completion **{pct}%** ({meets} 70% target)"
            )
        c_dz, c_dg = st.columns(2)
        with c_dz:
            if DASH_ZIP.exists():
                st.download_button(
                    "Download LookML dashboards (.zip)",
                    data=DASH_ZIP.read_bytes(),
                    file_name="LOOKML_DASHBOARDS.zip",
                    mime="application/zip",
                    type="primary",
                    key="dl_dash_zip",
                )
            else:
                st.warning("Dashboards ZIP not found — re-run migration.")
        with c_dg:
            if DASH_GUIDE_PDF.exists():
                st.download_button(
                    "Download dashboard developer guide (.pdf)",
                    data=DASH_GUIDE_PDF.read_bytes(),
                    file_name="DASHBOARD_DEVELOPER_GUIDE.pdf",
                    mime="application/pdf",
                    type="primary",
                    key="dl_dash_guide",
                )
            else:
                st.warning("Dashboard guide PDF not found — re-run migration.")

        cmp = PHASE3 / "comparison" / "PAGE_COMPARISON.md"
        if cmp.exists():
            st.download_button(
                "Download PBI ↔ Looker page comparison (.md)",
                data=cmp.read_bytes(),
                file_name="PAGE_COMPARISON.md",
                mime="text/markdown",
                key="dl_page_cmp",
            )

        st.markdown(f"### ✓ · {PHASE_LABELS['v']}")
        v = st.session_state.get("validation") or {}
        if v:
            st.caption(
                f"Overall **{v.get('overall_pct_done', '?')}%** done · "
                f"**{v.get('overall_pct_left', '?')}%** left · "
                f"confidence **{v.get('confidence', '?')}** · "
                f"steps 1/2/3 = {v.get('phase1_pct')}% / {v.get('phase2_pct')}% / {v.get('phase3_pct')}%"
            )
            if v.get("warning"):
                st.warning(v["warning"])
        if VAL_PDF.exists():
            st.download_button(
                "Download validation report (.pdf)",
                data=VAL_PDF.read_bytes(),
                file_name="VALIDATION_REPORT.pdf",
                mime="application/pdf",
                type="primary",
                key="dl_val_pdf",
            )
        else:
            st.warning("Validation PDF not found — re-run migration.")
    else:
        st.write("Upload a PBIX and click **Run full migration**. Previous outputs for other PBIX files are replaced.")
        _render_disk_downloads()


else:
    # QandA at page root (not inside st.tabs) so chat_input keeps working
    try:
        from ui_chat import render_qanda_chat

        render_qanda_chat()
    except Exception as e:
        st.warning(f"QandA chat unavailable: {e}")
