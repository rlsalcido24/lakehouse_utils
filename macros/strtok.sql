{% macro strtok(arg, delim, part) %}
    element_at(split({{arg}}, {{delim}}), {{part}} )
{% endmacro %}
