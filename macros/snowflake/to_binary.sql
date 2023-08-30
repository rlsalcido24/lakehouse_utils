{% macro to_binary(arg) %}
    unhex({{arg}})
{% endmacro %}