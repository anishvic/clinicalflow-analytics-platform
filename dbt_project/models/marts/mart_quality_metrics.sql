-- ============================================================
-- Model: mart_quality_metrics
-- Purpose: HEDIS-aligned quality metrics by department
-- ============================================================

with encounter_details as (

    select * from {{ ref('int_encounter_details') }}

),

quality as (

    select
        department,
        diagnosis_category,
        insurance_category,
        date_part('year', admission_date)       as year,

        -- Volume
        count(encounter_id)                     as total_encounters,

        -- Length of Stay
        round(avg(length_of_stay)::numeric, 1)  as avg_los,
        max(length_of_stay)                     as max_los,
        min(length_of_stay)                     as min_los,

        -- Mortality
        sum(case when is_mortality
            then 1 else 0 end)                  as total_deaths,
        round(
            sum(case when is_mortality
                then 1 else 0 end) * 100.0
            / nullif(count(encounter_id), 0)
        , 2)                                    as mortality_rate_pct,

        -- Encounter Mix
        sum(case when encounter_type = 'Inpatient'
            then 1 else 0 end)                  as inpatient_count,
        sum(case when encounter_type = 'Outpatient'
            then 1 else 0 end)                  as outpatient_count,
        sum(case when encounter_type = 'Emergency'
            then 1 else 0 end)                  as emergency_count,

        -- LOS Categories
        sum(case when los_category = 'Short Stay'
            then 1 else 0 end)                  as short_stay_count,
        sum(case when los_category = 'Long Stay'
            then 1 else 0 end)                  as long_stay_count

    from encounter_details
    group by
        department,
        diagnosis_category,
        insurance_category,
        date_part('year', admission_date)

)

select * from quality