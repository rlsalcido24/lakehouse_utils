{% macro base64_decode_binary(arg) %}
    unbase64({{arg}})
{% endmacro %}
