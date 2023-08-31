{% macro hll_create_sketch(expr) %}
    hll_sketch_agg({{expr}})
{% endmacro %}
