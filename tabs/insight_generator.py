import streamlit as st
import pandas as pd
from utils.rule_based_summary import generate_summary
from utils.segmenter import create_segment
from utils.stats_runner import run_t_test

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

def show():
    st.header("🚀 Insight Generator")

    df = get_dataframe()
    if df is None:
        return

    st.markdown("""
    **What is this?**  
    This tool scans all numeric columns, automatically generates "High vs Low" segments, and searches for statistically significant differences.

    **How to use:**  
    1. No setup required — it works automatically  
    2. The app compares each variable with all others  
    3. Results are shown as human-readable insights  
    """)

    insights = []
    for col in df.select_dtypes(include='number').columns:
        median, seg_col = create_segment(df, col)
        df["segment"] = seg_col
        for other_col in df.select_dtypes(include='number').columns:
            if other_col != col:
                group1 = df[df["segment"] == "High"][other_col]
                group2 = df[df["segment"] == "Low"][other_col]
                stat, p_val = run_t_test(group1, group2)
                summary = generate_summary(other_col, group1.mean() - group2.mean(), p_val)
                if summary:
                    insights.append(summary)

    if insights:
        st.subheader("🔍 Automatically Discovered Insights")
        for i, ins in enumerate(insights):
            st.markdown(f"**Insight {i+1}:** {ins}")
    else:
        st.info("No significant insights found.")
