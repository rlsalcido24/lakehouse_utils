{% macro date_part(unit, expr) %}
CASE
-- Millenia
WHEN lower({{ unit }}::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR( '{{ expr }}'::timestamp ) - 1) / 1000))
-- Century
WHEN lower({{ unit }}::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR( '{{ expr }}'::timestamp ) - 1) / 100))
-- Decade
WHEN lower({{ unit }}::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR( '{{ expr }}'::timestamp ) - 1) / 10))
-- Years
WHEN lower({{ unit }}::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR', '{{expr}}'::timestamp) / 1)
-- Quarter
WHEN lower({{ unit }}::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER', '{{expr}}'::timestamp)
-- Month
WHEN lower({{ unit }}::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH', '{{expr}}'::timestamp)
-- Week
WHEN lower({{ unit }}::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK', '{{expr}}'::timestamp)
-- Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with Sunday
WHEN lower({{ unit }}::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK', '{{expr}}'::timestamp) - 1
-- Day
WHEN lower({{ unit }}::string) IN ('day', 'days', 'd') THEN date_part('DAY', '{{expr}}'::timestamp)
-- Hour
WHEN lower({{ unit }}::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR', '{{expr}}'::timestamp)
-- Minute
WHEN lower({{ unit }}::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE', '{{expr}}'::timestamp)
-- Second
WHEN lower({{ unit }}::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND', '{{expr}}'::timestamp)
-- Millisecond
WHEN lower({{ unit }}::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND', '{{expr}}'::timestamp)*1000
-- Microsecond
WHEN lower({{ unit }}::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND', '{{expr}}'::timestamp)*1000000
-- Else just try to use the raw unit - let it fail if it doenst convert so users know
ELSE NULL
END

{% endmacro %}
