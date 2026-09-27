# Telco Analytics Platform: Modern Data Architecture & Engineering

[![dbt Core](https://img.shields.io/badge/dbt-Core_1.8+-orange.svg)](https://docs.getdbt.com/)
[![DuckDB](https://img.shields.io/badge/Engine-DuckDB-yellow.svg)](https://duckdb.org/)
[![Google BigQuery](https://img.shields.io/badge/Cloud_DW-BigQuery-blue.svg)](https://cloud.google.com/bigquery)
[![Databricks](https://img.shields.io/badge/Lakehouse-Databricks-red.svg)](https://databricks.com/)

---

## 1. Visão Executiva & Contexto de Negócio

No setor de Telecomunicações e Serviços Corporativos (TMT / B2B & B2C), a perda de clientes (*churn*) e a degradação de receita estão diretamente correlacionadas com incidentes operacionais de rede e violações contratuais de Service Level Agreement (SLA).

Esta plataforma analítica implementa uma arquitetura orientada ao ciclo de vida canónico de engenharia de dados, transformando telemetria bruta de rede (CDRs, instabilidades de enlace, falhas de pacotes) e faturamento recorrente (MRR, ARPU, aditivos contratuais) em camadas dimensionais de alto desempenho, prontas para auditoria financeira e inferência de inteligência artificial.

### Objetivos Primordiais
* **Eliminar silos operacionais:** Unificar o sinal de telemetria da infraestrutura física com os registros de contratos do CRM/ERP financeiro.
* **Governança & Rastreabilidade Canónica:** Garantir conformidade dimensional estrita (Kimball) com linhagem completa de dados (DAG) e idempotência.
* **Otimização FinOps:** Arquitetar pipelines focados em baixo consumo de computação (pruning via partições e *clustering*), eliminando varreduras redundantes.
* **Capacitação Estratégica:** Estabelecer a transição de desenvolvimento reativo para a prática de *Principal Analytics Engineering*.

---

## 2. Fundamentos Arquiteturais e Teóricos

A plataforma apoia-se em três pilares metodológicos internacionais:

1. **Modelagem Dimensional Estrita (Ralph Kimball & Margy Ross):**
   * Definição explícita de granularidade antes da escrita de qualquer transformação analítica.
   * Matriz de barramento analítico (*Bus Matrix*) com dimensões conformadas (`dim_customers`, `dim_network_nodes`, `dim_date`).
   * Manuseamento estrito de dimensões com variação temporal lenta (SCD Tipo 1 e Tipo 2) e tabelas de fatos transacionais e periódicas.
2. **Ciclo de Vida de Engenharia de Dados (Joe Reis & Matt Housley):**
   * Adoção de *Data Contracts* desde a camada de ingestão.
   * Separação estrita entre armazenamento (*Storage*) e processamento (*Compute*).
   * Idempotência garantida em cada modelo por meio de materializações declarativas (`view`, `table`, `incremental`).
3. **Padrões Canónicos dbt Labs:**
   * Arquitetura em camadas: `staging` (limpeza/tipagem atómica), `intermediate` (regras de negócio e cruzamentos complexos) e `marts` (exposição dimensional para consumo).
   * Testes automatizados obrigatórios de unicidade, não-nulidade e integridade relacional via schema (`.yml`).

---

## 3. Estrutura da Trilha e Roteiro de Entregas

```mermaid
graph TD
    A[Fontes Brutas & Telemetria Telco] --> B[Ciclo 1: Engenharia Analítica Local]
    B -->|DuckDB + dbt Core| C[Ciclo 2: Cloud DW & FinOps]
    C -->|BigQuery + Particionamento| D[Ciclo 3: Enterprise Lakehouse]
    D -->|Databricks + Unity Catalog| E[Ciclo 4: Camada Semântica & IA]

    subgraph Ciclo_1 [Ciclo 1: Fundação & Contratos]
        B1[Testes de Contrato] --- B2[Staging, Intermediate, Marts]
    end

    subgraph Ciclo_2 [Ciclo 2: Escala Corporativa]
        C1[Otimização de Slots] --- C2[FinOps & Pruning]
    end

    subgraph Ciclo_3 [Ciclo 3: Governança Lakehouse]
        D1[Delta Lake ACID] --- D2[Time Travel & Liquid Clustering]
    end

    subgraph Ciclo_4 [Ciclo 4: Consumo por IA]
        E1[MetricFlow Semantic Layer] --- E2[Modelos Preditivos In-Database]
    end
```

## 4. Estado Atual da Implementação (Ciclo 1: Fundação Local)

* [x] **Ingestão Sintética:** Gerador vetorial via DuckDB (`generate_telemetry.py`) produzindo 10.000 registros de telemetria em formato colunar Parquet (`raw_telemetry.parquet`).
* [x] **Exploração & Rastreabilidade:** Validação interativa via Jupyter Notebook (`exploracao_telemetria.ipynb`) documentando as etapas de dados brutos e materializações.
* [x] **Camada Staging:** Modelo `stg_telemetry` implementado com padronização de nomenclatura, casting e flag idempotente de violação de SLA (`is_sla_breached`).
* [x] **Data Marts:** Agregação executiva `agg_router_health` compilada via DAG usando `{{ ref() }}`, expondo taxa de violação por nó de rede.
* [ ] **Governança & Testes:** Implementação de testes de contrato e regras de schema (`schema.yml`) — *Em andamento*.

---

## 5. Como Reproduzir o Ambiente Local

Para executar o pipeline analítico localmente no ambiente DuckDB:

1. **Instale as dependências:**
    pip install dbt-duckdb

2. **Gere os dados brutos de telemetria:**
    python telco_analytics/generate_telemetry.py

3. **Compile e execute os modelos dbt:**
    cd telco_analytics
    dbt run --profiles-dir .

---

Observe que logo abaixo de `end` estão as três crases sozinhas na linha: elas fecham a caixa escura do diagrama[cite: 8]. Depois disso, basta alternar para **Preview** para verificar o layout limpo e clicar em **Commit changes...**.
