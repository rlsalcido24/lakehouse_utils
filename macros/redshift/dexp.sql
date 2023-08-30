-- macros/dexp.sql

{% macro dexp(x) %}
  POWER(2.71828, {{ x }})
{% endmacro %}