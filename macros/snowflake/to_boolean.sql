{% macro to_boolean(arg) %}
 CASE 
WHEN lower({{arg}}) = 'false' THEN FALSE
WHEN lower({{arg}}) = 'f' THEN FALSE
WHEN lower({{arg}}) =  'no' THEN FALSE
WHEN lower({{arg}}) = 'n' THEN FALSE
WHEN lower({{arg}}) = 'off' THEN FALSE
WHEN lower({{arg}}) = '0' THEN FALSE
WHEN lower({{arg}}) = 'true' THEN TRUE
WHEN lower({{arg}}) = 't' THEN TRUE
WHEN lower({{arg}}) =  'yes' THEN TRUE
WHEN lower({{arg}}) = 'y' THEN TRUE
WHEN lower({{arg}}) = 'on' THEN TRUE
WHEN lower({{arg}}) = '1' THEN TRUE

ELSE NULL
END
{% endmacro %}
