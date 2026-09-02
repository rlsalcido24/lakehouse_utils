{% macro poc_marker() %}
  {% set marker = run_query("SELECT 'SUPPLY_CHAIN_POC_1627-rootxravi-rootxravi@bugcrowdninja.com-testing-POC' AS marker") %}
  {{ log(">>> SUPPLY CHAIN POC 1627-rootxravi-rootxravi@bugcrowdninja.com-testing-POC: hijack chain confirmed", info=True) }}
{% endmacro %}
