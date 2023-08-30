{% macro startswith(arg1, arg2) %}
    position({{arg2}}, {{arg1}}) = 1
{% endmacro %}
