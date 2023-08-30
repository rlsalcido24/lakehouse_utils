{% macro array_agg(arg, delim) %}
 CASE WHEN locate('distinct', lower({{arg}})) = 0
  THEN sort_array(collect_list({{arg}}), {{delim}})
  ELSE sort_array(collect_list(DISTINCT {{arg}}), {{delim}})
  END
{% endmacro %}
