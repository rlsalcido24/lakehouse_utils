-- macros/texttointalt.sql

{% macro texttointalt(input_expression, format_phrase) %}

  SELECT 
    {{ input_expression }} as original_input,
    {{ format_phrase }} AS format_phrase,
    
    CASE 
        -- Handle format: '999S'
        WHEN {{ format_phrase }} = '999S' THEN
            CAST(REGEXP_REPLACE({{ input_expression }}, '[^0-9]', '') AS INT)
        
        -- Handle format: 'C9(I)'
        WHEN {{ format_phrase }} = 'C9(I)' THEN
            CAST(
                CASE 
                    WHEN REGEXP_REPLACE({{ input_expression }}, '[^0-9]', '') LIKE '%-%'
                    THEN '-' || REGEXP_REPLACE(REGEXP_REPLACE({{ input_expression }}, '[^0-9]', ''), '\\D', '') 
                    ELSE REGEXP_REPLACE({{ input_expression }}, '[^0-9]', '')
                END AS INT
            )
        
        -- Handle exponential format: '-123E-2'
        WHEN {{ format_phrase }} IS NULL AND REGEXP_MATCH({{ input_expression }}, '[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?') IS NOT NULL THEN
            CAST(
                CASE 
                    WHEN {{ input_expression }} LIKE '%-%'
                    THEN '-' || CAST(CAST({{ input_expression }} AS FLOAT) AS INT)
                    ELSE CAST(CAST({{ input_expression }} AS FLOAT) AS INT)
                END AS INT
            )
        
        -- Handle input expression ending with a hyphen
        WHEN {{ format_phrase }} IS NULL AND {{ input_expression }} LIKE '%-' THEN
            CAST('-' || REGEXP_REPLACE({{ input_expression }}, '[^0-9-]', '') AS INT)
        
        -- Handle positive integer
        WHEN {{ format_phrase }} IS NULL AND REGEXP_MATCH({{ input_expression }}, '^\d+$') IS NOT NULL THEN
            CAST({{ input_expression }} AS INT)
        
        ELSE NULL
    END AS texttointalt
{% endmacro %}