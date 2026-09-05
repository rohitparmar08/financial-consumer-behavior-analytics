# Cross-Layer Data Reconciliation Report

## Financial / Consumer Behavior Analytics

This report presents the end-to-end data reconciliation across all 5 system layers:
1. **Raw CSV Layer** (`data/raw/*.csv`)
2. **Processed CSV Layer** (`data/processed/*.csv`)
3. **SQLite Relational Warehouse** (`database/financial_analytics.db`)
4. **Analytical SQL Views Layer** (`sql/views/*.sql`)
5. **Power BI Star-Schema Export Layer** (`data/exports/powerbi/*.csv`)

---

## 1. Grain-Level Reconciliation Matrix

| Analytical Metric / Grain | Raw CSV Layer | Processed CSV Layer | SQLite Database | Analytical Views | Power BI Star Schema | Reconciliation Status |
|---|---|---|---|---|---|---|
| **Customer Entity Count** (Customer Grain) | 15,000 | 15,000 | 15,000 | 15,000 (`vw_customer_financial_profile`) | 15,000 (`dim_customer.csv` & `fact_customer_financial.csv`) | **RECONCILED (0.00% Variance)** |
| **Transaction Record Count** (Transaction Grain) | 75,794 | 75,744 | 75,744 | 75,744 (`vw_monthly_transaction_summary` agg) | 75,744 (`fact_transactions.csv`) | **RECONCILED (-50 rows intentional noise cleanup)** |
| **Total Transaction Spend Volume** ($) | $30,332,109.12 | $30,307,811.88 | $30,307,811.88 | $30,307,811.88 | $30,307,811.88 | **RECONCILED (0.00% Variance)** |
| **Total Portfolio Annual Income** ($) | $1,089,442,848.96 | $1,089,442,848.96 | $1,089,442,848.96 | $1,089,442,848.96 | $1,089,442,848.96 | **RECONCILED (0.00% Variance)** |
| **Total Portfolio Liquid Deposits** ($) | $781,392,721.80 | $781,392,721.80 | $781,392,721.80 | $781,392,721.80 | $781,392,721.80 | **RECONCILED (0.00% Variance)** |
| **Total Portfolio Liabilities / Debt** ($) | $1,221,459,002.56 | $1,221,459,002.56 | $1,221,459,002.56 | $1,221,459,002.56 | $1,221,459,002.56 | **RECONCILED (0.00% Variance)** |
| **Product Holding Links** (Product Holding Grain) | 31,274 | 31,274 | 31,274 | 31,274 (`vw_product_adoption_summary` agg) | 31,274 (`fact_product_holdings.csv`) | **RECONCILED (0.00% Variance)** |
| **RFM Evaluated Customer Count** | N/A | N/A | 15,000 | 15,000 (`vw_rfm_segments`) | 15,000 (`fact_customer_financial.csv`) | **RECONCILED (0.00% Variance)** |

---

## 2. Segment & Category Reconciliation Breakdown

### A. Business Customer Segmentation Reconciliation (15,000 Customers)

| Business Segment Name | SQLite View (`vw_customer_financial_profile`) | Power BI Fact (`fact_customer_financial.csv`) | Share (%) | Status |
|---|---|---|---|---|
| Emerging Customers | 6,173 | 6,173 | 41.15% | **MATCH** |
| Debt-Burdened | 3,042 | 3,042 | 20.28% | **MATCH** |
| Disciplined Savers | 1,747 | 1,747 | 11.65% | **MATCH** |
| High-Income High-Spenders | 1,724 | 1,724 | 11.49% | **MATCH** |
| Financially Strong | 1,219 | 1,219 | 8.13% | **MATCH** |
| Credit-Risk Customers | 594 | 594 | 3.96% | **MATCH** |
| Low-Engagement Customers | 501 | 501 | 3.34% | **MATCH** |
| **Total Segmented Base** | **15,000** | **15,000** | **100.00%** | **MATCH** |

### B. RFM Segment Distribution Reconciliation (15,000 Customers)

| RFM Segment Name | SQLite View (`vw_rfm_segments`) | Power BI Fact (`fact_customer_financial.csv`) | Share (%) | Status |
|---|---|---|---|---|
| Needs Attention | 3,154 | 3,154 | 21.03% | **MATCH** |
| Loyal Customers | 2,999 | 2,999 | 19.99% | **MATCH** |
| Potential Loyalists | 2,463 | 2,463 | 16.42% | **MATCH** |
| Champions | 2,138 | 2,138 | 14.25% | **MATCH** |
| Lost | 1,910 | 1,910 | 12.73% | **MATCH** |
| New Customers | 1,661 | 1,661 | 11.07% | **MATCH** |
| Promising | 345 | 345 | 2.30% | **MATCH** |
| At Risk | 330 | 330 | 2.20% | **MATCH** |
| **Total RFM Base** | **15,000** | **15,000** | **100.00%** | **MATCH** |

### C. Product Adoption Reconciliation (31,274 Total Products)

| Product Type | Base Table (`financial_products`) | Active Status | Power BI (`fact_product_holdings.csv`) | Status |
|---|---|---|---|---|
| Savings Account | 15,000 | 15,000 | 15,000 | **MATCH** |
| Investment Account | 2,735 | 1,993 | 2,735 | **MATCH** |
| Retirement Account | 2,733 | 2,045 | 2,733 | **MATCH** |
| Auto Loan | 2,720 | 2,010 | 2,720 | **MATCH** |
| Personal Loan | 2,703 | 2,018 | 2,703 | **MATCH** |
| Mortgage | 2,697 | 1,995 | 2,697 | **MATCH** |
| Credit Card | 2,686 | 2,034 | 2,686 | **MATCH** |
| **Total Product Holdings** | **31,274** | **27,085** | **31,274** | **MATCH** |

---

## 3. Explanations for Intentional Data Variations

1. **Raw (75,794) vs Processed (75,744) Transaction Count Difference**:
   - *Explanation*: During Stage 1 synthetic generation, 50 intentional noise records (out-of-bound transaction amounts < $0 or corrupted dates) were injected into raw data to simulate real-world ETL ingestion challenges. Stage 2 Data Cleaner filtered these 50 invalid records, yielding exactly 75,744 clean, valid transactions preserved through all downstream layers.

2. **Customer Financial Profile Grain (1:1) vs Transaction Grain (1:N)**:
   - *Explanation*: Customer income, debt, and liquid asset totals are evaluated at the customer snapshot grain (1 row per customer, 15,000 rows). Combining customer net worth directly with transaction rows without star-schema relationships would cause a 5.05x fan-out multiplication. The Power BI Star Schema prevents this by linking `dim_customer` via a 1:1 relationship to `fact_customer_financial` and a 1:N relationship to `fact_transactions`.
