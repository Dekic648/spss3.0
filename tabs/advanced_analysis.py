import streamlit as st
import pandas as pd

def get_dataframe():
    if "df" not in st.session_state:
        st.info("Please upload a file in the 'Upload & Overview' tab first.")
        return None
    return st.session_state["df"]

import streamlit as st
import pandas as pd
from utils.clustering_utils import run_kmeans
import matplotlib.pyplot as plt

def show():
    st.header("🧪 Advanced Statistical Analysis")

    df = get_dataframe()
    if df is None:
        st.info("Please upload a file in the Upload tab first.")
        return

    df = df

    st.subheader("Clustering (K-Means)")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_cols = st.multiselect("Select numeric columns for clustering", numeric_cols)

    if len(selected_cols) >= 2:
        n_clusters = st.slider("Select number of clusters", 2, 10, 3)
        clustered_df, model = run_kmeans(df.copy(), selected_cols, n_clusters=n_clusters)

        st.write("Cluster Counts:")
        st.dataframe(clustered_df['Cluster'].value_counts().rename("Count"))

        st.subheader("Cluster Scatterplot")
        x_axis = st.selectbox("X-axis", selected_cols)
        y_axis = st.selectbox("Y-axis", [col for col in selected_cols if col != x_axis])

        fig, ax = plt.subplots()
        for cluster in sorted(clustered_df['Cluster'].unique()):
            cluster_data = clustered_df[clustered_df['Cluster'] == cluster]
            ax.scatter(cluster_data[x_axis], cluster_data[y_axis], label=f"Cluster {cluster}")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.legend()
        st.pyplot(fig)

        st.write("Full Clustered Data:")
        st.dataframe(clustered_df)
    else:
        st.warning("Please select at least 2 numeric columns for clustering.")
