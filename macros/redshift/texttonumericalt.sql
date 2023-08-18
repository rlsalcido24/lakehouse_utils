-- macros/texttonumericalt.sql

{% macro texttonumericalt(input_string, precision, scale) %}
  ROUND(CAST({{ input_string }} AS DECIMAL({{ precision }}, {{ scale }})), {{ scale }})
{% endmacro %}