{% macro array_compact(arg) %}
  filter({{arg}} , x -> x IS NOT NULL)
{% endmacro %}
