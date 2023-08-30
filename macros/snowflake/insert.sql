{% macro insert(base, pos, len, ins) %}
   overlay({{base}}, {{ins}}, {{pos}}, {{len}})
{% endmacro %}
