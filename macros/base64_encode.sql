{% macro base64_encode(arg) %}
    base64({{arg}})
{% endmacro %}
