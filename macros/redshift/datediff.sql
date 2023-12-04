{% macro datediff(unit, start, end) %}
CASE
-- Millenia
WHEN lower({{ unit }}::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN FLOOR(timestampdiff(YEAR, '{{start}}'::timestamp, '{{end}}'::timestamp) / 1000)
-- Century
WHEN lower({{ unit }}::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN FLOOR(timestampdiff(YEAR, '{{start}}'::timestamp, '{{end}}'::timestamp) / 100)
-- Decade
WHEN lower({{ unit }}::string) IN ('decade', 'decades', 'dec', 'decs') THEN FLOOR(timestampdiff(YEAR, '{{start}}'::timestamp, '{{end}}'::timestamp) / 10)
-- Years
WHEN lower({{ unit }}::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(timestampdiff(YEAR, '{{start}}'::timestamp, '{{end}}'::timestamp) / 1)
-- Quarter
WHEN lower({{ unit }}::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN timestampdiff(QUARTER, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Month
WHEN lower({{ unit }}::string) IN ('month', 'months', 'mon', 'mons') THEN timestampdiff(MONTH, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Week
WHEN lower({{ unit }}::string) IN ('week', 'weeks', 'w') THEN timestampdiff(WEEK, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Day
WHEN lower({{ unit }}::string) IN ('day', 'days', 'd') THEN timestampdiff(DAY, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Hour
WHEN lower({{ unit }}::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN timestampdiff(HOUR, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Minute
WHEN lower({{ unit }}::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN timestampdiff(MINUTE, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Second
WHEN lower({{ unit }}::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN timestampdiff(SECOND, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Millisecond
WHEN lower({{ unit }}::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN timestampdiff(MILLISECOND, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Microsecond
WHEN lower({{ unit }}::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN timestampdiff(MICROSECOND, '{{start}}'::timestamp, '{{end}}'::timestamp)
-- Else just try to use the raw unit - let it fail if it doenst convert so users know
ELSE NULL
END
{% endmacro %}
