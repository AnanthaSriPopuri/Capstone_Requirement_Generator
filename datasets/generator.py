import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()   # Default = English, non-Indian names

def random_date(start_years_ago=3):
    start = datetime.now() - timedelta(days=start_years_ago*365)
    return (start + timedelta(days=random.randint(0, start_years_ago*365))).strftime("%Y-%m-%d")

def generate_value(field_name):
    f = field_name.lower()
    if "id" in f:             return str(uuid.uuid4())[:8].upper()
    elif "name" in f:         return fake.name()
    elif "email" in f:        return fake.email()
    elif "phone" in f:        return fake.phone_number()
    elif "date" in f:         return random_date()
    elif "age" in f:          return random.randint(18, 75)
    elif "amount" in f or "price" in f or "cost" in f or "fee" in f or "balance" in f:
        return round(random.uniform(100, 80000), 2)
    elif "qty" in f or "count" in f or "units" in f:
        return random.randint(1, 500)
    elif "pct" in f or "rate" in f:
        return round(random.uniform(0.1, 99.9), 2)
    elif "status" in f:       return random.choice(["Active","Inactive","Pending","Completed","Cancelled"])
    elif "gender" in f:       return random.choice(["Male","Female","Other"])
    elif "city" in f:         return fake.city()
    elif "location" in f:     return fake.address().replace("\n", ", ")
    elif "notes" in f or "description" in f: return fake.sentence()
    elif "type" in f:         return fake.word().capitalize()
    elif "grade" in f:        return random.choice(["A","B","C","D","F"])
    elif "rating" in f:       return round(random.uniform(1.0, 5.0), 1)
    elif "kg" in f or "tons" in f or "mw" in f or "gb" in f:
        return round(random.uniform(0.5, 1000.0), 2)
    elif "km" in f:           return round(random.uniform(5, 2000), 1)
    elif "year" in f:         return random.randint(2000, 2024)
    elif "month" in f:        return random.choice(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    else:                     return fake.word()

def generate_dataset(entity_config, rows=90000):
    print(f"  Generating {rows:,} rows for entity: {entity_config['name']} ...")
    records = []
    for _ in range(rows):
        row = {field: generate_value(field) for field in entity_config["fields"]}
        records.append(row)
    return pd.DataFrame(records)

def save_dataset(df, entity_config, sector_name, base_dir="datasets/generated"):
    import os
    path = f"{base_dir}/{sector_name}"
    os.makedirs(path, exist_ok=True)
    fmt  = entity_config["format"]
    name = entity_config["name"].lower()
    fp   = f"{path}/{name}.{fmt}"

    if fmt == "csv":
        df.to_csv(fp, index=False)
    elif fmt == "json":
        df.to_json(fp, orient="records", indent=2)
    elif fmt == "excel":
        df.to_excel(fp, index=False)
    elif fmt == "parquet":
        df.to_parquet(fp, index=False)

    print(f"  Saved: {fp}  ({len(df):,} rows)")
    return fp