{% macro hex_decode_string(arg1) %}
    decode(unhex({{arg1}}), 'UTF-8')
{% endmacro %}
