def dataframe_memory_mb(frame):
    return float(frame.memory_usage(deep=True).sum() / (1024 * 1024))
