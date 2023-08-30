{% macro to_varchar(expr, format) %}

{% if format %}

case when typeof({{expr}}) = 'date'
then to_date({{expr}}, {{format}})::string
when typeof({{expr}}) = 'timestamp'
then to_timestamp({{expr}}, {{format}})::string
when typeof({{expr}}) = 'binary'
then to_binary({{expr}}, {{format}})::string
else to_char({{expr}}, {{format}})::string
end

{% else %}

cast({{expr}} as string)



{% endif %}	

{% endmacro %}
