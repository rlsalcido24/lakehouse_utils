{% macro try_to_number(expr, format, precision, scale) %}


{% if scale %}




try_cast({{expr}} as decimal({{precision}}, {{scale}}))


{% elif precision %}

try_cast({{expr}} as decimal({{format}}, {{precision}}))


{% elif format %}

try_to_number({{expr}}, "{{format}}")


{% else %}

try_cast({{expr}} as decimal(38, 0))

{% endif %}	

{% endmacro %}
