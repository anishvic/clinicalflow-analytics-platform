-- ============================================================
-- Model: stg_encounters
-- Purpose: Clean and standardize raw encounter data
-- FHIR Resource: Encounter
-- ============================================================

with source as (

    select * from raw_encounters

),

cleaned as (

    select
        -- Encounter Identity
        encounter_id,
        patient_id,

        -- Dates
        admission_date::timestamp                   as admission_date,
        discharge_date::timestamp                   as discharge_date,

        -- Length of Stay
        length_of_stay,
        case
            when length_of_stay between 0 and 3   then 'Short Stay'
            when length_of_stay between 4 and 7   then 'Medium Stay'
            when length_of_stay between 8 and 15  then 'Long Stay'
            else 'Extended Stay'
        end                                         as los_category,

        -- Encounter Type
        encounter_type,

        -- Diagnosis
        upper(primary_diagnosis_code)               as primary_diagnosis_code,
        initcap(primary_diagnosis_desc)             as primary_diagnosis_desc,
        case
            when primary_diagnosis_code like 'I%'  then 'Cardiovascular'
            when primary_diagnosis_code like 'E%'  then 'Endocrine'
            when primary_diagnosis_code like 'J%'  then 'Respiratory'
            when primary_diagnosis_code like 'N%'  then 'Renal'
            when primary_diagnosis_code like 'F%'  then 'Mental Health'
            when primary_diagnosis_code like 'M%'  then 'Musculoskeletal'
            when primary_diagnosis_code like 'Z%'  then 'Preventive'
            else 'Other'
        end                                         as diagnosis_category,

        -- Discharge
        discharge_disposition,
        case
            when discharge_disposition = 'Expired' then true
            else false
        end                                         as is_mortality,

        -- Provider
        initcap(attending_physician)                as attending_physician,
        initcap(department)                         as department,

        -- Metadata
        created_at::timestamp                       as created_at

    from source
    where encounter_id is not null
      and patient_id is not null
      and admission_date is not null

)

select * from cleaned