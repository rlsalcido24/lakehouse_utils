{% macro to_number(expr, format, precision, scale) %}


{% if scale %}




cast({{expr}} as decimal({{precision}}, {{scale}}))


{% elif precision %}

cast({{expr}} as decimal({{format}}, {{precision}}))


{% elif format %}

to_number({{expr}}, "{{format}}")


{% else %}

cast({{expr}} as decimal(38, 0))

{% endif %}	

{% endmacro %}
