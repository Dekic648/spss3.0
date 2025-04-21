def create_segment(df, column):
    return df[column].median(), df[column].apply(lambda x: 'High' if x >= df[column].median() else 'Low')
