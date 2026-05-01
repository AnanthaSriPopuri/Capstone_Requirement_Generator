SECTORS = {
    "healthcare": {
        "display": "Healthcare",
        "entities": [
            {"name":"Patient",     "format":"csv",     "fields":["patient_id","full_name","age","gender","diagnosis","admission_date","discharge_date","blood_group","ward"]},
            {"name":"Doctor",      "format":"json",    "fields":["doctor_id","full_name","specialization","hospital_name","experience_years","contact","department"]},
            {"name":"Prescription","format":"excel",   "fields":["rx_id","patient_id","doctor_id","drug_name","dosage_mg","frequency","start_date","end_date","notes"]},
            {"name":"Billing",     "format":"parquet", "fields":["bill_id","patient_id","total_amount","tax","payment_mode","payment_date","insurance_covered","outstanding"]},
        ]
    },
    "retail": {
        "display": "Retail",
        "entities": [
            {"name":"Product",   "format":"csv",     "fields":["product_id","product_name","category","price","cost","brand","stock_qty","supplier_id"]},
            {"name":"Customer",  "format":"json",    "fields":["customer_id","full_name","email","phone","city","loyalty_tier","registration_date","total_orders"]},
            {"name":"Order",     "format":"excel",   "fields":["order_id","customer_id","product_id","quantity","order_date","delivery_date","status","discount_pct"]},
            {"name":"Inventory", "format":"parquet", "fields":["inventory_id","product_id","warehouse_id","qty_available","reorder_level","last_updated","expiry_date"]},
        ]
    },
    "education": {
        "display": "Education",
        "entities": [
            {"name":"Student",    "format":"csv",     "fields":["student_id","full_name","age","gender","course","enrollment_date","cgpa","attendance_pct","city"]},
            {"name":"Faculty",    "format":"json",    "fields":["faculty_id","full_name","department","designation","qualification","experience_years","subjects_taught"]},
            {"name":"Exam",       "format":"excel",   "fields":["exam_id","student_id","subject","marks_obtained","max_marks","exam_date","grade","attempt_number"]},
            {"name":"Fee",        "format":"parquet", "fields":["fee_id","student_id","semester","amount","due_date","paid_date","payment_mode","status","scholarship"]},
        ]
    },
    "logistics": {
        "display": "Logistics",
        "entities": [
            {"name":"Shipment",  "format":"csv",     "fields":["shipment_id","origin","destination","dispatch_date","delivery_date","weight_kg","status","carrier"]},
            {"name":"Driver",    "format":"json",    "fields":["driver_id","full_name","license_no","vehicle_type","vehicle_no","experience_years","rating","city"]},
            {"name":"Warehouse", "format":"excel",   "fields":["warehouse_id","location","capacity_tons","current_load","manager_name","region","last_audit"]},
            {"name":"Route",     "format":"parquet", "fields":["route_id","shipment_id","driver_id","distance_km","fuel_used","toll_charges","delay_hours","weather_condition"]},
        ]
    },
    "agriculture": {
        "display": "Agriculture",
        "entities": [
            {"name":"Farm",      "format":"csv",     "fields":["farm_id","owner_name","location","area_acres","crop_type","soil_type","irrigation_type","state"]},
            {"name":"Crop",      "format":"json",    "fields":["crop_id","farm_id","crop_name","sowing_date","harvest_date","yield_tons","fertilizer_used","pesticide_used"]},
            {"name":"Equipment", "format":"excel",   "fields":["equip_id","farm_id","name","purchase_date","condition","last_service","cost","fuel_type"]},
            {"name":"Sale",      "format":"parquet", "fields":["sale_id","crop_id","buyer_name","quantity_tons","price_per_ton","sale_date","market","payment_status"]},
        ]
    },
    "fintech": {
        "display": "Fintech",
        "entities": [
            {"name":"Account",     "format":"csv",     "fields":["account_id","holder_name","account_type","balance","created_date","status","branch","ifsc_code"]},
            {"name":"Transaction", "format":"json",    "fields":["txn_id","account_id","txn_type","amount","timestamp","merchant","category","channel","status"]},
            {"name":"Loan",        "format":"excel",   "fields":["loan_id","account_id","loan_type","principal","interest_rate","tenure_months","emi","disbursement_date","status"]},
            {"name":"KYC",         "format":"parquet", "fields":["kyc_id","account_id","document_type","verified","verification_date","agent_id","risk_score","flags"]},
        ]
    },
    "telecom": {
        "display": "Telecom",
        "entities": [
            {"name":"Subscriber", "format":"csv",     "fields":["sub_id","full_name","phone","plan","activation_date","city","data_used_gb","calls_made","status"]},
            {"name":"Plan",       "format":"json",    "fields":["plan_id","plan_name","monthly_rent","data_gb","calls_min","sms_count","validity_days","4g_5g"]},
            {"name":"Bill",       "format":"excel",   "fields":["bill_id","sub_id","billing_month","amount","due_date","paid_date","payment_mode","late_fee","status"]},
            {"name":"Tower",      "format":"parquet", "fields":["tower_id","location","city","coverage_radius_km","frequency_band","operator","last_maintenance","uptime_pct"]},
        ]
    },
    "energy": {
        "display": "Energy",
        "entities": [
            {"name":"Plant",      "format":"csv",     "fields":["plant_id","plant_name","type","capacity_mw","location","state","commissioned_year","operator"]},
            {"name":"Meter",      "format":"json",    "fields":["meter_id","consumer_id","plant_id","installation_date","meter_type","status","last_reading","unit"]},
            {"name":"Consumption","format":"excel",   "fields":["cons_id","meter_id","month","units_consumed","peak_units","off_peak_units","bill_amount","reading_date"]},
            {"name":"Outage",     "format":"parquet", "fields":["outage_id","plant_id","start_time","end_time","duration_hrs","cause","affected_consumers","loss_mw"]},
        ]
    },
    "tourism": {
        "display": "Tourism",
        "entities": [
            {"name":"Tourist",    "format":"csv",     "fields":["tourist_id","full_name","nationality","passport_no","arrival_date","departure_date","city_visited","purpose"]},
            {"name":"Hotel",      "format":"json",    "fields":["hotel_id","hotel_name","city","star_rating","rooms","price_per_night","amenities","contact"]},
            {"name":"Booking",    "format":"excel",   "fields":["booking_id","tourist_id","hotel_id","check_in","check_out","rooms_booked","total_amount","status"]},
            {"name":"Attraction", "format":"parquet", "fields":["attr_id","name","city","category","entry_fee","open_hours","avg_visitors_daily","rating"]},
        ]
    },
    "smart_city": {
        "display": "Smart City",
        "entities": [
            {"name":"Sensor",    "format":"csv",     "fields":["sensor_id","type","location","installation_date","status","last_reading","battery_pct","zone"]},
            {"name":"Citizen",   "format":"json",    "fields":["citizen_id","full_name","ward","services_enrolled","complaint_count","rating","registration_date"]},
            {"name":"Complaint", "format":"excel",   "fields":["complaint_id","citizen_id","category","description","raised_date","resolved_date","status","officer_id"]},
            {"name":"Traffic",   "format":"parquet", "fields":["traffic_id","sensor_id","timestamp","vehicle_count","avg_speed_kmh","congestion_level","incident"]},
        ]
    },
}

def get_all_sector_names():
    return list(SECTORS.keys())

def get_random_sector():
    import random
    return random.choice(list(SECTORS.keys()))