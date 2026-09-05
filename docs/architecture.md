# System Architecture & Data Pipeline Flow

## Financial / Consumer Behavior Analytics

This document presents the technical architecture and end-to-end data flow for the **Financial / Consumer Behavior Analytics** portfolio project.

---

## 1. End-to-End Data Pipeline Architecture

```
Synthetic Data Generation Engine (Python / NumPy / Faker)
                     │
                     ▼
Raw CSV Datasets (data/raw/*.csv - 15,000 customers, 8 entities)
                     │
                     ▼
Data Cleaning & Transformation Engine (src/data_cleaning/cleaner.py)
                     │
                     ▼
Processed Clean Datasets (data/processed/*.csv)
                     │
                     ▼
Automated Quality Assertion & Pytest Suite (src/validation/validator.py & tests/)
                     │
                     ▼
SQLite Database Relational Warehouse (database/financial_analytics.db)
                     │
                     ▼
Analytical SQL Views Layer (sql/views/*.sql - 7 views)
                     │
                     ▼
SQL Analytical Query Modules (sql/analysis/*.sql - 12 modules)
                     │
                     ▼
Power BI Star-Schema Dataset Exporter (src/database/export_powerbi_tables.py)
                     │
                     ▼
Power BI CSV Data Model Exports (data/exports/powerbi/*.csv - 5 Dims, 3 Facts)
                     │
                     ▼
Power BI DAX & Semantic Data Model (powerbi/dax_measures.md & theme.json)
                     │
                     ▼
Dashboard Visual Specifications (docs/powerbi_dashboard_specification.md - 6 Pages)
                     │
                     ▼
Business Insights & Strategic Recommendations (reports/executive_business_insights.md)
```

---

## 2. Stage-by-Stage Component Design

### Stage 1: Synthetic Data Generation Engine (`src/data_generation/generator.py`)
- **Technology**: Python 3.10+, NumPy, Pandas, Faker.
- **Function**: Generates reproducible random seed `42` synthetic datasets.
- **Correlations**: Enforces realistic statistical correlations (e.g., log-normal income distribution, credit score inverse correlation with debt, emergency reserve months).
- **Noise Injection**: Injects 50 controlled noise records into raw transactions to test cleaning resilience.

### Stage 2: Data Cleaning & Standardisation (`src/data_cleaning/cleaner.py`)
- **Function**: Standardizes string encodings, imputes missing values, removes noise records, recalculates derived financial formulas (e.g., Net Savings Capacity, Expense Ratio), and formats date keys.

### Stage 3: Data Quality & Referential Integrity Validation (`src/validation/validator.py`)
- **Function**: Executes 25 automated quality checks verifying 0% duplicate primary keys, 0% orphaned foreign keys, valid numeric range bounds, and non-negative balances.

### Stage 4: SQLite Database Ingestion (`src/database/db_loader.py`)
- **Technology**: SQLite3 engine with DDL schemas (`sql/schema/01_create_tables.sql`) and indexes (`sql/schema/02_create_indexes.sql`).
- **Function**: Deploys relational tables with strict `PRAGMA foreign_keys = ON;` and performance indexes.

### Stage 5 & 6: Analytical SQL Views & Query Modules (`sql/views/` & `sql/analysis/`)
- **Views**: Deploys 7 analytical SQL views including `vw_customer_financial_profile` (master profile), `vw_rfm_segments`, and `vw_financial_risk_summary`.
- **Query Suite**: Runs 12 structured SQL analysis scripts utilizing CTEs, Window Functions (`NTILE(5)`), and multi-table aggregations.

### Stage 7: Power BI Star-Schema Exporter (`src/database/export_powerbi_tables.py`)
- **Function**: Exports 5 Dimension tables (`dim_customer`, `dim_date`, `dim_product`, `dim_segment`, `dim_risk`) and 3 Fact tables (`fact_transactions`, `fact_customer_financial`, `fact_product_holdings`).
- **0 Join Multiplication**: Ensures `dim_customer` and `fact_customer_financial` link 1-to-1, eliminating fan-out.

---

## 3. Data Storage & File Layout

```
financial-consumer-behavior-analytics/
├── config/
│   └── config.yaml               # Pipeline settings
├── data/
│   ├── raw/                      # Raw dataset CSVs
│   ├── processed/                # Cleaned dataset CSVs
│   └── exports/                  # Power BI star schema CSVs
├── database/
│   └── financial_analytics.db    # SQLite relational database
├── docs/                         # Documentation index
├── powerbi/                      # DAX & visual themes
├── reports/                      # Validation & business reports
├── sql/                          # DDL schemas, views, analytical queries
├── src/                          # Core Python engine codebase
└── tests/                        # Automated pytest suite
```
