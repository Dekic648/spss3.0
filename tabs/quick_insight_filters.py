import streamlit as st
import pandas as pd

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

import streamlit as st
import pandas as pd

def show():
    st.header("⚡ Quick Insight Filters")

    df = get_dataframe()
    if df is None:
        st.info("Please upload a file in the Upload tab first.")
        return

    df = df
    filter_col = st.selectbox("Choose a column to filter", df.columns)
    filter_val = st.selectbox("Choose a value", df[filter_col].unique())

    filtered_df = df[df[filter_col] == filter_val]
    st.write("Filtered Data")
    st.dataframe(filtered_df)
