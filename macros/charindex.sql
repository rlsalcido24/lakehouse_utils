{% macro charindex(arg1, arg2, start) %}
    position({{arg1}}, {{arg2}}, {{start}})
{% endmacro %}
