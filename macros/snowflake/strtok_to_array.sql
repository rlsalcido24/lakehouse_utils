{% macro strtok_to_array(arg, delim) %}
    split({{arg}}, concat("[", {{delim}}, "]"))
{% endmacro %}
