# Financial / Consumer Behavior Analytics

> **End-to-End Financial Data Engineering, SQL Analytics, & BI Portfolio Project (Part 1, Part 2, & Part 3 Completed)**

---

## 1. Project Overview

The **Financial / Consumer Behavior Analytics** project is a production-grade analytics repository designed to analyze retail consumer financial behavior across income, expenses, savings, debt, credit score distributions, transaction velocity, financial product adoption, and portfolio financial health scoring.

This project covers the full analytics engineering life cycle:
- Correlated synthetic data generation
- Automated data cleaning, transformation, and recalculation
- Data quality assertion and pytest suite
- Relational schema modeling & SQLite database ingestion
- Advanced SQL Analytical Views & Window Functions (Part 2)
- RFM Customer Segmentation & Business Opportunity Targeting (Part 2)
- Power BI Star-Schema Data Model & DAX Library (Part 3)
- 6-Page Power BI Report Specifications & Corporate Theme (Part 3)
- Technical & Domain Interview Guide (Part 3)

---

## 2. Business Problem

Financial institutions, retail banks, and fintech organizations require deep visibility into customer financial health to:
- Identify credit default risks before delinquency occurs.
- Segment customers by liquidity, net savings capacity, and debt-to-income (DTI) ratios.
- Personalize financial product cross-selling (e.g., mortgages, premium credit cards, investment accounts).
- Monitor transaction velocity across spending categories and merchant types.
- Quantify portfolio-wide balance sheet resilience using a composite Financial Health Index (0-100).

---

## 3. Key Objectives

1. **Build a Scalable Data Pipeline**: Ingest, clean, validate, and store >150,000 entity records with 100% referential integrity.
2. **Relational Data Engineering**: Normalize customer data across 8 relational entities enforcing strict primary and foreign keys.
3. **Data Quality Automation**: Guarantee 0% missing primary keys, 0% orphaned records, and 100% range bound compliance via `pytest`.
4. **Advanced SQL Analytics**: Provide 12 structured SQL analytical query modules and 7 reusable analytical SQLite views.
5. **RFM & Behavioral Segmentation**: Classify customers into 7 primary business segments and 8 RFM (Recency, Frequency, Monetary) quintile cohorts.
6. **Power BI Star Schema & DAX**: Architect a 0-join-multiplication Star Schema data model with 50+ production DAX measures (KPIs, Time Intelligence, Financial Health Index, Credit Risk, Product Cross-Sell).
7. **Production Report Package**: Provide complete visual specifications for 6 dashboard pages, custom corporate JSON theme, automated reconciliation testing, and an interview preparation guide.

---

## 4. Key Analytical Questions Answered

- How does income stability impact savings rates across different city tiers?
- What is the correlation between debt-to-income (DTI) ratio and credit score degradation?
- Which demographic segments represent the highest adoption of investment accounts and mortgages?
- What are the top spending categories by transaction volume and dollar amount?
- Which customers represent prime targets for financial product cross-selling, wealth management, or credit growth?
- What proportion of customers maintain an emergency fund covering at least 3 to 6 months of expenses?
- How is portfolio financial health distributed across customer segments and age tiers?

---

## 5. Dataset Description

The project utilizes a substantial relational dataset containing **15,000 unique customers** and over **197,000 entity records** across 8 relational tables:

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

## 6. Power BI Star Schema Data Model (Part 3)

The Power BI model follows a pure **Star Schema** architecture to avoid fan-out, double-counting, and DAX calculation errors:

```
                  ┌─────────────────┐
                  │    DIM_DATE     │
                  └────────┬────────┘
                           │ 1:N
                           ▼
┌─────────────────┐   ┌─────────────────────┐   ┌──────────────────────┐
│  DIM_CUSTOMER   │───┤  FACT_TRANSACTIONS  ├───│     DIM_PRODUCT      │
└────────┬────────┘1:N└─────────────────────┘N:1└──────────────────────┘
         │
         ├─── 1:1 ───► FACT_CUSTOMER_FINANCIAL ◄─── 1:N ─── DIM_SEGMENT
         │                      ▲
         │                      │ 1:N
         │                 DIM_RISK
         │
         └─── 1:N ───► FACT_PRODUCT_HOLDINGS ◄───── 1:N ─── DIM_PRODUCT
```

### Table Grains
* **`DIM_CUSTOMER`**: 1 row per customer (15,000 rows).
* **`DIM_DATE`**: 1 row per calendar date (2,922 rows, 2018–2025).
* **`DIM_PRODUCT`**: 1 row per product type (7 rows).
* **`DIM_SEGMENT`**: 1 row per business segment (7 rows).
* **`DIM_RISK`**: 1 row per risk combination (9 rows).
* **`FACT_TRANSACTIONS`**: 1 row per transaction (75,744 rows).
* **`FACT_CUSTOMER_FINANCIAL`**: 1 row per customer snapshot (15,000 rows).
* **`FACT_PRODUCT_HOLDINGS`**: 1 row per customer product holding (31,274 rows).

---

## 7. Technology Stack

- **Data Generation & Engineering**: Python 3.10+, Pandas, NumPy, PyYAML
- **Database Engine**: SQLite3 (Foreign Key Constraints, DDL Indexes, Analytical Views)
- **Data Validation & Testing**: Pytest (21 automated unit/reconciliation tests)
- **Query Language**: ANSI SQL / SQLite Dialect (Window Functions, CTEs, NTILE)
- **BI & Data Modeling**: Power BI Desktop Star Schema, DAX (50+ measures), Custom Theme JSON

---

## 8. Dashboard Layout Specifications (6 Pages)

1. **Executive Overview & Financial Health Summary**: Macro-level portfolio KPIs, net worth, deposit growth, cash flow trends.
2. **Consumer Spending & Behavioral Patterns**: Spend by category, merchant channel adoption (Online/POS/ATM), spending heatmaps.
3. **Financial Health & Balance Sheet Resilience**: Financial Health Score distribution, emergency reserve coverage months, savings capacity.
4. **Risk, Credit & Default Analysis**: Delinquency rates, DTI risk matrix, credit score migration, exposure-at-risk.
5. **Customer Segmentation & RFM Clustering**: RFM segment treemaps, cluster behavioral matrix, churn risk profiles.
6. **Product Holdings & Cross-Sell Opportunities**: Product penetration rates, co-occurrence analysis, wallet share expansion targets.

---

## 9. How to Run

### Setup Environment
```bash
git clone https://github.com/rohitparmar08/financial-consumer-behavior-analytics.git
cd financial-consumer-behavior-analytics

python -m venv .venv
# On Windows: .venv\Scripts\activate  (On macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

### Run Full Pipeline (Stages 1 through 7)
```bash
python run_pipeline.py --all
```

### Run Pytest Suite
```bash
pytest tests/ -v
```

---

## 10. Documentation Index

- [`docs/data_dictionary.md`](docs/data_dictionary.md): Comprehensive 8-entity data dictionary.
- [`docs/analytics_methodology.md`](docs/analytics_methodology.md): Business segmentation & RFM methodology.
- [`docs/powerbi_data_model.md`](docs/powerbi_data_model.md): Star Schema definition, grains, and relationship matrix.
- [`docs/powerbi_dashboard_specification.md`](docs/powerbi_dashboard_specification.md): Detailed visual specs for 6 dashboard pages.
- [`docs/interview_guide.md`](docs/interview_guide.md): Technical, DAX, and domain interview Q&A guide.
- [`powerbi/dax_measures.md`](powerbi/dax_measures.md): Complete library of 50+ DAX measures.
- [`powerbi/theme.json`](powerbi/theme.json): Custom corporate Power BI visual theme.
- [`powerbi/README.md`](powerbi/README.md): Step-by-step Power BI import instructions.
