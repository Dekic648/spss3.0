import pandas as pd
from sklearn.cluster import KMeans

def run_kmeans(df, selected_cols, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df[selected_cols])
    df['Cluster'] = cluster_labels
    return df, kmeans
