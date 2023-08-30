{%- macro exclude() -%}

  {%- set all_args = [] -%}
    {% for col in kwargs.items() -%}
      {%- do all_args.append(col) -%}
    {%- endfor -%}
  
  
  except({{ all_args|join(', ') }})
{%- endmacro -%}
