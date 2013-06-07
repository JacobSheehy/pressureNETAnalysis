CALL_READINGS = 'readings'
CALL_CONDITIONS = 'conditions'

CALL_TYPES = (
    (CALL_READINGS, 'Readings'),
    (CALL_CONDITIONS, 'Conditions'),
)


CUSTOMER_INTERNAL = 'internal'
CUSTOMER_PUBLIC = 'public'
CUSTOMER_RESEARCHER = 'researcher'
CUSTOMER_FORECASTER = 'forecaster'

CUSTOMER_TYPES = (
    (CUSTOMER_INTERNAL, 'Internal'),
    (CUSTOMER_PUBLIC, 'Public'),
    (CUSTOMER_RESEARCHER, 'Researcher'),
    (CUSTOMER_FORECASTER, 'Forecaster'),
)

CUSTOMER_FORM_TYPES = (
    (CUSTOMER_RESEARCHER, 'Researcher', 'Currently, researchers receive our hourly, global data at no charge. You must be researchingat an academic institution to qualify.'),
    #(CUSTOMER_FORECASTER, 'Forecaster', 'For Forecasters'),
    (CUSTOMER_PUBLIC, 'Public', 'Everyone may access our smaller, public dataset, which contains only data our users have agreed to share publicly.'),
)
