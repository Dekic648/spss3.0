def detect_column_types(df):
    types = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            types[col] = 'categorical'
        elif df[col].nunique() <= 7:
            types[col] = 'likert'
        else:
            types[col] = 'numeric'
    return types
