-- ============================================================
-- Model: mart_readmissions
-- Purpose: 30-day readmission analysis
-- CMS Benchmark: < 15% readmission rate
-- ============================================================

with encounters as (

    select * from {{ ref('int_encounter_details') }}

),

readmissions as (

    select
        e1.encounter_id,
        e1.patient_id,
        e1.full_name,
        e1.age_years,
        e1.gender,
        e1.insurance_category,
        e1.diagnosis_category,
        e1.primary_diagnosis_code,
        e1.primary_diagnosis_desc,
        e1.department,
        e1.discharge_date,
        e1.discharge_disposition,
        e1.length_of_stay,
        e1.los_category,

        -- Check if patient came back within 30 days
        e2.encounter_id                         as readmission_encounter_id,
        e2.admission_date                       as readmission_date,
        e2.primary_diagnosis_code               as readmission_diagnosis_code,

        case
            when e2.encounter_id is not null    then true
            else false
        end                                     as is_readmission,

        case
            when e2.encounter_id is not null
            then extract(
                epoch from (e2.admission_date - e1.discharge_date)
            ) / 86400
            else null
        end                                     as days_to_readmission

    from encounters e1
    left join encounters e2
        on  e1.patient_id    = e2.patient_id
        and e2.admission_date > e1.discharge_date
        and e2.admission_date <= e1.discharge_date
                                + interval '30 days'
        and e1.encounter_id != e2.encounter_id

)

select * from readmissions