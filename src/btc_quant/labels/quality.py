def label_quality_summary(labels):
    counts = labels["target"].value_counts(dropna=False).to_dict() if "target" in labels else {}
    return {"rows": int(len(labels)), "class_counts": {str(k): int(v) for k, v in counts.items()}, "status": "PASS" if len(counts) >= 2 else "FAIL"}

