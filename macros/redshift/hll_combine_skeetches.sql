{% macro hll_combine_sketches(expr1, expr2) %}
    hll_union({{expr1}}, {{expr2}} )
{% endmacro %}
