{% macro array_to_string(arg, delim) %}
    array_join({{arg}}, {{delim}}, null)
{% endmacro %}
