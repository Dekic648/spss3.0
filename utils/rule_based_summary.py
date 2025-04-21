def generate_summary(column, mean_diff, p_val):
    if p_val < 0.05:
        return f"{column} shows a significant difference with a mean difference of {mean_diff:.2f}"
    return ""
