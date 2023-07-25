{% macro json_extract_path_text(expr, key) %}
    get_json_object({{expr}}, '$.{{key}}') 
{% endmacro %}
