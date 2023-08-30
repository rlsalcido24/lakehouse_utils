{% macro week(stamp) %}
    EXTRACT(WEEK FROM {{stamp}})
{% endmacro %}
