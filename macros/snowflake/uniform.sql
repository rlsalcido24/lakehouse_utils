{% macro uniform(min, max, double) %}
    {{min}} + ({{max}} - {{min}}) * {{rand}}
{% endmacro %}
