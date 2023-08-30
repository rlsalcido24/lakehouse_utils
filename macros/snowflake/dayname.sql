{% macro dayname(arg) %}
    CASE 
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 0 THEN 'Sun'
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 1 THEN 'Mon'
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 2 THEN 'Tue'
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 3 THEN 'Wed'
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 4 THEN 'Thu'
         WHEN datediff(CAST({{arg}} AS DATE), DATE'1799-12-29') % 7 = 5 THEN 'Fri'
         ELSE 'Sat' END
{% endmacro %}
