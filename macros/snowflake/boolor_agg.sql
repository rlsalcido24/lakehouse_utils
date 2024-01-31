{% macro boolor_agg(arg1) %}
    bool_or({{arg1}})
{% endmacro %}