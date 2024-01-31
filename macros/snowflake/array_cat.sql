{% macro array_cat(arg1, arg2) %}
    concat({{arg1}}, {{arg2}})
{% endmacro %}
