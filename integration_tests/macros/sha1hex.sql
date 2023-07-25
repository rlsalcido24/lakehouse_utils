{% macro sha1hex(arg, len) %}
    sha1({{arg}}, {{len}})
{% endmacro %}
