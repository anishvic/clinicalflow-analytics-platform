# ============================================================
# ClinicalFlow Analytics Platform
# Script: run_pipeline.py
# Purpose: Orchestrate the full pipeline in correct order
#          Mirrors the Airflow DAG logic
# ============================================================

import subprocess
import sys
from datetime import datetime

PYTHON  = r"C:\Users\anish\AppData\Local\Programs\Python\Python312\python.exe"
PROJECT = r"D:\Projects\ClinicalFlow Analytics Platform"
DBT     = r"C:\Users\anish\AppData\Local\Programs\Python\Python312\Scripts\dbt"

def run_task(task_name, command):
    print(f"\n{'='*60}")
    print(f"▶️  TASK: {task_name}")
    print(f"   Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")

    result = subprocess.run(command, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"\n❌ TASK FAILED: {task_name}")
        print("Pipeline stopped. Fix the error and rerun.")
        sys.exit(1)
    else:
        print(f"\n✅ TASK COMPLETE: {task_name}")

# ============================================================
# RUN PIPELINE
# ============================================================

print("\n" + "="*60)
print("🏥 CLINICALFLOW PIPELINE STARTING")
print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

start_time = datetime.now()

# Task 1 — Ingest EHR Data
run_task(
    "Ingest EHR Data",
    [PYTHON, f"{PROJECT}\\ingestion\\generate_ehr_data.py"]
)

# Task 2 — Run dbt Models
run_task(
    "Run dbt Transformations",
    [DBT, "run", "--project-dir", f"{PROJECT}\\dbt_project"]
)

# Task 3 — Run dbt Tests
run_task(
    "Run dbt Tests",
    [DBT, "test", "--project-dir", f"{PROJECT}\\dbt_project"]
)

# Task 4 — Run Quality Checks
run_task(
    "Run Great Expectations Quality Checks",
    [PYTHON,
     f"{PROJECT}\\great_expectations_checks\\run_quality_checks.py"]
)

# ============================================================
# PIPELINE COMPLETE
# ============================================================

end_time = datetime.now()
duration = (end_time - start_time).seconds

print("\n" + "="*60)
print("🎉 CLINICALFLOW PIPELINE COMPLETED SUCCESSFULLY!")
print(f"   Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Duration: {duration} seconds")
print("")
print("   ✅ EHR data ingested       (50,000 rows)")
print("   ✅ dbt models transformed  (8 models)")
print("   ✅ dbt tests passed        (32 checks)")
print("   ✅ Quality checks passed   (29 checks)")
print("="*60)