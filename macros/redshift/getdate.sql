{% macro redshift_getdate() %}
    date_format(date_trunc('second', current_timestamp()), 'yyyy-MM-dd HH:mm:ss')
{% endmacro %}