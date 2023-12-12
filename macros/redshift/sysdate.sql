{% macro sysdate() %}
   date_format(current_timestamp(), 'yyyy-MM-dd HH:mm:ss')
{% endmacro %}
