import streamlit as st
import pandas as pd

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

import streamlit as st
import yaml

def show():
    st.header("📚 Use-case Templates")

    with open("data/templates.yaml") as f:
        templates = yaml.safe_load(f)

    st.subheader("Insight Templates")
    st.json(templates)
