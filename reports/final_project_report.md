# Financial / Consumer Behavior Analytics — Final Master Project Report

## Executive Summary & Master Repository Report

---

## 1. Project Overview

The **Financial / Consumer Behavior Analytics** project is an end-to-end, production-grade analytics repository designed to analyze retail consumer financial behavior across income, expenses, savings, debt, credit score distributions, transaction velocity, financial product adoption, and portfolio financial health scoring.

Developed across 4 structured phases:
- **Part 1**: Synthetic Data Engineering, Pipeline Orchestration, Data Quality Validation, & SQLite Warehouse Setup.
- **Part 2**: Advanced SQL Analytics Suite, 7 Analytical SQLite Views, Business Segmentation, & NTILE(5) RFM Clustering.
- **Part 3**: Power BI Star Schema Data Model, 50+ DAX Measure Library, Corporate Theme, & 6-Page Visual Specifications.
- **Part 4**: Comprehensive Final QA, Executive Business Insights, Strategic Recommendations, Master KPI Catalog, Interview Materials, & Local Verification.

---

## 2. Business Problem

Retail banking institutions require integrated visibility into customer financial health to:
- Detect credit default risks before delinquency occurs.
- Segment customers by net savings capacity, liquidity, and debt-to-income (DTI) ratios.
- Personalize financial product cross-selling (e.g., mortgages, premium credit cards, investment accounts).
- Quantify portfolio-wide balance sheet resilience using a composite Financial Health Index (0-100).

---

## 3. Dataset Description

The project processes a synthetic relational dataset containing **15,000 unique customers** and over **197,000 entity records** across 8 relational tables:

| Entity Table | Primary Key | Foreign Key | Record Count | Description |
|---|---|---|---|---|
| `CUSTOMERS` | `customer_id` | - | 15,000 | Demographics, education, occupation, tenure |
| `INCOME` | `income_id` | `customer_id` | 15,000 | Monthly & annual earnings, income source, stability |
| `EXPENSES` | `expense_id` | `customer_id` | 15,000 | Itemized monthly expense categories & total outlay |
| `SAVINGS` | `savings_id` | `customer_id` | 15,000 | Monthly savings, balances, rate, emergency status |
| `DEBT` | `debt_id` | `customer_id` | 15,000 | Credit card, personal, auto, education, mortgage debt |
| `CREDIT` | `credit_id` | `customer_id` | 15,000 | FICO credit score, missed payments, utilization, risk tier |
| `TRANSACTIONS` | `transaction_id` | `customer_id` | 75,744 | Transaction logs, amounts, dates, categories, merchants |
| `FINANCIAL_PRODUCTS` | `product_id` | `customer_id` | 31,274 | Adopted banking products and operational status |

---

## 4. Data Engineering Pipeline

The pipeline is orchestrated via `run_pipeline.py` supporting 7 sequential stages:
1. `generate`: Reproducible synthetic data generation (Seed `42`).
2. `clean`: Standardizes encodings, imputes missing values, removes 50 noise records, and recalculates derived financial metrics.
3. `validate`: Executes 25 automated data quality assertions.
4. `db`: Deploys DDL schema in SQLite with performance indexes.
5. `query`: Executes SQL validation queries.
6. `analytics`: Deploys 7 analytical SQL views and runs 12 structured query scripts.
7. `export`: Exports analytical CSVs and Power BI Star Schema tables.

---

## 5. Data Quality Assurance

- **Assertion Engine**: Custom validator (`src/validation/validator.py`) asserts 0% missing primary keys, 0% orphaned records, valid range bounds, and non-negative financial values.
- **Data Quality Result**: 25 out of 25 quality checks passed (100%).

---

## 6. SQLite Relational Database Warehouse

- **Database Path**: `database/financial_analytics.db`
- **Schema & Indexes**: `sql/schema/01_create_tables.sql` & `sql/schema/02_create_indexes.sql`
- **Integrity**: Enforces strict `PRAGMA foreign_keys = ON;` and index coverage across all foreign key columns.

---

## 7. SQL Analytics Suite

- **7 Analytical SQL Views** deployed under `sql/views/`:
  - `vw_customer_financial_profile` (Master profile, 15,000 rows)
  - `vw_customer_behavior_summary`
  - `vw_customer_segments`
  - `vw_rfm_segments`
  - `vw_monthly_transaction_summary`
  - `vw_product_adoption_summary`
  - `vw_financial_risk_summary`
- **12 Analytical Query Modules** deployed under `sql/analysis/`.

---

## 8. Customer Business Segmentation

Classifies customers into 7 primary business segments:
- **Emerging Customers**: 6,173 customers (41.15%)
- **Debt-Burdened**: 3,042 customers (20.28%)
- **Disciplined Savers**: 1,747 customers (11.65%)
- **High-Income High-Spenders**: 1,724 customers (11.49%)
- **Financially Strong**: 1,219 customers (8.13%)
- **Credit-Risk Customers**: 594 customers (3.96%)
- **Low-Engagement Customers**: 501 customers (3.34%)

---

## 9. RFM Cohort Segmentation

Utilizes `NTILE(5)` window functions on Recency (relative to reference date `2025-12-31`), Frequency, and Monetary spend:
- **Needs Attention**: 3,154 customers (21.03%)
- **Loyal Customers**: 2,999 customers (19.99%)
- **Potential Loyalists**: 2,463 customers (16.42%)
- **Champions**: 2,138 customers (14.25%)
- **Lost**: 1,910 customers (12.73%)
- **New Customers**: 1,661 customers (11.07%)
- **Promising**: 345 customers (2.30%)
- **At Risk**: 330 customers (2.20%)

---

## 10. Credit Risk Analytics

Evaluates 9 credit risk combinations across credit bureau risk categories and debt risk tiers, identifying **3,158 high-risk/critical-debt customers** requiring proactive monitoring.

---

## 11. Power BI Star Schema Data Model

Architected as a pure Star Schema in `data/exports/powerbi/*.csv`:
- **Dimension Tables**: `dim_customer` (15k), `dim_date` (2,922), `dim_product` (7), `dim_segment` (7), `dim_risk` (9).
- **Fact Tables**: `fact_transactions` (75,744), `fact_customer_financial` (15,000), `fact_product_holdings` (31,274).
- **0 Join Multiplication**: `dim_customer` links 1:1 with `fact_customer_financial` and 1:N with `fact_transactions`.

---

## 12. DAX Measure Library

- **50+ Production DAX Measures** documented in [`powerbi/dax_measures.md`](powerbi/dax_measures.md).
- Features Core Financial KPIs, Portfolio Health Index, YoY Spend Growth, RFM counts, and Product Penetration metrics.

---

## 13. Dashboard Design Specifications

- **6 Dashboard Pages** documented in [`docs/powerbi_dashboard_specification.md`](docs/powerbi_dashboard_specification.md):
  1. Executive Overview & Financial Health Summary
  2. Consumer Spending & Behavioral Patterns
  3. Financial Health & Balance Sheet Resilience
  4. Risk, Credit & Default Analysis
  5. Customer Segmentation & RFM Clustering
  6. Product Holdings & Cross-Sell Opportunities
- **Corporate Visual Theme**: Configured in [`powerbi/theme.json`](powerbi/theme.json).

---

## 14. Key Business Insights

1. **Total Portfolio Annual Income**: **$1.089 Billion** (Avg $72,629.52).
2. **Total Portfolio Liabilities**: **$1.221 Billion** (Avg $81,430.60 per customer).
3. **Total Portfolio Liquid Deposits**: **$781.39 Million** (Avg $52,092.85 per customer).
4. **Single-Product Cross-Sell Whitespace**: **4,564 customers (30.43%)** hold only 1 product.
5. **Portfolio Financial Health Index**: Average score **76.09 / 100** (72.67% Healthy, 17.37% Vulnerable, 9.95% High Risk).

---

## 15. Strategic Recommendations

Documented in [`reports/strategic_recommendations.md`](reports/strategic_recommendations.md):
1. **Wealth Expansion** (HIGH Priority): Automated wealth management onboarding for 1,219 Financially Strong customers.
2. **Cross-Sell Activation** (HIGH Priority): In-app credit card & personal loan pre-approvals for 4,564 single-product customers.
3. **Risk Mitigation** (HIGH Priority): Pre-delinquency refinancing for 3,158 critical debt customers.

---

## 16. Testing & Quality Verification

- **Pytest Suite**: Executed `pytest tests/ -v`.
- **Result**: **21 PASSED / 0 FAILED** in 39.10 seconds.
- **Reconciliation**: 100% exact numerical match across all data layers.

---

## 17. Reproducibility

- Dependencies pinned in `requirements.txt`.
- Single command pipeline execution: `python run_pipeline.py --all`.
- Seed `42` guarantees 100% data reproducibility from a clean Python environment.

---

## 18. Security Review

- **Secrets & Credentials**: 0 API keys or passwords detected.
- **Privacy**: 0 personal paths in public-facing markdown documentation.
- **Git Exclusion**: `.gitignore` excludes `.env`, `credentials`, `secrets`, `.venv`, and `__pycache__`.

---

## 19. Limitations

- Dataset is synthetically generated with statistical correlations; findings cannot establish real-world causal mechanisms.
- Financial Health Score is a portfolio storytelling index, not a credit bureau score.

---

## 20. Future Enhancements

- Integrate machine learning models (XGBoost / Scikit-Learn) for predictive churn forecasting and default probability scoring.
- Implement dbt (data build tool) transformation models and automated documentation lineage.

---

## 21. GitHub Publication Status

> [!IMPORTANT]
> **NOT PUBLISHED — READY FOR MANUAL REVIEW**
>
> GitHub publication intentionally not performed in Part 4. The repository is completely developed, tested, documented, and locally verified, ready for final review and separate GitHub publication.
