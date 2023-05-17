{% macro date_from_parts(year, month, day) %}
    make_date({{year}}, {{month}}, {{day}})
{% endmacro %}
