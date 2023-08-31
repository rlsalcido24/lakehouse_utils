{% macro hll(expr) %}
    cardinality({{expr}})
{% endmacro %}
