{% macro div0(arg1, arg2) %}
   CASE WHEN {{arg2}} = 0 THEN 0 ELSE {{arg1}} / {{arg2}} END;
{% endmacro %}
