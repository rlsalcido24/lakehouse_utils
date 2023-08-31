{% macro hll_combine(expr) %}
    hll_union_agg({{expr}})
{% endmacro %}
