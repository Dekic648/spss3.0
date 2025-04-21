import streamlit as st
import pandas as pd
from utils.clustering_utils import run_kmeans

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

def show():
    st.header("🧬 Persona Lab")

    df = get_dataframe()
    if df is None:
        return

    st.markdown("""
    **What is this?**  
    This tool identifies groups of users with similar behaviors — useful for defining personas based on patterns in your survey data.

    **How to use:**  
    1. Select 2+ numeric columns that represent user traits  
    2. The system will create 3 clusters by default  
    3. You'll see average scores for each group — start naming them!  
    """)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_cols = st.multiselect("Select numeric columns to define personas", numeric_cols)

    if len(selected_cols) >= 2:
        cluster_df, _ = run_kmeans(df.copy(), selected_cols, n_clusters=3)

        st.subheader("📊 Cluster Averages by Feature")
        avg_scores = cluster_df.groupby('Cluster')[selected_cols].mean().round(2).reset_index()
        st.dataframe(avg_scores)

        st.subheader("🧠 Persona Descriptions (Auto Summary)")
        for idx, row in avg_scores.iterrows():
            traits = ", ".join([f"{col}={row[col]}" for col in selected_cols])
            st.markdown(f"**Cluster {int(row['Cluster'])}**: Users with {traits}")
    else:
        st.warning("Please select at least 2 numeric columns.")
