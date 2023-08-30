{% macro weekiso(arg) %}
    extract (week from {{arg}})
{% endmacro %}
