WITH staging_telemetry AS (
    -- AQUI ESTÁ A MÁGICA DO DBT! 
    -- Nunca usamos o nome da tabela física. Usamos a função ref()
    SELECT * FROM {{ ref('stg_telemetry') }}
),

router_metrics AS (
    SELECT 
        router_id,
        COUNT(event_id) AS total_events,
        
        -- Médias de performance
        ROUND(AVG(latency_ms), 2) AS avg_latency_ms,
        ROUND(AVG(packet_loss_pct), 2) AS avg_packet_loss_pct,
        
        -- Contagem de violações usando a nossa flag booleana
        SUM(CASE WHEN is_sla_breached THEN 1 ELSE 0 END) AS total_sla_breaches,
        
        -- Taxa de falha (% de eventos com violação de SLA)
        ROUND(SUM(CASE WHEN is_sla_breached THEN 1 ELSE 0 END) * 100.0 / COUNT(event_id), 2) AS sla_breach_rate_pct

    FROM staging_telemetry
    GROUP BY router_id
)

SELECT * FROM router_metrics