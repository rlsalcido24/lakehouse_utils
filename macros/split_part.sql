{% macro split_part(arg, delim, part) %}
    element_at(split({{arg}}, {{delim}}), {{part}})
{% endmacro %}
