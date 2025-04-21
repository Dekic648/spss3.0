def rank_insights(insights):
    return sorted(insights, key=lambda x: x.get('effect_size', 0), reverse=True)
