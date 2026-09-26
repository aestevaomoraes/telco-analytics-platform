WITH raw_data AS (
    -- O DuckDB permite ler o arquivo parquet diretamente como se fosse uma tabela
    SELECT * FROM 'raw_telemetry.parquet'
),

renamed_and_casted AS (
    SELECT
        -- Identificadores
        event_id,
        customer_id,
        router_id,
        
        -- Padronização de tempo (convertendo para um nome mais amigável)
        event_timestamp AS event_created_at,
        
        -- Métricas de Rede
        latency_ms,
        packet_loss_pct,
        connection_status,
        
        -- [TELCO LEAD VIEW] 
        -- Flag booleana preparada no Staging para facilitar o cálculo de violação de SLA.
        CASE 
            WHEN connection_status IN ('Down', 'Degraded') THEN true
            ELSE false
        END AS is_sla_breached

    FROM raw_data
)

SELECT * FROM renamed_and_casted