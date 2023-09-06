{% macro strtol(num, frombase) %}
    conv({{num}}, {{frombase}}, 10)
{% endmacro %}
