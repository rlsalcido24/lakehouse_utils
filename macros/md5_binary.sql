{% macro md5_binary(arg) %}
    unhex(md5({{arg}}))
{% endmacro %}
