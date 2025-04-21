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
        st.session_state["df"] = df

        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("⚙️ Auto-Detected + Editable Variable Types")
        auto_types = detect_column_types(df)
        st.session_state["column_types"] = st.session_state.get("column_types", auto_types)
        edited_types = {}
        for col in df.columns:
            default_type = st.session_state["column_types"].get(col, "numeric")
            edited_types[col] = st.selectbox(f"{col}", ["numeric", "likert", "categorical", "checkbox", "matrix", "open_ended"], index=["numeric", "likert", "categorical", "checkbox", "matrix", "open_ended"].index(default_type))
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

        # GROUPING INTERFACE
        st.subheader("🧩 Group Checkbox & Matrix Questions")

        checkbox_map = st.session_state.get("checkbox_map", {})
        matrix_map = st.session_state.get("matrix_map", {})

        # checkbox
        checkbox_candidates = [col for col, typ in edited_types.items() if typ == "checkbox"]
        with st.expander("➕ Create Checkbox Group"):
            group_name = st.text_input("New Checkbox Group Name", key="cb_group_name")
            selected_cols = st.multiselect("Select checkbox columns", checkbox_candidates, key="cb_selected")
            if st.button("Add Checkbox Group"):
                if group_name and selected_cols:
                    for col in selected_cols:
                        checkbox_map[col] = group_name
                    st.session_state["checkbox_map"] = checkbox_map
                    st.success(f"Added group '{group_name}' with {len(selected_cols)} columns")

        # matrix
        matrix_candidates = [col for col, typ in edited_types.items() if typ == "matrix"]
        with st.expander("➕ Create Matrix Group"):
            matrix_name = st.text_input("New Matrix Group Name", key="mtx_group_name")
            matrix_cols = st.multiselect("Select matrix columns", matrix_candidates, key="mtx_selected")
            if st.button("Add Matrix Group"):
                if matrix_name and matrix_cols:
                    for col in matrix_cols:
                        matrix_map[col] = matrix_name
                    st.session_state["matrix_map"] = matrix_map
                    st.success(f"Added matrix group '{matrix_name}'")

        # ✅ Show Checkbox Group Charts
        st.subheader("☑️ Checkbox Group Charts")
        for group_id in set(checkbox_map.values()):
            group_cols = [col for col, grp in checkbox_map.items() if grp == group_id]
            if not group_cols:
                continue
            if segment_col == "(none)":
                pct = (df[group_cols].notnull().sum() / len(df)) * 100
                fig, ax = plt.subplots()
                pct.plot(kind="bar", ax=ax)
                for i, val in enumerate(pct):
                    ax.text(i, val, f"{val:.1f}%", ha='center', va='bottom')
                ax.set_title(f"Checkbox group: {group_id}")
                st.pyplot(fig)
            else:
                grouped = df.groupby(segment_col)[group_cols].apply(lambda x: x.notnull().sum() / len(x) * 100).T
                fig, ax = plt.subplots()
                grouped.plot(kind="bar", ax=ax)
                for c in ax.containers:
                    ax.bar_label(c, fmt="%.1f%%")
                ax.set_title(f"Checkbox group: {group_id} by {segment_col}")
                st.pyplot(fig)

        # ✅ Show Matrix Group Charts
        st.subheader("📐 Matrix Group Charts")
        for group_id in set(matrix_map.values()):
            group_cols = [col for col, grp in matrix_map.items() if grp == group_id]
            if not group_cols:
                continue
            melted = df[group_cols].melt(var_name="Item", value_name="Response")
            if segment_col == "(none)":
                value_counts = pd.crosstab(melted["Item"], melted["Response"], normalize="index") * 100
                fig, ax = plt.subplots()
                value_counts.plot(kind="bar", stacked=True, ax=ax)
                ax.set_title(f"Matrix group: {group_id}")
                ax.set_ylabel("% Response")
                ax.legend(title="Response", bbox_to_anchor=(1.0, 1.0))
                st.pyplot(fig)
            else:
                melted["Segment"] = df[segment_col].repeat(len(group_cols)).reset_index(drop=True)
                grouped = pd.crosstab([melted["Item"], melted["Segment"]], melted["Response"], normalize="index") * 100
                grouped = grouped.reset_index().pivot(index="Item", columns="Segment")
                grouped.columns = ['_'.join(map(str, col)).strip() for col in grouped.columns]
                fig, ax = plt.subplots()
                grouped.plot(kind="bar", stacked=True, ax=ax)
                ax.set_title(f"Matrix group: {group_id} by {segment_col}")
                ax.set_ylabel("% Response")
                ax.legend(title="Segmented Response", bbox_to_anchor=(1.0, 1.0))
                st.pyplot(fig)
    else:
        st.info("Please upload a file to continue.")
