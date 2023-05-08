{% macro to_boolean(arg) %}
 CASE 
WHEN lower({{arg}}) = 'false' THEN FALSE
WHEN lower({{arg}}) = 'f' THEN FALSE
WHEN lower({{arg}}) =  'no' THEN FALSE
WHEN lower({{arg}}) = 'n' THEN FALSE
WHEN lower({{arg}}) = 'off' THEN FALSE
WHEN lower({{arg}}) = '0' THEN FALSE
WHEN lower({{arg}}) = 'null' THEN NULL
ELSE 'true'
END;
{% endmacro %}
