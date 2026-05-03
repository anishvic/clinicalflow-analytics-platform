-- ============================================================
-- Model: stg_medications
-- Purpose: Clean and standardize raw medications data
-- FHIR Resource: MedicationRequest
-- ============================================================

with source as (

    select * from raw_medications

),

cleaned as (

    select
        -- Identity
        medication_id,
        encounter_id,

        -- Medication Details
        initcap(medication_name)                    as medication_name,
        dose,
        route,
        frequency,

        -- Dates
        start_date::date                            as start_date,
        end_date::date                              as end_date,

        -- Duration in days
        end_date::date - start_date::date           as duration_days,

        -- Route Category
        case
            when route = 'Oral'          then 'Non-Invasive'
            when route = 'IV'            then 'Invasive'
            when route = 'Subcutaneous'  then 'Invasive'
            else 'Other'
        end                                         as route_category,

        -- Status
        upper(status)                               as status,
        case
            when status = 'Active'       then true
            else false
        end                                         as is_active,

        -- Provider
        initcap(prescribing_physician)              as prescribing_physician

    from source
    where medication_id is not null
      and encounter_id is not null
      and start_date is not null

)

select * from cleaned