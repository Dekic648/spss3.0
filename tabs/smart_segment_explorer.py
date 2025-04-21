import streamlit as st
import pandas as pd
from utils.segmenter import create_segment
from utils.stats_runner import run_t_test
from utils.rule_based_summary import generate_summary

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

def show():
    st.header("🧠 Smart Segment Explorer")

    df = get_dataframe()
    if df is None:
        return

    st.markdown("""
    **What is this?**  
    This tool auto-creates segments like "High" vs. "Low Satisfaction" and runs statistical tests to find meaningful differences across other variables.

    **How to use:**  
    1. Choose a numeric column you'd like to segment  
    2. The app will create two groups and compare them  
    3. You'll see insights where statistically significant differences exist  
    """)

    col = st.selectbox("Select a numeric column to segment", df.select_dtypes(include='number').columns)
    
    median, seg_col = create_segment(df, col)
    df["segment"] = seg_col

    insights = []
    for other_col in df.select_dtypes(include='number').columns:
        if other_col != col:
            group1 = df[df["segment"] == "High"][other_col]
            group2 = df[df["segment"] == "Low"][other_col]
            stat, p_val = run_t_test(group1, group2)
            insights.append(generate_summary(other_col, group1.mean() - group2.mean(), p_val))

    significant = [ins for ins in insights if ins]
    if significant:
        st.subheader("🔍 Key Differences Found:")
        st.write(significant)
    else:
        st.info("No significant insights were found based on this segment.")
