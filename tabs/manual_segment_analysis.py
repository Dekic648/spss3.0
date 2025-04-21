import streamlit as st
import pandas as pd

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

import streamlit as st
import pandas as pd
from utils.stats_runner import run_t_test

def show():
    st.header("📊 Manual Segment Analysis")

    df = get_dataframe()
    if df is None:
        st.info("Please upload a file in the Upload tab first.")
        return

    df = df

    segment_col = st.selectbox("Select a segment column (categorical)", df.select_dtypes(include='object').columns)
    compare_col = st.selectbox("Select a numeric column to compare", df.select_dtypes(include='number').columns)

    groups = df[segment_col].unique()
    if len(groups) == 2:
        group1 = df[df[segment_col] == groups[0]][compare_col]
        group2 = df[df[segment_col] == groups[1]][compare_col]
        stat, p_val = run_t_test(group1, group2)
        st.write(f"t-test between {groups[0]} and {groups[1]}: p = {p_val:.4f}")
    else:
        st.warning("Currently supports only 2-group comparisons.")
