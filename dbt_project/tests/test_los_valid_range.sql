-- Test: Length of stay must be between 0 and 365 days
-- Any rows returned = TEST FAILS

select
    encounter_id,
    length_of_stay
from {{ ref('stg_encounters') }}
where length_of_stay < 0
   or length_of_stay > 365