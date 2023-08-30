{% macro timediff(unit, arg1,arg2) %}
  CASE 
  WHEN lower({{unit}}) = 'year'   THEN EXTRACT(YEAR FROM {{arg2}}) - EXTRACT(YEAR FROM {{arg1}})
  WHEN lower({{unit}}) = 'month'  THEN (EXTRACT(YEAR FROM {{arg2}}) * 12 + EXTRACT(MONTH FROM {{arg2}}))
                          - (EXTRACT(YEAR FROM {{arg1}}) * 12 + EXTRACT(MONTH FROM {{arg1}}))
  WHEN lower({{unit}}) = 'day'    THEN datediff(CAST({{arg2}} AS DATE), CAST({{arg1}} AS DATE))
  WHEN lower({{unit}}) = 'hour'   THEN EXTRACT(HOUR FROM {{arg2}}) - EXTRACT(HOUR FROM {{arg1}})
  WHEN lower({{unit}}) = 'minute' THEN (EXTRACT(HOUR FROM {{arg2}}) * 60 + EXTRACT(MINUTE FROM {{arg2}}))
                          - (EXTRACT(HOURs FROM {{arg1}}) * 60 + EXTRACT(MINUTE FROM {{arg1}}))
  WHEN lower({{unit}}) = 'second' THEN (EXTRACT(HOUR FROM {{arg2}}) * 3600 + EXTRACT(MINUTE FROM {{arg2}}) * 60 + EXTRACT(SECOND FROM {{arg2}}))
                          - (EXTRACT(HOUR FROM {{arg2}}) * 3600 + EXTRACT(MINUTE FROM {{arg2}}) * 60 + EXTRACT(SECOND FROM {{arg2}}))
  END
{% endmacro %}
