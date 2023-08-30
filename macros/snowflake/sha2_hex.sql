{% macro sha2_hex(arg, len) %}
 sha2({{arg}}, {{len}})
{% endmacro %}
