{% macro hll_cardinality(expr) %}
    hll_sketch_estimate({{expr}})
{% endmacro %}
