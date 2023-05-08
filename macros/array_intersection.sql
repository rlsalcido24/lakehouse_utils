{% macro array_intersection(arg1, arg2) %}
    array_intersect({{arg1}}, {{arg2}})
{% endmacro %}
