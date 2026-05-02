import pandas as pd
import random

# 17 distinct inconsistency types — meets the 15-20 requirement
ALL_STRATEGIES = [
    "null_value",       "duplicate_row",     "wrong_type",
    "negative_value",   "future_date",       "empty_string",
    "outlier_value",    "extra_whitespace",  "mixed_case",
    "zero_value",       "corrupt_id",        "wrong_format_date",
    "duplicate_id",     "invalid_email",     "invalid_phone",
    "html_injection",   "encoding_artifact",
]


def inject_inconsistencies(df, count=17):
    df   = df.copy()
    cols = df.columns.tolist()
    log  = []

    num_cols   = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    date_cols  = [c for c in cols if "date" in c.lower() or "time" in c.lower()]
    id_cols    = [c for c in cols if c.lower().endswith("_id") or c.lower() == "id"]
    email_cols = [c for c in cols if "email" in c.lower()]
    phone_cols = [c for c in cols if "phone" in c.lower()]
    text_cols  = [c for c in cols if c not in num_cols + date_cols + id_cols]

    # Pick strategies — rotate through all 17 types
    picks = random.sample(ALL_STRATEGIES, min(count, len(ALL_STRATEGIES)))
    if len(picks) < count:
        picks += random.choices(ALL_STRATEGIES, k=count - len(picks))
    random.shuffle(picks)

    for strategy in picks[:count]:
        row = random.randint(0, len(df) - 1)
        try:
            if strategy == "null_value":
                col = random.choice(cols)
                df.at[row, col] = None
                log.append({"row": row, "col": col, "type": "null_value"})

            elif strategy == "duplicate_row":
                df = pd.concat([df, df.iloc[[row]]], ignore_index=True)
                log.append({"row": row, "col": "—", "type": "duplicate_row"})

            elif strategy == "wrong_type" and num_cols:
                col = random.choice(num_cols)
                df[col] = df[col].astype(object)
                df.at[row, col] = "N/A##INVALID_DATA"
                log.append({"row": row, "col": col, "type": "wrong_type"})

            elif strategy == "negative_value" and num_cols:
                col = random.choice(num_cols)
                df[col] = df[col].astype(object)
                df.at[row, col] = -abs(random.randint(1, 99999))
                log.append({"row": row, "col": col, "type": "negative_value"})

            elif strategy == "future_date" and date_cols:
                col = random.choice(date_cols)
                df.at[row, col] = "2099-12-31"
                log.append({"row": row, "col": col, "type": "future_date"})

            elif strategy == "empty_string" and text_cols:
                col = random.choice(text_cols)
                df.at[row, col] = "   "
                log.append({"row": row, "col": col, "type": "empty_string"})

            elif strategy == "outlier_value" and num_cols:
                col = random.choice(num_cols)
                df[col] = df[col].astype(object)
                df.at[row, col] = random.choice([99999999, -99999999, 0.000001])
                log.append({"row": row, "col": col, "type": "outlier_value"})

            elif strategy == "extra_whitespace" and text_cols:
                col = random.choice(text_cols)
                df.at[row, col] = "  " + str(df.at[row, col]) + "  "
                log.append({"row": row, "col": col, "type": "extra_whitespace"})

            elif strategy == "mixed_case" and text_cols:
                col = random.choice(text_cols)
                df.at[row, col] = str(df.at[row, col]).swapcase()
                log.append({"row": row, "col": col, "type": "mixed_case"})

            elif strategy == "zero_value" and num_cols:
                col = random.choice(num_cols)
                df[col] = df[col].astype(object)
                df.at[row, col] = 0
                log.append({"row": row, "col": col, "type": "zero_value"})

            elif strategy == "corrupt_id" and id_cols:
                col = random.choice(id_cols)
                df.at[row, col] = "??CORRUPT??"
                log.append({"row": row, "col": col, "type": "corrupt_id"})

            elif strategy == "wrong_format_date" and date_cols:
                col = random.choice(date_cols)
                df.at[row, col] = f"{random.randint(1,28)}/{random.randint(1,12)}/{random.randint(2019,2024)}"
                log.append({"row": row, "col": col, "type": "wrong_format_date"})

            elif strategy == "duplicate_id" and id_cols:
                col = random.choice(id_cols)
                src = random.randint(0, len(df) - 1)
                df.at[row, col] = df.at[src, col]
                log.append({"row": row, "col": col, "type": "duplicate_id"})

            elif strategy == "invalid_email" and email_cols:
                col = random.choice(email_cols)
                df.at[row, col] = "not_an_email_@@@"
                log.append({"row": row, "col": col, "type": "invalid_email"})

            elif strategy == "invalid_phone" and phone_cols:
                col = random.choice(phone_cols)
                df.at[row, col] = "000"
                log.append({"row": row, "col": col, "type": "invalid_phone"})

            elif strategy == "html_injection" and text_cols:
                col = random.choice(text_cols)
                df.at[row, col] = "<script>alert('xss')</script>"
                log.append({"row": row, "col": col, "type": "html_injection"})

            elif strategy == "encoding_artifact" and text_cols:
                col = random.choice(text_cols)
                df.at[row, col] = str(df.at[row, col]) + " ñ£¥"
                log.append({"row": row, "col": col, "type": "encoding_artifact"})

            else:
                col = random.choice(cols)
                df.at[row, col] = None
                log.append({"row": row, "col": col, "type": "null_fallback"})

        except Exception as e:
            log.append({"row": row, "col": "—", "type": f"error:{e}"})

    print(f"  Injected {len(log)} inconsistencies into dataset.")
    return df, log