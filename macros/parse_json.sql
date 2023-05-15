{% macro parse_json(string) %}
 from_json({{string}}, schema_of_json({{string}}))
{% endmacro %}
