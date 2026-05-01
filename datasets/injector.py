import pandas as pd
import random
import numpy as np

def inject_inconsistencies(df, count=17):
    df = df.copy()
    cols = df.columns.tolist()
    issues_injected = []

    strategies = [
        "null_value", "duplicate_row", "wrong_type",
        "negative_value", "future_date", "empty_string",
        "outlier_value", "whitespace", "mixed_case"
    ]

    for i in range(count):
        strategy = strategies[i % len(strategies)]
        row_idx  = random.randint(0, len(df) - 1)
        col      = random.choice(cols)

        try:
            if strategy == "null_value":
                df.at[row_idx, col] = None
            elif strategy == "duplicate_row":
                df = pd.concat([df, df.iloc[[row_idx]]], ignore_index=True)
            elif strategy == "wrong_type":
                df.at[row_idx, col] = "N/A##INVALID"
            elif strategy == "negative_value":
                df.at[row_idx, col] = -abs(random.randint(1, 9999))
            elif strategy == "future_date":
                df.at[row_idx, col] = "2099-12-31"
            elif strategy == "empty_string":
                df.at[row_idx, col] = "   "
            elif strategy == "outlier_value":
                df.at[row_idx, col] = 9999999
            elif strategy == "whitespace":
                val = str(df.at[row_idx, col])
                df.at[row_idx, col] = "  " + val + "  "
            elif strategy == "mixed_case":
                val = str(df.at[row_idx, col])
                df.at[row_idx, col] = val.swapcase()

            issues_injected.append({"row": row_idx, "col": col, "type": strategy})
        except Exception:
            pass

    print(f"  Injected {len(issues_injected)} inconsistencies into dataset.")
    return df, issues_injected