
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

        st.subheader("📊 Descriptive Charts")
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

        # GROUPING INTERFACE
        st.subheader("🧩 Group Checkbox & Matrix Questions")

        # Initialize session states if missing
        if "checkbox_map" not in st.session_state:
            st.session_state["checkbox_map"] = {}
        if "matrix_map" not in st.session_state:
            st.session_state["matrix_map"] = {}

        # Checkbox Group UI
        st.markdown("### ➕ Create Checkbox Group")
        checkbox_candidates = [col for col, typ in edited_types.items() if typ == "checkbox"]
        cb_group_name = st.text_input("New Checkbox Group Name")
        cb_selected_cols = st.multiselect("Select checkbox columns", checkbox_candidates)
        if st.button("Add Checkbox Group"):
            if cb_group_name and cb_selected_cols:
                st.session_state["checkbox_map"][cb_group_name] = cb_selected_cols
                st.success(f"Group '{cb_group_name}' added!")

        # Show charts for checkbox groups
        for group_name, columns in st.session_state["checkbox_map"].items():
            st.markdown(f"#### ✅ Checkbox Group: {group_name}")
            group_df = df[columns].notna().astype(int)
            if segment_col == "(none)":
                percentages = group_df.sum() / len(group_df) * 100
                fig, ax = plt.subplots()
                percentages.sort_values().plot(kind="barh", ax=ax)
                for i, v in enumerate(percentages.sort_values()):
                    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
                ax.set_title(f"{group_name} – % Selected")
                st.pyplot(fig)
            else:
                grouped = df.groupby(segment_col)[columns].apply(lambda x: x.notna().sum()).T
                grouped_pct = grouped.divide(df[segment_col].value_counts(), axis=1) * 100
                fig, ax = plt.subplots()
                grouped_pct.T.plot(kind="bar", ax=ax)
                ax.set_title(f"{group_name} – % Selected by {segment_col}")
                st.pyplot(fig)

        # Matrix Group UI
        st.markdown("### ➕ Create Matrix Group")
        matrix_candidates = [col for col, typ in edited_types.items() if typ == "matrix"]
        matrix_group_name = st.text_input("New Matrix Group Name")
        matrix_selected_cols = st.multiselect("Select matrix columns", matrix_candidates)
        if st.button("Add Matrix Group"):
            if matrix_group_name and matrix_selected_cols:
                st.session_state["matrix_map"][matrix_group_name] = matrix_selected_cols
                st.success(f"Group '{matrix_group_name}' added!")

        # Show charts for matrix groups
        for group_name, columns in st.session_state["matrix_map"].items():
            st.markdown(f"#### 🧪 Matrix Group: {group_name}")
            if segment_col == "(none)":
                means = df[columns].mean()
                fig, ax = plt.subplots()
                means.sort_values().plot(kind="barh", ax=ax)
                for i, v in enumerate(means.sort_values()):
                    ax.text(v + 0.1, i, f"{v:.2f}", va="center")
                ax.set_title(f"{group_name} – Average Scores")
                st.pyplot(fig)
            else:
                grouped = df.groupby(segment_col)[columns].mean()
                fig, ax = plt.subplots()
                grouped.plot(kind="bar", ax=ax)
                ax.set_title(f"{group_name} – Avg Scores by {segment_col}")
                st.pyplot(fig)

    else:
        st.info("Please upload a file to continue.")
