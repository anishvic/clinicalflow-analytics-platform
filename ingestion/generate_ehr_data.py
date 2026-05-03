# ============================================================
# ClinicalFlow Analytics Platform
# Script: generate_ehr_data.py
# Purpose: Generate 50,000 rows of synthetic EHR data
#          and load it into PostgreSQL
# ============================================================

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text
import random
from datetime import datetime, timedelta

# ---- SETUP ----
fake = Faker()
random.seed(42)
Faker.seed(42)

# Connect to your PostgreSQL database
engine = create_engine("postgresql://postgres:postgres123@localhost:5432/clinicalflow")

print("✅ Connected to PostgreSQL!")

# ============================================================
# 1. PATIENTS TABLE
# ============================================================

def generate_patients(n=5000):
    patients = []
    for i in range(n):
        patients.append({
            "patient_id": f"PAT{str(i+1).zfill(5)}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
            "gender": random.choice(["M", "F"]),
            "race": random.choice(["White", "Black", "Asian", "Hispanic", "Other"]),
            "address": fake.address().replace("\n", ", "),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "phone": fake.phone_number(),
            "insurance_type": random.choice(["Medicare", "Medicaid", "Commercial", "Self-Pay"]),
            "created_at": fake.date_time_between(start_date="-5y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(patients)

# ============================================================
# 2. ENCOUNTERS TABLE
# ============================================================

ICD10_CODES = [
    ("I10", "Hypertension"),
    ("E11.9", "Type 2 Diabetes"),
    ("J18.9", "Pneumonia"),
    ("I50.9", "Heart Failure"),
    ("N18.3", "Chronic Kidney Disease"),
    ("J44.1", "COPD"),
    ("I21.9", "Acute MI"),
    ("F32.9", "Depression"),
    ("M54.5", "Low Back Pain"),
    ("Z23", "Vaccination"),
]

def generate_encounters(patients_df, n=20000):
    encounters = []
    patient_ids = patients_df["patient_id"].tolist()

    for i in range(n):
        admission_date = fake.date_time_between(start_date="-3y", end_date="now")
        los = random.randint(1, 15)
        discharge_date = admission_date + timedelta(days=los)
        icd = random.choice(ICD10_CODES)

        encounters.append({
            "encounter_id": f"ENC{str(i+1).zfill(6)}",
            "patient_id": random.choice(patient_ids),
            "admission_date": admission_date.strftime("%Y-%m-%d %H:%M:%S"),
            "discharge_date": discharge_date.strftime("%Y-%m-%d %H:%M:%S"),
            "length_of_stay": los,
            "encounter_type": random.choice(["Inpatient", "Outpatient", "Emergency"]),
            "primary_diagnosis_code": icd[0],
            "primary_diagnosis_desc": icd[1],
            "discharge_disposition": random.choice([
                "Home", "SNF", "Rehab", "Expired", "AMA"
            ]),
            "attending_physician": fake.name(),
            "department": random.choice([
                "Cardiology", "Neurology", "Orthopedics",
                "General Medicine", "Emergency", "Oncology"
            ]),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(encounters)

# ============================================================
# 3. VITALS TABLE
# ============================================================

def generate_vitals(encounters_df, n=15000):
    vitals = []
    encounter_ids = encounters_df["encounter_id"].tolist()

    for i in range(n):
        vitals.append({
            "vital_id": f"VIT{str(i+1).zfill(6)}",
            "encounter_id": random.choice(encounter_ids),
            "recorded_at": fake.date_time_between(start_date="-3y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "systolic_bp": random.randint(90, 180),
            "diastolic_bp": random.randint(60, 120),
            "heart_rate": random.randint(55, 110),
            "temperature": round(random.uniform(97.0, 103.0), 1),
            "oxygen_saturation": random.randint(92, 100),
            "respiratory_rate": random.randint(12, 25),
            "weight_kg": round(random.uniform(45.0, 150.0), 1),
            "height_cm": round(random.uniform(150.0, 200.0), 1),
        })
    return pd.DataFrame(vitals)

# ============================================================
# 4. MEDICATIONS TABLE
# ============================================================

MEDICATIONS = [
    ("Metformin", "500mg", "Oral"),
    ("Lisinopril", "10mg", "Oral"),
    ("Atorvastatin", "20mg", "Oral"),
    ("Aspirin", "81mg", "Oral"),
    ("Amoxicillin", "500mg", "Oral"),
    ("Insulin Glargine", "10 units", "Subcutaneous"),
    ("Furosemide", "40mg", "IV"),
    ("Metoprolol", "25mg", "Oral"),
    ("Omeprazole", "20mg", "Oral"),
    ("Morphine", "2mg", "IV"),
]

def generate_medications(encounters_df, n=10000):
    medications = []
    encounter_ids = encounters_df["encounter_id"].tolist()

    for i in range(n):
        med = random.choice(MEDICATIONS)
        start_date = fake.date_time_between(start_date="-3y", end_date="now")
        medications.append({
            "medication_id": f"MED{str(i+1).zfill(6)}",
            "encounter_id": random.choice(encounter_ids),
            "medication_name": med[0],
            "dose": med[1],
            "route": med[2],
            "frequency": random.choice(["Once daily", "Twice daily", "Every 8 hrs", "PRN"]),
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "prescribing_physician": fake.name(),
            "status": random.choice(["Active", "Discontinued", "Completed"]),
        })
    return pd.DataFrame(medications)

# ============================================================
# 5. LOAD EVERYTHING INTO POSTGRESQL
# ============================================================

def load_to_postgres(df, table_name):
    # Drop table with CASCADE to handle dependent views
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
        conn.commit()
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Loaded {len(df)} rows into table: {table_name}")

# ---- RUN EVERYTHING ----
print("\n🏥 Generating synthetic EHR data...\n")

print("👤 Generating patients...")
patients_df = generate_patients(5000)

print("🏨 Generating encounters...")
encounters_df = generate_encounters(patients_df, 20000)

print("💉 Generating vitals...")
vitals_df = generate_vitals(encounters_df, 15000)

print("💊 Generating medications...")
medications_df = generate_medications(encounters_df, 10000)

print("\n📤 Loading data into PostgreSQL...\n")
load_to_postgres(patients_df, "raw_patients")
load_to_postgres(encounters_df, "raw_encounters")
load_to_postgres(vitals_df, "raw_vitals")
load_to_postgres(medications_df, "raw_medications")

print("\n🎉 Done! All EHR data loaded into clinicalflow database.")
print(f"   Patients:   {len(patients_df):,}")
print(f"   Encounters: {len(encounters_df):,}")
print(f"   Vitals:     {len(vitals_df):,}")
print(f"   Medications:{len(medications_df):,}")