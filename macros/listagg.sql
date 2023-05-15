{% macro listagg(arg, delim) %}
  CASE WHEN locate('distinct', lower({{arg}})) = 0
  THEN array_join(sort_array(collect_list({{arg}})), {{delim}})
  ELSE array_join(sort_array(collect_list(DISTINCT {{arg}})), {{delim}})
  END
{% endmacro %}