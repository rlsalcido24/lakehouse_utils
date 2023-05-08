{% macro contains(position, column_name) %}

charindex({{position}}, {{column_name}}) > 0 

{% endmacro %}
