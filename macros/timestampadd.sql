{% macro timestampadd(unit, measure, base) %}
CASE 
  WHEN lower({{unit}}) = 'year'   THEN {{base}} + make_interval({{measure}})
  WHEN lower({{unit}}) = 'month'  THEN {{base}}+ make_interval(0, {{measure}})
  WHEN lower({{unit}}) = 'day'    THEN {{base}} + make_interval(0, 0, {{measure}})
  WHEN lower({{unit}}) = 'hour'   THEN {{base}} + make_interval(0, 0, 0, {{measure}})
  WHEN lower({{unit}}) = 'minute' THEN {{base}} + make_interval(0, 0, 0, 0, {{measure}})
  WHEN lower({{unit}}) = 'second' THEN {{base}} + make_interval(0, 0, 0, 0, 0, {{measure}})
{% endmacro %}
