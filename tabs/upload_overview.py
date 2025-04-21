
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

        # Initialize group state
        st.session_state.setdefault("checkbox_map", {})
        st.session_state.setdefault("matrix_map", {})
        st.session_state.setdefault("show_checkbox_form", False)
        st.session_state.setdefault("show_matrix_form", False)

        st.subheader("🧩 Group Checkbox & Matrix Questions")

        # Checkbox group UI
        st.markdown("### ✅ Existing Checkbox Groups")
        for group_name, columns in st.session_state["checkbox_map"].items():
            st.markdown(f"#### {group_name}")
            group_df = df[columns].notna().astype(int)
            if segment_col == "(none)":
                percentages = group_df.sum() / len(group_df) * 100
                fig, ax = plt.subplots()
                percentages_sorted = percentages.sort_values()
                percentages_sorted.plot(kind="barh", ax=ax)
                for i, v in enumerate(percentages_sorted):
                    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
                                ax.set_title(f"{group_name} – % Selected")
                st.pyplot(fig)
            else:
                grouped = df.groupby(segment_col)[columns].apply(lambda x: x.notna().sum()).T
                grouped_pct = grouped.divide(df[segment_col].value_counts(), axis=1) * 100
                fig, ax = plt.subplots()
                grouped_pct.T.plot(kind="bar", ax=ax)
                for container in ax.containers:
                    ax.bar_label(container, fmt="%.1f%%")
                ax.set_title(f"{group_name} – % Selected by {segment_col}")
                st.pyplot(fig)

        
        with st.expander("➕ Create New Checkbox Group", expanded=False):
            cb_group_name = st.text_input("Checkbox Group Name", key="cb_group_name")
            cb_candidates = [col for col, typ in edited_types.items() if typ == "checkbox"]
            cb_selected_cols = st.multiselect("Select checkbox columns", cb_candidates, key="cb_columns")
            if st.button("Add Checkbox Group", key="cb_add_button"):
                if cb_group_name and cb_selected_cols:
                    st.session_state["checkbox_map"][cb_group_name] = cb_selected_cols
                    st.success(f"Added checkbox group: '{cb_group_name}'")
    
            st.session_state["show_checkbox_form"] = True

        if st.session_state["show_checkbox_form"]:
            with st.form("checkbox_group_form"):
                st.markdown("### ➕ New Checkbox Group")
                cb_group_name = st.text_input("Group Name")
                cb_candidates = [col for col, typ in edited_types.items() if typ == "checkbox"]
                cb_selected_cols = st.multiselect("Select checkbox columns", cb_candidates)
                submitted = st.form_submit_button("Add Group")
                if submitted and cb_group_name and cb_selected_cols:
                    st.session_state["checkbox_map"][cb_group_name] = cb_selected_cols
                    st.session_state["show_checkbox_form"] = False
                    st.success(f"Added group '{cb_group_name}'")

        # Matrix group UI
        st.markdown("### 🧪 Existing Matrix Groups")
        for group_name, columns in st.session_state["matrix_map"].items():
            st.markdown(f"#### {group_name}")
            if segment_col == "(none)":
                means = df[columns].mean()
                fig, ax = plt.subplots()
                means_sorted = means.sort_values()
                means_sorted.plot(kind="barh", ax=ax)
                for i, v in enumerate(means_sorted):
                    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
                                ax.set_title(f"{group_name} – Avg Score (%)")
                st.pyplot(fig)
            else:
                grouped = df.groupby(segment_col)[columns].mean() * 20  # scale 1-5 to %
                fig, ax = plt.subplots()
                grouped.plot(kind="bar", ax=ax)
                for container in ax.containers:
                    ax.bar_label(container, fmt="%.1f%%")
                ax.set_title(f"{group_name} – Avg Score (%) by {segment_col}")
                st.pyplot(fig)

        
        with st.expander("➕ Create New Matrix Group", expanded=False):
            mtx_group_name = st.text_input("Matrix Group Name", key="matrix_group_name")
            mtx_candidates = [col for col, typ in edited_types.items() if typ == "matrix"]
            mtx_selected_cols = st.multiselect("Select matrix columns", mtx_candidates, key="matrix_columns")
            if st.button("Add Matrix Group", key="matrix_add_button"):
                if mtx_group_name and mtx_selected_cols:
                    st.session_state["matrix_map"][mtx_group_name] = mtx_selected_cols
                    st.success(f"Added matrix group: '{mtx_group_name}'")
    
            st.session_state["show_matrix_form"] = True

        if st.session_state["show_matrix_form"]:
            with st.form("matrix_group_form"):
                st.markdown("### ➕ New Matrix Group")
                mtx_group_name = st.text_input("Group Name", key="mtx_name")
                mtx_candidates = [col for col, typ in edited_types.items() if typ == "matrix"]
                mtx_selected_cols = st.multiselect("Select matrix columns", mtx_candidates)
                submitted = st.form_submit_button("Add Group")
                if submitted and mtx_group_name and mtx_selected_cols:
                    st.session_state["matrix_map"][mtx_group_name] = mtx_selected_cols
                    st.session_state["show_matrix_form"] = False
                    st.success(f"Added group '{mtx_group_name}'")
    else:
        st.info("Please upload a file to continue.")
