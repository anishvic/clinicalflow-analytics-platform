-- Test: Vital signs must be within clinically valid ranges
-- Any rows returned = TEST FAILS

select
    vital_id,
    systolic_bp,
    heart_rate,
    oxygen_saturation,
    temperature
from {{ ref('stg_vitals') }}
where systolic_bp < 40    or systolic_bp > 300
   or heart_rate < 20     or heart_rate > 250
   or oxygen_saturation < 50 or oxygen_saturation > 100
   or temperature < 80    or temperature > 115