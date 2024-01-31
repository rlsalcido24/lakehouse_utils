{% macro booland_agg(arg1) %}
    bool_and({{arg1}})
{% endmacro %}