# 🏥 ClinicalFlow Analytics Platform

> End-to-end clinical data engineering pipeline transforming raw EHR data into FHIR-aligned, analytics-ready models with automated quality validation and executive dashboards.

---

## 📊 Project Overview

ClinicalFlow is a production-style healthcare analytics platform that simulates a real hospital data engineering workflow. It ingests raw Electronic Health Record (EHR) data, transforms it through a layered dbt architecture aligned to FHIR standards, validates quality automatically, orchestrates the pipeline, and delivers insights through Power BI dashboards benchmarked against CMS quality measures.

---

## 🏗️ Architecture

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Synthetic EHR data generation + pipeline orchestration |
| PostgreSQL | Data warehouse (raw + staging + mart layers) |
| dbt Core | SQL transformations, testing, lineage documentation |
| Great Expectations | Automated data quality validation |
| Apache Airflow | Pipeline orchestration (DAG designed, Linux-ready) |
| Power BI | Clinical dashboards and executive reporting |
| GitHub | Version control and portfolio |

---

## 📁 Project Structure

---

## 📈 Dashboards

| Dashboard | Key Metrics |
|---|---|
| Patient & Encounter Overview | Total encounters, encounter mix, monthly admissions trend |
| Length of Stay Analysis | Avg LOS by department, LOS categories, LOS by diagnosis |
| 30-Day Readmission Analysis | Readmission rate by diagnosis and department |
| Quality Metrics | Mortality rate, encounter mix, deaths by diagnosis |
| Insurance & Demographics | Payer mix, gender split, age distribution |

---

## 🔍 Data Quality

### dbt Tests (32 checks)
- Uniqueness checks on all primary keys
- Not null validation on critical fields
- Accepted values for categorical columns
- Referential integrity between tables
- Custom clinical range tests (LOS, vitals, ICD-10 format)

### Great Expectations (29 checks)
- Patient ID uniqueness and null validation
- ICD-10 code format validation
- Vital signs within clinical ranges
- Medication route and status validation
- Row count thresholds

---

## 🏥 Clinical Domain Knowledge

- **FHIR Alignment** — Models mapped to Patient, Encounter, Observation, MedicationRequest resources
- **ICD-10 Categorization** — Diagnosis codes mapped to clinical chapters
- **CMS Benchmarks** — 30-day readmission rate benchmarked against CMS 15% threshold
- **HEDIS Metrics** — Quality measures aligned to HEDIS reporting standards
- **LOS Categories** — Short/Medium/Long Stay buckets for clinical operations reporting

---

## 🚀 How To Run

### Prerequisites
- Python 3.12+
- PostgreSQL 17
- dbt Core
- Great Expectations

### Setup

### Pipeline Output

---

## 📊 Key Results

- **50,000** synthetic EHR records across 4 clinical domains
- **8 dbt models** across staging, intermediate, and mart layers
- **32 automated tests** validating data integrity and clinical rules
- **29 quality checks** validating raw data before pipeline entry
- **5 Power BI dashboards** delivering clinical insights
- **Full pipeline** runs end-to-end in under 30 seconds

---

## 🎯 Skills Demonstrated

- Healthcare data engineering (EHR, FHIR, ICD-10, HEDIS, CMS)
- ETL pipeline design and implementation
- dbt layered architecture (staging → intermediate → marts)
- Automated data quality validation
- Pipeline orchestration (Airflow DAG design)
- Clinical dashboard development
- SQL transformations and optimization
- Python scripting for data engineering

---

*Built as a portfolio project demonstrating production-style healthcare data engineering practices.*

