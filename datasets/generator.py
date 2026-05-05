import pandas as pd
import random
import uuid
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()  # en_US — non-Indian names

# ── Indian cities for India-contextual data ───────────────────────────────────
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat",
    "Lucknow", "Nagpur", "Indore", "Bhopal", "Coimbatore",
    "Kochi", "Patna", "Vadodara", "Agra", "Visakhapatnam",
]
INDIAN_STATES = [
    "Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu",
    "West Bengal", "Gujarat", "Rajasthan", "Uttar Pradesh",
    "Madhya Pradesh", "Bihar", "Punjab", "Haryana", "Odisha",
]
STATUSES   = ["Active", "Inactive", "Pending", "Completed", "Cancelled"]
PAY_MODES  = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash", "Cheque"]
BLOOD      = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def random_date(start_years_ago=3):
    start = datetime.now() - timedelta(days=start_years_ago * 365)
    return (start + timedelta(days=random.randint(0, start_years_ago * 365))).strftime("%Y-%m-%d")


def generate_value(field_name):
    f = field_name.lower()

    # IDs
    if f.endswith("_id") or f == "id":
        return str(uuid.uuid4())[:8].upper()
    if "passport" in f:  return fake.bothify("??#######").upper()
    if "license"  in f:  return fake.bothify("??-##-####-#######")
    if "ifsc"     in f:  return fake.bothify("????0######")

    # Names — NON-INDIAN (en_US faker)
    if "full_name" in f or "holder_name" in f or "owner_name" in f or "manager_name" in f:
        return fake.name()
    if "hotel_name" in f or "hospital_name" in f or "plant_name" in f:
        return fake.company()
    if "name" in f:      return fake.name()

    # Contact
    if "email"   in f:   return fake.email()
    if "phone"   in f:   return fake.numerify("9#########")  # ← FIXED: Indian 10-digit

    # Dates
    if "timestamp" in f or "start_time" in f or "end_time" in f:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "date" in f or "_dt" in f:
        return random_date()

    # Money
    if any(k in f for k in ("amount", "price", "cost", "fee", "balance", "salary",
                             "revenue", "rent", "charge", "fine", "emi", "principal")):
        return round(random.uniform(500, 80000), 2)
    if "interest_rate" in f: return round(random.uniform(6.5, 18.5), 2)
    if "discount"      in f: return round(random.uniform(0, 50), 2)
    if "tax"           in f: return round(random.uniform(0, 5000), 2)

    # Numeric counts
    if any(k in f for k in ("qty", "count", "rooms", "trips", "refill", "sms")):
        return random.randint(1, 500)
    if "capacity_mw" in f:   return round(random.uniform(100, 5000), 1)
    if "capacity"    in f:   return round(random.uniform(100, 50000), 1)
    if "tons"        in f or "yield" in f: return round(random.uniform(1, 5000), 2)
    if "area"        in f:   return round(random.uniform(0.5, 500), 2)
    if "distance"    in f or "km" in f: return round(random.uniform(5, 3000), 1)
    if "duration"    in f or "hours_used" in f: return round(random.uniform(1, 200), 1)
    if "uptime"      in f or "efficiency" in f: return round(random.uniform(70, 99.9), 2)
    if any(k in f for k in ("pct", "percent", "attendance", "cgpa")):
        return round(random.uniform(0, 100), 2)
    if "rating"      in f:   return round(random.uniform(1.0, 5.0), 1)
    if "score"       in f:   return round(random.uniform(1.0, 5.0), 2)
    if "marks"       in f:   return random.randint(0, 100)
    if "age"         in f:   return random.randint(18, 75)
    if "experience"  in f:   return random.randint(1, 35)
    if "year"        in f:   return random.randint(2000, 2024)
    if "weight"      in f or "kg" in f: return round(random.uniform(0.5, 5000), 2)
    if "fuel_used"   in f:   return round(random.uniform(10, 800), 2)
    if "toll"        in f:   return round(random.uniform(50, 2000), 2)
    if "delay"       in f:   return round(random.uniform(0, 72), 2)
    if "data_used"   in f or "data_gb" in f: return round(random.uniform(0.1, 150), 2)
    if "units"       in f:   return round(random.uniform(50, 2000), 2)
    if "vehicle_count" in f: return random.randint(0, 2000)
    if "avg_speed"   in f:   return round(random.uniform(5, 120), 1)
    if "visitors"    in f:   return random.randint(50, 10000)
    if "battery"     in f:   return random.randint(1, 100)
    if "credit_score" in f:  return random.randint(300, 900)
    if "risk_score"  in f:   return random.randint(1, 100)
    if "overdue"     in f:   return random.randint(0, 365)
    if "tenure"      in f:   return random.choice([12, 24, 36, 48, 60, 84, 120])
    if "attempt"     in f:   return random.randint(1, 3)
    if "entry_fee"   in f:   return random.choice([0, 20, 50, 100, 250, 500])
    if "star_rating" in f:   return random.choice([1, 2, 3, 4, 5])
    if "mw"          in f:   return round(random.uniform(0, 500), 2)

    # Booleans
    if any(k in f for k in ("fragile", "certified", "roaming", "smart_meter", "verified")):
        return random.choice([True, False])

    # Categoricals
    if "blood_group" in f:   return random.choice(BLOOD)
    if "gender"      in f:   return random.choice(["Male", "Female", "Other"])
    if "status"      in f:   return random.choice(STATUSES)
    if "payment_mode" in f:  return random.choice(PAY_MODES)
    if "city"        in f or "origin" in f or "destination" in f:
        return random.choice(INDIAN_CITIES)              # ← FIXED: Indian cities
    if "state"       in f:   return random.choice(INDIAN_STATES)
    if "grade"       in f:   return random.choice(["A+", "A", "B+", "B", "C", "D", "F"])
    if "rating"      in f:   return round(random.uniform(1.0, 5.0), 1)
    if "month"       in f:   return random.choice(["Jan","Feb","Mar","Apr","May","Jun",
                                                    "Jul","Aug","Sep","Oct","Nov","Dec"])
    if "txn_type"    in f:   return random.choice(["Credit", "Debit", "Transfer", "Refund"])
    if "loan_type"   in f:   return random.choice(["Home Loan","Personal Loan","Education Loan",
                                                    "Vehicle Loan","Business Loan"])
    if "account_type" in f:  return random.choice(["Savings","Current","Salary","NRI"])
    if "channel"     in f:   return random.choice(["Mobile App","Web","Branch","ATM","Agent"])
    if "category"    in f:   return random.choice(["Electronics","Clothing","Food",
                                                    "Furniture","Sports","Books"])
    if "department"  in f:   return random.choice(["Engineering","Medicine","Arts",
                                                    "Commerce","Science","Management"])
    if "vehicle_type" in f:  return random.choice(["Truck","Mini Truck","Bike","Tempo"])
    if "carrier"     in f:   return random.choice(["FedEx","DHL","DTDC","BlueDart","Delhivery"])
    if "energy_type" in f or (f == "type" and "plant" in f):
        return random.choice(["Solar","Wind","Thermal","Hydro","Nuclear"])
    if "soil_type"   in f:   return random.choice(["Alluvial","Black","Red","Laterite"])
    if "irrigation"  in f:   return random.choice(["Drip","Sprinkler","Canal","Borewell"])
    if "crop_name"   in f or "crop_type" in f:
        return random.choice(["Rice","Wheat","Maize","Cotton","Sugarcane","Soybean"])
    if "severity"    in f:   return random.choice(["Low","Medium","High","Critical"])
    if "priority"    in f:   return random.choice(["Low","Medium","High","Urgent"])
    if "purpose"     in f:   return random.choice(["Leisure","Business","Medical","Education"])
    if "nationality" in f:   return random.choice(["American","British","German","French",
                                                    "Australian","Canadian","Japanese"])
    if "network_type" in f:  return random.choice(["2G","3G","4G","5G"])
    if "frequency_band" in f:return random.choice(["700 MHz","900 MHz","1800 MHz","2600 MHz"])
    if "room_type"   in f:   return random.choice(["Standard","Deluxe","Suite","Executive"])
    if "cause"       in f:   return random.choice(["Technical Fault","Weather","Maintenance","Overload"])
    if "weather"     in f:   return random.choice(["Clear","Cloudy","Rainy","Foggy","Stormy"])
    if "congestion"  in f:   return random.choice(["Free Flow","Light","Moderate","Heavy"])
    if "ward"        in f:   return f"Ward {random.randint(1, 200)}"
    if "zone"        in f:   return random.choice(["Zone A","Zone B","Zone C","Zone D"])
    if "region"      in f:   return random.choice(["North","South","East","West","Central"])
    if "semester"    in f:   return random.choice(["Sem 1","Sem 2","Sem 3","Sem 4","Sem 5","Sem 6"])
    if "drug_name"   in f:   return fake.word().capitalize() + random.choice([" XR"," SR",""])
    if "frequency"   in f:   return random.choice(["Once daily","Twice daily","Thrice daily","SOS"])
    if "notes"       in f or "description" in f: return fake.sentence(nb_words=8)
    if "condition"   in f:   return random.choice(["Excellent","Good","Fair","Poor"])
    if "brand"       in f:   return random.choice(["Samsung","Nike","Bosch","LG","Adidas","Sony"])
    if "document_type" in f: return random.choice(["Aadhaar","PAN","Passport","Voter ID"])
    if "flags"       in f:   return random.choice(["None","Suspicious","High Value","Duplicate"])
    if "amenities"   in f:   return ",".join(random.sample(["WiFi","Pool","Gym","Spa","Restaurant"],k=3))

    # Fallback
    return fake.word().capitalize()


def generate_dataset(entity_config, rows=90_000, verbose=True):
    if verbose:
        print(f"  Generating {rows:,} rows for entity: {entity_config['name']} ...")
    records = [
        {field: generate_value(field) for field in entity_config["fields"]}
        for _ in range(rows)
    ]
    return pd.DataFrame(records)


def save_dataset(df, entity_config, sector_name, base_dir="datasets/generated"):
    path = os.path.join(base_dir, sector_name)
    os.makedirs(path, exist_ok=True)

    fmt  = entity_config["format"]
    name = entity_config["name"].lower()

    # ── Map format label to correct file extension ────────────────────────────
    ext_map = {
        "csv":     "csv",
        "json":    "json",
        "excel":   "xlsx",      # ← KEY FIX: "excel" label → ".xlsx" extension
        "parquet": "parquet",
    }
    ext = ext_map.get(fmt, fmt)   # fallback to fmt itself if unknown
    fp  = os.path.join(path, f"{name}.{ext}")

    if   fmt == "csv":     df.to_csv(fp, index=False)
    elif fmt == "json":    df.to_json(fp, orient="records", indent=2)
    elif fmt == "excel":   df.to_excel(fp, index=False, engine="openpyxl")
    elif fmt == "parquet": df.to_parquet(fp, index=False, engine="pyarrow")
    else: raise ValueError(f"Unsupported format: {fmt}")

    size_mb = os.path.getsize(fp) / (1024 * 1024)
    print(f"  Saved: {fp}  ({len(df):,} rows | {size_mb:.1f} MB)")
    return fp