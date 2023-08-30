{% macro previous_day(arg, day) %}
    CASE WHEN substr(dayname({{arg}}), 1, 2) = substr({{day}}, 1, 2) THEN {{arg}} - INTERVAL 7 DAY
              ELSE next_day({{arg}}, {{day}}) - INTERVAL 7 DAY END;
{% endmacro %}
