{% macro nullifzero(arg) %}
    nullif({{arg}}, 0)
{% endmacro %}
