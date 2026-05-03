-- Test: ICD-10 codes must start with a valid letter
-- Valid chapters: I, E, J, N, F, M, Z
-- Any rows returned = TEST FAILS

select
    encounter_id,
    primary_diagnosis_code
from {{ ref('stg_encounters') }}
where primary_diagnosis_code !~ '^[IEJNFMZ][0-9]'