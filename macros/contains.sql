{% macro contains(column_name, position) %}

charindex({{position}}, {{column_name}}) > 0 

{% endmacro %}
