# SQL Analytics & Views Sitemap

This directory contains the analytical views, relational schemas, and structured SQL analysis scripts for the **Financial / Consumer Behavior Analytics** project.

---

## 1. Directory Structure

```
sql/
├── schema/
│   ├── 01_create_tables.sql            # DDL table creation with PK/FK constraints
│   └── 02_create_indexes.sql           # Performance indexing script
├── views/                              # Reusable SQLite Analytical Views
│   ├── 01_vw_customer_financial_profile.sql
│   ├── 02_vw_customer_behavior_summary.sql
│   ├── 03_vw_customer_segments.sql
│   ├── 04_vw_rfm_segments.sql
│   ├── 05_vw_monthly_transaction_summary.sql
│   ├── 06_vw_product_adoption_summary.sql
│   └── 07_vw_financial_risk_summary.sql
├── analysis/                           # 12 Structured Analytical Query Modules
│   ├── 01_initial_validation_queries.sql
│   ├── 02_customer_financial_profile.sql
│   ├── 03_income_expense_analysis.sql
│   ├── 04_savings_analysis.sql
│   ├── 05_debt_credit_analysis.sql
│   ├── 06_transaction_analysis.sql
│   ├── 07_financial_product_analysis.sql
│   ├── 08_customer_segmentation.sql
│   ├── 09_rfm_analysis.sql
│   ├── 10_window_function_analysis.sql
│   ├── 11_cohort_analysis.sql
│   └── 12_business_opportunity_analysis.sql
└── README.md
```

---

## 2. Reusable Analytical Views

| View Name | Primary Key / Multiplicity | Purpose & Content |
|---|---|---|
| `vw_customer_financial_profile` | `customer_id` (1 row/cust, 15,000 rows) | Master customer view combining demographics, earnings, expenses, savings, debt, credit, aggregated transactions, product count, and 7 business segments. |
| `vw_customer_behavior_summary` | `(city_tier, employment_status, education)` | Demographic aggregation of financial health KPIs. |
| `vw_customer_segments` | `customer_segment` | Summary of customer counts and averages across the 7 business segments. |
| `vw_rfm_segments` | `customer_id` (15,000 rows) | Recency, Frequency, Monetary NTILE(5) scores and RFM segment labels. |
| `vw_monthly_transaction_summary` | `(year_month, category)` | Monthly aggregate spend, transaction count, debit/credit breakdown by category. |
| `vw_product_adoption_summary` | `(product_type, product_status, income_band)` | Product penetration and status breakdown across income bands. |
| `vw_financial_risk_summary` | `(credit_risk_category, debt_risk_tier)` | Delinquency matrix combining credit risk and debt burden. |

---

## 3. How to Execute SQL Scripts

All SQL views and analysis scripts are executed via the automated runner:

```bash
# Execute views, analysis scripts, and export CSVs to data/exports/
python src/database/run_sql_analysis.py

# Or via main pipeline CLI:
python run_pipeline.py --analytics
```

---

## 4. Power BI Star Schema Preparation (Part 3 Mapping)

The analytical views map directly to a Power BI dimensional model:

- **Fact Table**: `vw_customer_financial_profile` (Customer Fact) & `vw_monthly_transaction_summary` (Transaction Fact)
- **Dimension Tables**: `vw_customer_segments` (Segment Dim), `vw_rfm_segments` (RFM Dim), `vw_financial_risk_summary` (Risk Dim)
