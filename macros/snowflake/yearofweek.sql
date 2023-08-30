{% macro yearofweek(arg) %}
    extract(year from {{arg}})
{% endmacro %}
