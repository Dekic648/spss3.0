import streamlit as st
import pandas as pd

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

import streamlit as st
import pandas as pd
from utils.simulation_engine import simulate_effect

def show():
    st.header("🎛️ Simulation Playground")

    df = get_dataframe()
    if df is None:
        st.info("Please upload a file in the Upload tab first.")
        return

    df = df

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    column = st.selectbox("Select a numeric column to simulate", numeric_cols)
    delta = st.slider("Change value by", -10.0, 10.0, 1.0)

    simulated = simulate_effect(df, column, delta)
    st.write(f"Preview: {column} + {delta}")
    st.write(simulated.head())
