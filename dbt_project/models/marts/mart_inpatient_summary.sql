-- ============================================================
-- Model: mart_inpatient_summary
-- Purpose: Inpatient summary for dashboard reporting
-- ============================================================

with encounter_details as (

    select * from {{ ref('int_encounter_details') }}

),

summary as (

    select
        -- Time dimensions
        date_trunc('month', admission_date)     as admission_month,
        date_part('year', admission_date)       as admission_year,

        -- Encounter dimensions
        encounter_type,
        department,
        diagnosis_category,
        los_category,
        insurance_category,
        gender,
        race,

        -- Metrics
        count(encounter_id)                     as total_encounters,
        avg(length_of_stay)::numeric            as avg_los,
        sum(case when is_mortality
            then 1 else 0 end)                  as total_deaths,
        round(
            sum(case when is_mortality
                then 1 else 0 end) * 100.0
            / count(encounter_id)
        , 2)                                    as mortality_rate_pct

    from encounter_details
    group by
        date_trunc('month', admission_date),
        date_part('year', admission_date),
        encounter_type,
        department,
        diagnosis_category,
        los_category,
        insurance_category,
        gender,
        race

)

select * from summary