{% macro array_slice(arg1, arg2, arg3) %}
    slice({{arg1}}, {{arg2}}, ({{arg3}} - {{arg2}}))
{% endmacro %}