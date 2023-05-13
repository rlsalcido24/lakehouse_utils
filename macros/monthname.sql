{% macro monthname(arg) %}
     CASE 
         WHEN EXTRACT(MONTH FROM {{arg}}) = 1 THEN 'Jan'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 2 THEN 'Feb'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 3 THEN 'Mar'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 4 THEN 'Apr'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 5 THEN 'May'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 6 THEN 'Jun'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 7 THEN 'Jul'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 8 THEN 'Aug'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 9 THEN 'Sep'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 10 THEN 'Oct'
         WHEN EXTRACT(MONTH FROM {{arg}}) = 11 THEN 'Nov'
         ELSE 'Dec' END
{% endmacro %}
