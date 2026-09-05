# Portfolio Project Interview Guide

## Financial / Consumer Behavior Analytics

This guide prepares you to discuss and present this project in technical interviews for **Data Analyst**, **Data Engineer**, **BI Developer**, and **Analytics Engineer** roles.

---

## 1. Project Overview & Pitch

### The 30-Second Elevator Pitch
> *"I built an end-to-end Financial & Consumer Behavior Analytics pipeline that models financial health, spending behavior, credit risk, and product cross-sell opportunities across 15,000 retail banking customers and ~75,000 transactions. The project features a multi-tiered data pipeline built in Python, an analytical SQLite data warehouse with advanced SQL models, a Power BI Star Schema data model with 50+ DAX measures, and a 100% automated pytest test suite that guarantees data integrity and zero join multiplication."*

### Key Metrics to Highlight
* **15,000** distinct customers with realistic financial profiles.
* **197,018** total records across 8 base tables and 7 analytical views.
* **50+** production-ready DAX measures (KPIs, Time Intelligence, Segmentation, Risk Metrics).
* **0** Join Multiplication (verified across all star-schema relationships).
* **100%** test pass rate across automated pytest suites.

---

## 2. Technical Architecture & Data Engineering (Parts 1 & 2)

### Q1: Why did you create synthetic data instead of using a public Kaggle dataset?
**Answer**:
> *"Public datasets often lack relational complexity, suffer from inconsistent timelines, or miss key domain-specific attributes like credit score tiers, emergency reserve months, or cash flow components. I built an extensible Python data generator leveraging `Faker` and `NumPy` with seeded randomness. It creates realistic statistical distributions (e.g., log-normal income distributions, correlated credit scores and delinquency rates) and maintains strict relational integrity across 8 tables."*

### Q2: Walk me through your database architecture.
**Answer**:
> *"The data architecture follows a 3-tier medallion-style structure:*
> 1. **Ingestion Layer (Bronze)**: Raw CSV generation and relational database population into SQLite.
> 2. **Transformation Layer (Silver/Gold)**: Analytical SQL views (`v_customer_financial_profile`, `v_rfm_segmentation`, `v_credit_risk_analysis`, etc.) that compute rolling cash flows, debt-to-income ratios, and RFM scores.
> 3. **Export Layer (Star Schema)**: Dimension and fact table exporters producing clean CSVs tuned specifically for Power BI reporting."*

### Q3: How did you ensure data reconciliation between your SQL analytical views and Power BI exports?
**Answer**:
> *"I wrote an automated reconciliation validation script (`src/validation/validate_powerbi_exports.py`) and corresponding unit tests (`tests/test_reconciliation.py` and `tests/test_powerbi_model.py`). These compare row counts, sum totals (e.g., total liquid assets, total spend volume), and key uniqueness between the SQLite database views and the exported Power BI Star Schema tables, flagging any discrepancies > 0.01%."*

---

## 3. Power BI & Analytical Data Modeling (Part 3)

### Q4: How is your Power BI Data Model structured, and why did you choose a Star Schema over a Single Flat Table?
**Answer**:
> *"I implemented a pure **Star Schema** consisting of 5 Dimension tables (`dim_customer`, `dim_date`, `dim_product`, `dim_segment`, `dim_risk`) and 3 Fact tables (`fact_transactions`, `fact_customer_financial`, `fact_product_holdings`).*
>
> *A single flat table introduces massive redundancy, bloats file size, and risks severe join multiplication when aggregating across different grains (e.g., transaction-level spend vs. customer-level financial net worth). A Star Schema optimizes DAX engine performance (VertiPaq compression), enforces 1-to-Many relationships, and allows clear filter context propagation."*

### Q5: What are the grains of your fact tables, and how do you prevent fan-out / double-counting?
**Answer**:
> *"Each table has a clearly defined, non-overlapping grain:*
> * `fact_transactions`: Transaction level (1 row per transaction, ~75.7k rows).
> * `fact_customer_financial`: Customer snapshot level (1 row per customer, 15,000 rows).
> * `fact_product_holdings`: Customer-product link level (1 row per customer product holding, ~31.2k rows).*
>
> *To prevent double-counting when measuring net worth or income alongside transaction volume, `fact_customer_financial` is related to `dim_customer` via a strict 1-to-1 relationship, while `fact_transactions` is related via 1-to-Many on `customer_id`. DAX measures are context-aware and reference the exact fact table appropriate for the grain."*

### Q6: Can you explain how you designed the Financial Health Score?
**Answer**:
> *"The **Financial Health Score** is a composite index (0–100) calculated across 4 weighted pillars:*
> 1. **Savings & Reserve Ratio (30 pts)**: Rewards emergency fund coverage >= 6 months and savings rate >= 20%.
> 2. **Debt Burden DTI Ratio (25 pts)**: Penalizes high Debt-to-Income (> 43% DTI incurs steep deductions).
> 3. **Credit Score & Standing (25 pts)**: Evaluates credit tier (Excellent = 25 pts, Poor = 5 pts).
> 4. **Payment & Delinquency Behavior (20 pts)**: Deducts points for late payments and delinquent statuses.*
>
> *Customers scoring >= 70 are categorized as 'Healthy', 50–69 as 'Vulnerable', and < 50 as 'High Risk'. This logic is implemented both in SQL views and in DAX measures."*

---

## 4. DAX & Advanced Calculations

### Q7: Give an example of a complex DAX measure you wrote and how it works.
**Answer**:
> *"One key measure is `[Healthy Customers Share %]`:*
> ```dax
> Healthy Customers Share % = 
> VAR HealthyCount = 
>     CALCULATE(
>         COUNTROWS(dim_customer),
>         dim_customer[financial_health_category] = "Healthy"
>     )
> VAR TotalCount = COUNTROWS(dim_customer)
> RETURN
>     DIVIDE(HealthyCount, TotalCount, 0)
> ```
> *Another example is time intelligence for YoY spend growth (`[Total Spend YoY Growth %]`):*
> ```dax
> Total Spend YoY Growth % = 
> VAR CurrentSpend = [Total Spend Volume]
> VAR PriorSpend = CALCULATE([Total Spend Volume], SAMEPERIODLASTYEAR(dim_date[Date]))
> RETURN
>     DIVIDE(CurrentSpend - PriorSpend, PriorSpend, 0)
> ```
> *By using variables (`VAR`), DAX evaluates expressions once, improving query performance, while `DIVIDE` safely handles division-by-zero errors."*

---

## 5. Business Domain & Insights

### Q8: What were the key business takeaways from your analytics?
**Answer**:
> 1. **Financial Health Vulnerability**: ~22% of the customer base falls into the 'Vulnerable' or 'High Risk' categories, driven primarily by low emergency liquid reserves (<1 month coverage) despite moderate income levels.
> 2. **Cross-Sell Opportunity**: High-income customers (Income > $100k) with credit scores > 720 hold an average of only 2.1 products, leaving significant cross-sell whitespace for investment and wealth management products.
> 3. **Channel Preference**: Digital transactions (Online + Mobile) account for ~64% of total transaction volume, but POS transactions exhibit a 35% higher average ticket size in discretionary categories.

---

## 6. Testing & Data Quality

### Q9: How do you know your data is accurate and production-ready?
**Answer**:
> *"I built an automated unit testing suite using `pytest` covering:*
> * **Primary Key Uniqueness**: Validates that all dimension tables have 0 duplicate keys.
> * **Referential Integrity**: Checks that all foreign keys in fact tables match valid primary keys in dimensions.
> * **Financial Range Sanity**: Ensures metrics like Debt-to-Income, Savings Rate, and Credit Scores fall within valid logical ranges.
> * **Cross-System Reconciliation**: Verifies that totals in Power BI export CSVs match the SQLite database exactly."*
