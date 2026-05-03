-- ============================================================
-- Model: stg_patients
-- Purpose: Clean and standardize raw patient data
-- FHIR Resource: Patient
-- ============================================================

with source as (

    select * from raw_patients

),

cleaned as (

    select
        -- Patient Identity
        patient_id,
        initcap(first_name)                    as first_name,
        initcap(last_name)                     as last_name,
        first_name || ' ' || last_name         as full_name,

        -- Demographics
        date_of_birth::date                    as date_of_birth,
        date_part('year', age(date_of_birth::date)) as age_years,
        case
            when gender = 'M' then 'Male'
            when gender = 'F' then 'Female'
            else 'Unknown'
        end                                    as gender,
        race,

        -- Contact Info
        initcap(city)                          as city,
        upper(state)                           as state,
        zip_code,
        phone,

        -- Insurance
        insurance_type,
        case
            when insurance_type in ('Medicare', 'Medicaid') then 'Government'
            when insurance_type = 'Commercial'              then 'Private'
            when insurance_type = 'Self-Pay'                then 'Self-Pay'
            else 'Unknown'
        end                                    as insurance_category,

        -- Metadata
        created_at::timestamp                  as created_at

    from source
    where patient_id is not null
      and date_of_birth is not null

)

select * from cleaned