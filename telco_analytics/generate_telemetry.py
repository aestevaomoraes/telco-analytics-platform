import duckdb

print("Iniciando a geração de dados de telemetria...")

# Conecta a uma instância em memória do DuckDB
con = duckdb.connect()

# Query SQL robusta que gera 10.000 registros aleatórios simulando a rede
query = """
    COPY (
        SELECT 
            -- Gera um ID único para cada evento (ex: EVT-1, EVT-2...)
            'EVT-' || CAST(range AS VARCHAR) AS event_id,
            
            -- Simula 500 clientes diferentes (IDs de 1 a 500)
            CAST(FLOOR(RANDOM() * 500) + 1 AS INT) AS customer_id,
            
            -- Simula 10 nós/roteadores diferentes na rede
            'NODE-' || CAST(FLOOR(RANDOM() * 10) + 1 AS VARCHAR) AS router_id,
            
            -- Gera datas aleatórias nos últimos 30 dias
            CURRENT_TIMESTAMP - INTERVAL (RANDOM() * 30) DAY AS event_timestamp,
            
            -- Simula latência em milissegundos (de 5ms a 150ms)
            CAST(FLOOR(RANDOM() * 145) + 5 AS INT) AS latency_ms,
            
            -- Simula perda de pacotes (de 0% a 5%)
            ROUND(RANDOM() * 5, 2) AS packet_loss_pct,
            
            -- Simula o status da conexão com base em probabilidades
            CASE 
                WHEN RANDOM() > 0.95 THEN 'Down'       -- 5% de chance de queda
                WHEN RANDOM() > 0.85 THEN 'Degraded'   -- 10% de chance de degradação
                ELSE 'Online'                          -- 85% de chance de estar normal
            END AS connection_status
            
        FROM range(10000) -- Gera 10.000 linhas
    ) TO 'raw_telemetry.parquet' (FORMAT PARQUET);
"""

# Executa a query
con.execute(query)

print("✅ Arquivo 'raw_telemetry.parquet' gerado com sucesso com 10.000 registros!")