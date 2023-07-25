{% macro listagg(arg, delim) %}
   array_join(sort_array(collect_list({{arg}})), "{{delim}}")
  
{% endmacro %}