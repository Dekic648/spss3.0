from scipy import stats

def run_t_test(group1, group2):
    return stats.ttest_ind(group1, group2, nan_policy='omit')
