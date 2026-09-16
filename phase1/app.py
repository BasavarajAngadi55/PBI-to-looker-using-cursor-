#!/usr/bin/env python3
"""Simple UI: one PBIX at a time inside phase1/ (dynamic overwrite, no backups)."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
PHASE2 = ROOT.parent / "phase2"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "inventory"))
sys.path.insert(0, str(PHASE2))

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


st.set_page_config(page_title="PBIX Extract", layout="centered")
st.title("PBIX semantic extract")
st.caption(
    "Deterministic Phase 1 extract (Python + pbixray — no LLM). "
    "Each upload replaces all inventory for that PBIX only in phase1/. "
    "Phase 2 builds LookML ZIP + Looker developer guide PDF from that inventory."
)

if CURRENT_META.exists():
    try:
        cur = json.loads(CURRENT_META.read_text())
        st.caption(f"Current PBIX on disk: **{cur.get('pbix_name', '?')}**")
    except Exception:
        pass

uploaded = st.file_uploader("PBIX file", type=["pbix"], key="pbix_uploader")

st.markdown("**Or** paste a local path:")
pbix_path_input = st.text_input(
    "Local PBIX path",
    value="",
    placeholder="/Users/you/Downloads/model.pbix",
    label_visibility="collapsed",
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

can_run = uploaded is not None or bool(pbix_path_input.strip())
run = st.button("Extract summary", type="primary", disabled=not can_run)

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

    with st.spinner(f"Resetting phase1 outputs and extracting {pbix_path.name}..."):
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
                st.warning(f"Validation proof skipped: {e}")

            pdf_mod.write_summary_pdf(
                result["summary_text"],
                Path(result["pbix_path"]).name,
                SUMMARY_PDF,
            )

            phase2_summary = None
            try:
                import run_phase2 as phase2_mod

                phase2_mod = importlib.reload(phase2_mod)
                phase2_summary = phase2_mod.run(ROOT / "inventory")
            except Exception as e:
                st.warning(f"Phase 2 LookML / developer guide skipped: {e}")

            st.session_state["result"] = result
            st.session_state["phase2"] = phase2_summary
            st.session_state["ok"] = True
        except Exception as e:
            st.session_state["ok"] = False
            st.session_state["result"] = None
            st.session_state["phase2"] = None
            st.error(str(e))

if st.session_state.get("ok") and st.session_state.get("result"):
    result = st.session_state["result"]
    c = result["counts"]
    src_name = Path(result["pbix_path"]).name

    st.success(f"Extract complete for **{src_name}**")
    st.info(
        "phase1/ now holds only this PBIX’s inventory, M files, summary, and data model "
        f"(active upload: `uploads/{src_name}`)."
    )

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
        st.subheader("Data model")
        st.caption("Download the PDF to zoom and inspect the ER diagram + relationships clearly.")
        st.download_button(
            "Download data model (.pdf)",
            data=DATA_MODEL_PDF.read_bytes(),
            file_name="DATA_MODEL.pdf",
            mime="application/pdf",
            type="primary",
        )

    inv = ROOT / "inventory" / "OBJECT_INVENTORY.md"
    if inv.exists():
        st.download_button(
            "Download full inventory (.md)",
            data=inv.read_bytes(),
            file_name="OBJECT_INVENTORY.md",
            mime="text/markdown",
        )

    st.subheader("Phase 2 — Looker")
    p2 = st.session_state.get("phase2") or {}
    if p2:
        st.caption(
            f"LookML: **{p2.get('views', '?')}** views · **{p2.get('measures', '?')}** measures · "
            f"model `{p2.get('model_name', '?')}`"
        )
    else:
        st.caption("Generated from the Phase 1 inventory for this PBIX.")

    c_zip, c_guide = st.columns(2)
    with c_zip:
        if LOOKML_ZIP.exists():
            st.download_button(
                "Download all LookML (.zip)",
                data=LOOKML_ZIP.read_bytes(),
                file_name="LOOKML_PROJECT.zip",
                mime="application/zip",
                type="primary",
                key="dl_lookml_zip",
            )
        else:
            st.warning("LookML ZIP not found — re-run extract.")
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
            st.warning("Developer guide PDF not found — re-run extract.")
else:
    st.write("Upload a PBIX and click **Extract summary**. Previous extract files are replaced in place.")
    if LOOKML_ZIP.exists() or LOOKER_GUIDE_PDF.exists():
        st.subheader("Phase 2 — Looker (last run on disk)")
        c_zip, c_guide = st.columns(2)
        with c_zip:
            if LOOKML_ZIP.exists():
                st.download_button(
                    "Download all LookML (.zip)",
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
