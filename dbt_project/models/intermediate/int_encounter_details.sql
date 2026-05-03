-- ============================================================
-- Model: int_encounter_details
-- Purpose: Join encounters with patient details
-- Creates one wide table with everything needed for reporting
-- ============================================================

with encounters as (

    select * from {{ ref('stg_encounters') }}

),

patients as (

    select * from {{ ref('stg_patients') }}

),

joined as (

    select
        -- Encounter Info
        e.encounter_id,
        e.encounter_type,
        e.admission_date,
        e.discharge_date,
        e.length_of_stay,
        e.los_category,

        -- Diagnosis
        e.primary_diagnosis_code,
        e.primary_diagnosis_desc,
        e.diagnosis_category,

        -- Discharge
        e.discharge_disposition,
        e.is_mortality,

        -- Provider
        e.attending_physician,
        e.department,

        -- Patient Demographics
        p.patient_id,
        p.full_name,
        p.age_years,
        p.gender,
        p.race,
        p.state,
        p.insurance_type,
        p.insurance_category

    from encounters e
    inner join patients p
        on e.patient_id = p.patient_id

)

select * from joined