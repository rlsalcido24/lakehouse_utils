{% macro endswith(arg1, arg2) %}
    substr({{arg1}}, -length({{arg2}}), length({{arg2}})) = {{arg2}};
{% endmacro %}
