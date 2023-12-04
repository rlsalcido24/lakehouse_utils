{% macro date_trunc(unit, expr) %}

CASE
-- Millenia
WHEN lower({{ unit }}::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN CONCAT((1 + FLOOR((YEAR( '{{ expr }}'::timestamp ) - 1) / 1000) * 1000)::string, '-01-01 00:00:00')::timestamp
-- Century
WHEN lower({{ unit }}::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN CONCAT((1 + FLOOR((YEAR( '{{ expr }}'::timestamp ) - 1) / 100) * 100)::string, '-01-01 00:00:00')::timestamp
-- Decade
WHEN lower({{ unit }}::string) IN ('decade', 'decades', 'dec', 'decs') THEN CONCAT((1 + FLOOR((YEAR( '{{ expr }}'::timestamp ) - 1) / 10) * 10)::string, '-01-01 00:00:00')::timestamp
-- Years
WHEN lower({{ unit }}::string) IN ('year', 'years','y', 'yr', 'yrs') THEN date_trunc('year', '{{expr}}'::timestamp)::timestamp
-- Quarter
WHEN lower({{ unit }}::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_trunc('quarter', '{{expr}}'::timestamp)::timestamp
-- Month
WHEN lower({{ unit }}::string) IN ('month', 'months', 'mon', 'mons') THEN date_trunc('month', '{{expr}}'::timestamp)::timestamp
-- Week
WHEN lower({{ unit }}::string) IN ('week', 'weeks', 'w') THEN date_trunc('week', '{{expr}}'::timestamp)::timestamp
--Day
WHEN lower({{ unit }}::string) IN ('day', 'days', 'd') THEN date_trunc('day', '{{expr}}'::timestamp)::timestamp
-- Hour
WHEN lower({{ unit }}::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_trunc('hour', '{{expr}}'::timestamp)::timestamp
-- Minute
WHEN lower({{ unit }}::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_trunc('minute', '{{expr}}'::timestamp)::timestamp
-- Second
WHEN lower({{ unit }}::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_trunc('second', '{{expr}}'::timestamp)::timestamp
-- Millisecond
WHEN lower({{ unit }}::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_trunc('millisecond', '{{expr}}'::timestamp)::timestamp
-- Microsecond
WHEN lower({{ unit }}::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_trunc('microsecond', '{{expr}}'::timestamp)::timestamp
-- Else just try to use the raw unit - let it fail if it doenst convert so users know
ELSE NULL
END

{% endmacro %}

