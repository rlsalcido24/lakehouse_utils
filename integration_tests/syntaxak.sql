
{{
    config(
        materialized = 'table'
    )
}}

select 
    cast(c_custkey as string) as stringkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone, 
    log10(c_acctbal) as actbalbaseten,
    log10(c_acctbal) as actbalbaseten,
    get_json_object('{"f2":{"f3":1},"f4":{"f5":99,"f6":"star"}}', '$.f4.f6'),
    power(2.71828, 100),
    CASE  WHEN lower( dow ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR(   2008-01-05 14:00:00 ::timestamp ) - 1) / 1000))  WHEN lower( dow ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR(   2008-01-05 14:00:00 ::timestamp ) - 1) / 100))  WHEN lower( dow ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR(   2008-01-05 14:00:00 ::timestamp ) - 1) / 10))   WHEN lower( dow ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR',  2008-01-05 14:00:00::timestamp) / 1)   WHEN lower( dow ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK',  2008-01-05 14:00:00::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( dow ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK',  2008-01-05 14:00:00::timestamp) - 1   WHEN lower( dow ::string) IN ('day', 'days', 'd') THEN date_part('DAY',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND',  2008-01-05 14:00:00::timestamp)   WHEN lower( dow ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND',  2008-01-05 14:00:00::timestamp)*1000   WHEN lower( dow ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND',  2008-01-05 14:00:00::timestamp)*1000000 ELSE NULL END,
    hll_cardinality(expr),
    array_size('[11,12,13,{"f1":21,"f2":[25,26]},14]'),
    c_mktsegment,
    c_comment,
    date_format(CASE   WHEN lower( 'second' ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 1000))   WHEN lower( 'second' ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 100))   WHEN lower( 'second' ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 10))   WHEN lower( 'second' ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR', ' current_timestamp()'::timestamp) / 1)   WHEN lower( 'second' ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK', ' current_timestamp()'::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( 'second' ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK', ' current_timestamp()'::timestamp) - 1   WHEN lower( 'second' ::string) IN ('day', 'days', 'd') THEN date_part('DAY', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR', ' current_timestamp()'::timestamp)   WHEN lower( 'second' ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND', ' current_timestamp()'::timestamp)   WHEN lower( 'second' ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND', ' current_timestamp()'::timestamp)*1000   WHEN lower( 'second' ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND', ' current_timestamp()'::timestamp)*1000000 ELSE NULL END, 'yyyy-MM-dd HH:mm:ss') as hoy,
    date_format(CASE   WHEN lower( 'second' ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 1000))   WHEN lower( 'second' ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 100))   WHEN lower( 'second' ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR( '  current_timestamp() '::timestamp ) - 1) / 10))   WHEN lower( 'second' ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR', ' current_timestamp()'::timestamp) / 1)   WHEN lower( 'second' ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK', ' current_timestamp()'::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( 'second' ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK', ' current_timestamp()'::timestamp) - 1   WHEN lower( 'second' ::string) IN ('day', 'days', 'd') THEN date_part('DAY', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR', ' current_timestamp()'::timestamp)   WHEN lower( 'second' ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE', ' current_timestamp()'::timestamp)  WHEN lower( 'second' ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND', ' current_timestamp()'::timestamp)   WHEN lower( 'second' ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND', ' current_timestamp()'::timestamp)*1000   WHEN lower( 'second' ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND', ' current_timestamp()'::timestamp)*1000000 ELSE NULL END, 'yyyy-MM-dd HH:mm:ss') AS get_date_caps_test,
    date_format(current_timestamp(), 'yyyy-MM-dd HH:mm:ss') AS sys_date_col_test,
    date_format(current_timestamp(), 'yyyy-MM-dd HH:mm:ss') AS sys_date_caps_col_test,
    coalesce(test, test_is_null) AS null_test_col_caps,
    coalesce(test, test_is_null) AS null_test_col_caps,
    coalesce(test, 'test_is_null') AS null_test_col,
    CASE  WHEN lower( year ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 1000))  WHEN lower( year ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 100))  WHEN lower( year ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 10))   WHEN lower( year ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR',  date(origination_date)::timestamp) / 1)   WHEN lower( year ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK',  date(origination_date)::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( year ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK',  date(origination_date)::timestamp) - 1   WHEN lower( year ::string) IN ('day', 'days', 'd') THEN date_part('DAY',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND',  date(origination_date)::timestamp)   WHEN lower( year ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND',  date(origination_date)::timestamp)*1000   WHEN lower( year ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND',  date(origination_date)::timestamp)*1000000 ELSE NULL END || '-' || 'Q' || floor(
            (CASE  WHEN lower( month ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 1000))  WHEN lower( month ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 100))  WHEN lower( month ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR(   date(origination_date) ::timestamp ) - 1) / 10))   WHEN lower( month ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR',  date(origination_date)::timestamp) / 1)   WHEN lower( month ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK',  date(origination_date)::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( month ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK',  date(origination_date)::timestamp) - 1   WHEN lower( month ::string) IN ('day', 'days', 'd') THEN date_part('DAY',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND',  date(origination_date)::timestamp)   WHEN lower( month ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND',  date(origination_date)::timestamp)*1000   WHEN lower( month ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND',  date(origination_date)::timestamp)*1000000 ELSE NULL END - 1) / 3) + 1 as origination_quarter,
    CASE  WHEN lower( SECONDS ::string) IN ('millennium', 'millennia', 'mil', 'mils') THEN (CEILING((YEAR(   '2019-10-01 00:00:01.000001'::timestamp ::timestamp ) - 1) / 1000))  WHEN lower( SECONDS ::string) IN ('century', 'centuries',	'c', 'cent', 'cents') THEN (CEILING((YEAR(   '2019-10-01 00:00:01.000001'::timestamp ::timestamp ) - 1) / 100))  WHEN lower( SECONDS ::string) IN ('decade', 'decades', 'dec', 'decs') THEN (CEILING((YEAR(   '2019-10-01 00:00:01.000001'::timestamp ::timestamp ) - 1) / 10))   WHEN lower( SECONDS ::string) IN ('year', 'years','y', 'yr', 'yrs') THEN FLOOR(date_part('YEAR',  '2019-10-01 00:00:01.000001'::timestamp::timestamp) / 1)   WHEN lower( SECONDS ::string) IN ('quarter', 'quarters', 'qtr', 'qtrs') THEN date_part('QUARTER',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('month', 'months', 'mon', 'mons') THEN date_part('MONTH',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('week', 'weeks', 'w') THEN date_part('WEEK',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)  Day of Week: in Redshift day of week is 0-6, starting with Sunday, Databricks is 1-7, starting with  WHEN lower( SECONDS ::string) IN ('day of week', 'dayofweek', 'dow', 'dw', 'weekday') THEN date_part('DAYOFWEEK',  '2019-10-01 00:00:01.000001'::timestamp::timestamp) - 1   WHEN lower( SECONDS ::string) IN ('day', 'days', 'd') THEN date_part('DAY',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('hour', 'hours',	'h', 'hr', 'hrs') THEN date_part('HOUR',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('minute', 'minutes', 'm', 'min', 'mins') THEN date_part('MINUTE',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('second', 'seconds',	's', 'sec', 'secs') THEN date_part('SECOND',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)   WHEN lower( SECONDS ::string) IN ('millisecond', 'milliseconds',	'ms', 'msec', 'msecs', 'msecond', 'mseconds', 'millisec', 'millisecs', 'millisecon') THEN date_part('SECOND',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)*1000   WHEN lower( SECONDS ::string) IN ('microsecond', 'microseconds',	'microsec', 'microsecs', 'microsecond', 'usecond', 'useconds', 'us', 'usec', 'usecs') THEN date_part('SECOND',  '2019-10-01 00:00:01.000001'::timestamp::timestamp)*1000000 ELSE NULL END
    first_value(
            case when colA = 2 then id2
            end ) ignore nulls
          over (
            partition by
                customer_id
            order by
                created_at
            rows between unbounded preceding and unbounded following
        ) as test_syntax_change
from
    redshift_sample_data.tpch_rs1.customer
ORDER BY  colC NULLS FIRST,colB  DESC NULLS FIRST
