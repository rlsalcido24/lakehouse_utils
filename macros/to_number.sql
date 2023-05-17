{% macro to_number(expr, format, precision, scale) %}


{% if scale %}

cast({{expr}} as decimal({{precision}}, {{scale}}))


{% elif precision %}

case when typeof({{format}}) = 'string'
then to_number({{expr}}, {{format}})
else cast({{expr}} as decimal({{format}}, {{precision}}))
end


{% elif format %}

case when typeof({{format}}) = 'string'
then to_number({{expr}}, {{format}})
else cast({{expr}} as decimal({{format}}, 0))
end

{% else %}

decimal({{expr}})

{% endif %}	

{% endmacro %}
