{% macro base64_decode_string(arg) %}
    unbase({{arg}})
{% endmacro %}
