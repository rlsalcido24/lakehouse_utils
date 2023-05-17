{% macro sysdate() %}
   to_utc_timestamp(current_timestamp(), current_timezone());
{% endmacro %}
