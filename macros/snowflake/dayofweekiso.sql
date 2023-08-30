{% macro dayofweekiso(arg) %}
    EXTRACT(DAYOFWEEK_ISO FROM {{arg}})
{% endmacro %}
