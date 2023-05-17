{% macro to_varchar(expr, format) %}
    to_char({{expr}}, {{format}})
{% endmacro %}
