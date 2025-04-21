
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_loader import load_file
from utils.variable_detection import detect_column_types

def show():
    st.header("📥 Upload & Overview")

    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xls", "xlsx"])
    if uploaded_file:
        df = load_file(uploaded_file)
        if df is not None:
            st.session_state["df"] = df
            st.session_state["column_types"] = detect_column_types(df)

    if "df" in st.session_state:
        df = st.session_state["df"]
        column_types = st.session_state.get("column_types", detect_column_types(df))

        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("⚙️ Auto-Detected + Editable Variable Types")
        edited_types = {}
        for col in df.columns:
            default_type = column_types.get(col, "numeric")
            edited_types[col] = st.selectbox(
                f"{col}",
                ["numeric", "likert", "categorical", "checkbox", "matrix", "open_ended"],
                index=["numeric", "likert", "categorical", "checkbox", "matrix", "open_ended"].index(default_type),
                key=f"type_{col}"
            )
        st.session_state["column_types"] = edited_types

        st.subheader("📊 Descriptive Charts (Auto-generated)")
        segment_col = st.selectbox("Optional: Segment data by", ["(none)"] + [col for col, typ in edited_types.items() if typ == "categorical"])
        numeric_or_likert = [col for col, typ in edited_types.items() if typ in ["numeric", "likert"]]

        if segment_col == "(none)":
            for col in numeric_or_likert:
                fig, ax = plt.subplots()
                pct = df[col].value_counts(normalize=True).sort_index() * 100
                pct.plot(kind="bar", ax=ax)
                for i, val in enumerate(pct):
                    ax.text(i, val, f"{val:.1f}%", ha='center', va='bottom')
                ax.set_title(f"{col} (%)")
                st.pyplot(fig)
        else:
            for col in numeric_or_likert:
                fig, ax = plt.subplots()
                grouped = df.groupby(segment_col)[col].value_counts(normalize=True).unstack().fillna(0) * 100
                grouped.T.plot(kind="bar", ax=ax)
                for container in ax.containers:
                    ax.bar_label(container, fmt="%.1f%%")
                ax.set_title(f"{col} (%) grouped by {segment_col}")
                st.pyplot(fig)
    else:
        st.info("Please upload a file to continue.")
