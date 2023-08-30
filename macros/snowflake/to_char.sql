{% macro to_char(arg) %}
    cast({{arg}} as string)
{% endmacro %}
