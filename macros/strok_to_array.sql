{% macro strok_to_array(arg, delim) %}
    split({{arg}}, {{delim}})
{% endmacro %}
