-- ============================================================
-- Model: stg_vitals
-- Purpose: Clean and standardize raw vitals data
-- FHIR Resource: Observation
-- ============================================================

with source as (

    select * from raw_vitals

),

cleaned as (

    select
        -- Identity
        vital_id,
        encounter_id,

        -- Timestamp
        recorded_at::timestamp                          as recorded_at,

        -- Blood Pressure
        systolic_bp,
        diastolic_bp,
        case
            when systolic_bp < 120 and diastolic_bp < 80   then 'Normal'
            when systolic_bp between 120 and 129
                 and diastolic_bp < 80                     then 'Elevated'
            when systolic_bp between 130 and 139
                 or diastolic_bp between 80 and 89         then 'High Stage 1'
            when systolic_bp >= 140
                 or diastolic_bp >= 90                     then 'High Stage 2'
            else 'Unknown'
        end                                             as bp_category,

        -- Heart Rate
        heart_rate,
        case
            when heart_rate < 60   then 'Bradycardia'
            when heart_rate <= 100 then 'Normal'
            else 'Tachycardia'
        end                                             as heart_rate_category,

        -- Temperature
        temperature,
        case
            when temperature < 96.8  then 'Hypothermia'
            when temperature <= 99.5 then 'Normal'
            when temperature <= 103  then 'Fever'
            else 'High Fever'
        end                                             as temperature_category,

        -- Oxygen
        oxygen_saturation,
        case
            when oxygen_saturation >= 95 then 'Normal'
            when oxygen_saturation >= 90 then 'Low'
            else 'Critical'
        end                                             as spo2_category,

        -- Respiratory Rate
        respiratory_rate,

        -- BMI Calculation
        weight_kg,
        height_cm,
        round(
            (weight_kg / ((height_cm / 100.0) * (height_cm / 100.0)))::numeric
        , 1)                                            as bmi,
        case
            when weight_kg / ((height_cm/100.0) * (height_cm/100.0)) < 18.5
                                                        then 'Underweight'
            when weight_kg / ((height_cm/100.0) * (height_cm/100.0)) < 25
                                                        then 'Normal'
            when weight_kg / ((height_cm/100.0) * (height_cm/100.0)) < 30
                                                        then 'Overweight'
            else 'Obese'
        end                                             as bmi_category

    from source
    where vital_id is not null
      and encounter_id is not null
      and systolic_bp between 40 and 300
      and heart_rate between 20 and 250
      and oxygen_saturation between 50 and 100

)

select * from cleaned