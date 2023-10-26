{% macro hll_estimate(expr) %}
    hll_sketch_estimate({{expr}})
{% endmacro %}
