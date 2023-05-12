{% macro is_null_value(string) %}
    isnull({{string}})
{% endmacro %}
