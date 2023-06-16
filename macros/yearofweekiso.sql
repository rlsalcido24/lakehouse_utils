{% macro yearofweekiso(arg) %}
    extract(year from {{arg}})
{% endmacro %}
