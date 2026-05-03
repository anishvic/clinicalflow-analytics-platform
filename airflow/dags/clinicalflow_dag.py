# ============================================================
# ClinicalFlow Analytics Platform
# DAG: clinicalflow_dag.py
# Purpose: Orchestrate the full EHR data pipeline
#          Runs daily at 6am automatically
# ============================================================

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import sys

# ---- DAG DEFAULT SETTINGS ----
# These settings apply to every task in the DAG

default_args = {
    'owner': 'clinicalflow',
    'depends_on_past': False,        # don't wait for yesterday's run
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,                    # retry once if task fails
    'retry_delay': timedelta(minutes=5),  # wait 5 mins before retry
}

# ---- DEFINE THE DAG ----
dag = DAG(
    'clinicalflow_pipeline',         # DAG name
    default_args=default_args,
    description='ClinicalFlow EHR Analytics Pipeline',
    schedule='0 6 * * *',            # run every day at 6:00 AM
    catchup=False,                   # don't run missed historical runs
    tags=['healthcare', 'ehr', 'analytics'],
)

# ============================================================
# PYTHON PATH
# ============================================================

PYTHON = r"C:\Users\anish\AppData\Local\Programs\Python\Python312\python.exe"
PROJECT = r"D:\Projects\ClinicalFlow Analytics Platform"
DBT     = r"C:\Users\anish\AppData\Local\Programs\Python\Python312\Scripts\dbt"

# ============================================================
# TASK 1 — Generate / Ingest EHR Data
# ============================================================

def run_ingestion():
    print("🏥 Starting EHR data ingestion...")
    result = subprocess.run(
        [PYTHON, f"{PROJECT}\\ingestion\\generate_ehr_data.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Ingestion failed:\n{result.stderr}")
    print("✅ Ingestion complete!")

task_ingestion = PythonOperator(
    task_id='ingest_ehr_data',
    python_callable=run_ingestion,
    dag=dag,
)

# ============================================================
# TASK 2 — Run dbt Transformations
# ============================================================

def run_dbt():
    print("🔧 Running dbt transformations...")
    result = subprocess.run(
        [DBT, "run", "--project-dir",
         f"{PROJECT}\\dbt_project"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")
    print("✅ dbt transformations complete!")

task_dbt_run = PythonOperator(
    task_id='run_dbt_models',
    python_callable=run_dbt,
    dag=dag,
)

# ============================================================
# TASK 3 — Run dbt Tests
# ============================================================

def run_dbt_tests():
    print("🧪 Running dbt data quality tests...")
    result = subprocess.run(
        [DBT, "test", "--project-dir",
         f"{PROJECT}\\dbt_project"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt tests failed:\n{result.stderr}")
    print("✅ All dbt tests passed!")

task_dbt_test = PythonOperator(
    task_id='run_dbt_tests',
    python_callable=run_dbt_tests,
    dag=dag,
)

# ============================================================
# TASK 4 — Run Great Expectations Quality Checks
# ============================================================

def run_quality_checks():
    print("🔍 Running Great Expectations quality checks...")
    result = subprocess.run(
        [PYTHON,
         f"{PROJECT}\\great_expectations_checks\\run_quality_checks.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Quality checks failed:\n{result.stderr}")
    print("✅ All quality checks passed!")

task_quality = PythonOperator(
    task_id='run_quality_checks',
    python_callable=run_quality_checks,
    dag=dag,
)

# ============================================================
# TASK 5 — Pipeline Complete Notification
# ============================================================

def pipeline_complete():
    print("="*60)
    print("🎉 CLINICALFLOW PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"   Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("   All tasks passed:")
    print("   ✅ EHR data ingested")
    print("   ✅ dbt models transformed")
    print("   ✅ dbt tests passed")
    print("   ✅ Quality checks passed")
    print("="*60)

task_complete = PythonOperator(
    task_id='pipeline_complete',
    python_callable=pipeline_complete,
    dag=dag,
)

# ============================================================
# SET TASK ORDER — This is the pipeline sequence
# ============================================================

# >> means "then run next task"
task_ingestion >> task_dbt_run >> task_dbt_test >> task_quality >> task_complete