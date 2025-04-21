from sklearn.decomposition import PCA

def run_pca(df, cols):
    pca = PCA(n_components=2)
    return pca.fit_transform(df[cols])
