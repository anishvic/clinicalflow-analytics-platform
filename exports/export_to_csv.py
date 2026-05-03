# ============================================================
# ClinicalFlow Analytics Platform
# Script: export_to_csv.py
# Purpose: Export mart tables to CSV for Power BI
# ============================================================

import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(
    "postgresql://postgres:postgres123@localhost:5432/clinicalflow"
)

# Create exports folder
os.makedirs("exports/data", exist_ok=True)

tables = [
    "mart_inpatient_summary",
    "mart_readmissions",
    "mart_quality_metrics",
    "stg_patients",
    "stg_encounters",
]

print("📤 Exporting mart tables to CSV...\n")

for table in tables:
    df = pd.read_sql(f"select * from {table}", engine)
    path = f"exports/data/{table}.csv"
    df.to_csv(path, index=False)
    print(f"✅ Exported {len(df):,} rows → {path}")

print("\n🎉 All tables exported!")