# ============================================================
# ClinicalFlow Analytics Platform
# Script: run_quality_checks.py
# Purpose: Validate raw EHR data using Great Expectations
#          Generates HTML quality report automatically
# ============================================================

import great_expectations as gx
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ---- SETUP ----
print("🔍 Starting ClinicalFlow Data Quality Checks...\n")

# Connect to PostgreSQL
engine = create_engine(
    "postgresql://postgres:postgres123@localhost:5432/clinicalflow"
)

# ============================================================
# HELPER FUNCTION — Load table from PostgreSQL
# ============================================================

def load_table(table_name):
    df = pd.read_sql(f"select * from {table_name}", engine)
    print(f"✅ Loaded {len(df):,} rows from {table_name}")
    return df

# ============================================================
# LOAD ALL 4 RAW TABLES
# ============================================================

print("📥 Loading raw tables from PostgreSQL...\n")
patients_df     = load_table("raw_patients")
encounters_df   = load_table("raw_encounters")
vitals_df       = load_table("raw_vitals")
medications_df  = load_table("raw_medications")

# ============================================================
# SETUP GREAT EXPECTATIONS CONTEXT
# ============================================================

print("\n⚙️  Setting up Great Expectations context...\n")
context = gx.get_context(mode="ephemeral")

# ============================================================
# FUNCTION — Run expectations on a dataframe
# ============================================================

def run_checks(df, suite_name, expectations):
    """
    Run a list of expectations on a dataframe
    Returns results
    """
    # Create data source
    data_source = context.data_sources.add_pandas(name=suite_name)
    data_asset  = data_source.add_dataframe_asset(name=f"{suite_name}_asset")
    batch_def   = data_asset.add_batch_definition_whole_dataframe(
                    f"{suite_name}_batch"
                  )

    # Create expectation suite
    suite = context.suites.add(
        gx.ExpectationSuite(name=f"{suite_name}_suite")
    )

    # Add all expectations
    for expectation in expectations:
        suite.add_expectation(expectation)

    # Create validation definition
    validation_def = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=f"{suite_name}_validation",
            data=batch_def,
            suite=suite
        )
    )

    # Run validation
    batch_params = {"dataframe": df}
    results = validation_def.run(batch_parameters=batch_params)

    return results

# ============================================================
# 1. PATIENTS QUALITY CHECKS
# ============================================================

print("👤 Running patient quality checks...")

patient_expectations = [
    gx.expectations.ExpectColumnToExist(column="patient_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="patient_id"),
    gx.expectations.ExpectColumnValuesToBeUnique(column="patient_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="first_name"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="last_name"),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="gender",
        value_set=["M", "F"]
    ),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="insurance_type",
        value_set=["Medicare", "Medicaid", "Commercial", "Self-Pay"]
    ),
    gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=1000,
        max_value=100000
    ),
]

patient_results = run_checks(patients_df, "patients", patient_expectations)

# ============================================================
# 2. ENCOUNTERS QUALITY CHECKS
# ============================================================

print("🏥 Running encounter quality checks...")

encounter_expectations = [
    gx.expectations.ExpectColumnToExist(column="encounter_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="encounter_id"),
    gx.expectations.ExpectColumnValuesToBeUnique(column="encounter_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="patient_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="admission_date"),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="encounter_type",
        value_set=["Inpatient", "Outpatient", "Emergency"]
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="length_of_stay",
        min_value=0,
        max_value=365
    ),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="discharge_disposition",
        value_set=["Home", "SNF", "Rehab", "Expired", "AMA"]
    ),
]

encounter_results = run_checks(
    encounters_df, "encounters", encounter_expectations
)

# ============================================================
# 3. VITALS QUALITY CHECKS
# ============================================================

print("💉 Running vitals quality checks...")

vitals_expectations = [
    gx.expectations.ExpectColumnToExist(column="vital_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="vital_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="encounter_id"),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="systolic_bp",
        min_value=40,
        max_value=300
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="diastolic_bp",
        min_value=20,
        max_value=200
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="heart_rate",
        min_value=20,
        max_value=250
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="oxygen_saturation",
        min_value=50,
        max_value=100
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="temperature",
        min_value=80,
        max_value=115
    ),
]

vitals_results = run_checks(vitals_df, "vitals", vitals_expectations)

# ============================================================
# 4. MEDICATIONS QUALITY CHECKS
# ============================================================

print("💊 Running medications quality checks...")

medications_expectations = [
    gx.expectations.ExpectColumnToExist(column="medication_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="medication_id"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="encounter_id"),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["Active", "Discontinued", "Completed"]
    ),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="route",
        value_set=["Oral", "IV", "Subcutaneous"]
    ),
]

medications_results = run_checks(
    medications_df, "medications", medications_expectations
)

# ============================================================
# 5. PRINT SUMMARY REPORT
# ============================================================

print("\n" + "="*60)
print("📊 CLINICALFLOW DATA QUALITY REPORT")
print(f"   Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

all_results = {
    "Patients":     patient_results,
    "Encounters":   encounter_results,
    "Vitals":       vitals_results,
    "Medications":  medications_results,
}

total_passed = 0
total_failed = 0

for table_name, results in all_results.items():
    stats       = results.statistics
    passed      = stats["successful_expectations"]
    failed      = stats["unsuccessful_expectations"]
    total       = stats["evaluated_expectations"]
    pct         = stats["success_percent"]
    total_passed += passed
    total_failed += failed

    status = "✅ PASSED" if failed == 0 else "❌ FAILED"
    print(f"\n{status} — {table_name}")
    print(f"   Checks passed: {passed}/{total} ({pct:.1f}%)")

    if failed > 0:
        print(f"   ⚠️  Failed checks: {failed}")

print("\n" + "="*60)
print(f"TOTAL: {total_passed} passed, {total_failed} failed")
if total_failed == 0:
    print("🎉 ALL QUALITY CHECKS PASSED!")
else:
    print(f"⚠️  {total_failed} checks need attention")
print("="*60)