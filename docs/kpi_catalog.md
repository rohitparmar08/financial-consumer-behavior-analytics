# Comprehensive Key Performance Indicator (KPI) Catalog

## Financial / Consumer Behavior Analytics

This document serves as the master KPI dictionary for the **Financial / Consumer Behavior Analytics** data pipeline, SQL data warehouse, and Power BI semantic data model.

---

## 1. Customer & Portfolio KPIs

### Total Active Customers (`[Total Customers]`)
* **Business Definition**: The total count of unique retail banking customers in the active portfolio.
* **Formula**: $\sum 1 \text{ for each distinct } \text{customer\_id}$
* **Source Entity / View**: `CUSTOMERS` table / `vw_customer_financial_profile`
* **SQL Source**: `SELECT COUNT(DISTINCT customer_id) FROM customers;`
* **DAX Source**: `Total Customers = COUNTROWS(dim_customer)`
* **Table Grain**: Customer Grain (1 row per customer)
* **Interpretation**: Baseline metric for overall portfolio scale.
* **Caveats**: Excludes deleted or fully offboarded historical test accounts.

### Customer Tenure (`[Avg Customer Tenure Years]`)
* **Business Definition**: The average number of years a customer has maintained an active account relationship with the bank.
* **Formula**: $\frac{1}{N} \sum (\text{Report Date} - \text{customer\_since}) / 365.25$
* **Source Entity / View**: `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG((JULIANDAY('2025-12-31') - JULIANDAY(customer_since)) / 365.25) FROM customers;`
* **DAX Source**: `Avg Customer Tenure Years = AVERAGE(dim_customer[customer_tenure_years])`
* **Table Grain**: Customer Grain
* **Interpretation**: Measures portfolio loyalty and age of relationship.

---

## 2. Income & Financial Profile KPIs

### Total Annual Income (`[Total Annual Income]`)
* **Business Definition**: Total gross annual earnings across all customers in the portfolio.
* **Formula**: $\sum \text{annual\_income}$
* **Source Entity / View**: `INCOME` table / `vw_customer_financial_profile`
* **SQL Source**: `SELECT SUM(annual_income) FROM income;`
* **DAX Source**: `Total Annual Income = SUM(fact_customer_financial[annual_income])`
* **Table Grain**: Customer Grain
* **Interpretation**: Quantifies total earning power and top-line wealth generation capacity of the customer base.

### Average Annual Income (`[Avg Annual Income]`)
* **Business Definition**: Mean annual income per customer.
* **Formula**: $\frac{\sum \text{annual\_income}}{N}$
* **Source Entity / View**: `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG(annual_income) FROM income;`
* **DAX Source**: `Avg Annual Income = AVERAGE(fact_customer_financial[annual_income])`
* **Table Grain**: Customer Grain
* **Interpretation**: Benchmark metric for customer earning capacity.

---

## 3. Expense & Outlay KPIs

### Expense-to-Income Ratio (`[Avg Expense to Income Ratio %]`)
* **Business Definition**: The percentage of monthly gross income consumed by total monthly living expenses.
* **Formula**: $\frac{\text{total\_monthly\_expense}}{\text{monthly\_income}} \times 100$
* **Source Entity / View**: `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG(total_monthly_expense / monthly_income) * 100 FROM vw_customer_financial_profile;`
* **DAX Source**: `Avg Expense to Income Ratio % = AVERAGE(fact_customer_financial[expense_to_income_ratio])`
* **Table Grain**: Customer Grain
* **Interpretation**: Indicates cash flow strain; values $>70\%$ signal high living expense vulnerability.

---

## 4. Savings & Liquidity KPIs

### Total Liquid Assets (`[Total Liquid Assets]`)
* **Business Definition**: Total cash deposits held in savings accounts across the customer portfolio.
* **Formula**: $\sum \text{savings\_balance}$
* **Source Entity / View**: `SAVINGS` table / `vw_customer_financial_profile`
* **SQL Source**: `SELECT SUM(savings_balance) FROM savings;`
* **DAX Source**: `Total Liquid Assets = SUM(fact_customer_financial[savings_balance])`
* **Table Grain**: Customer Grain
* **Interpretation**: Represents bank deposit liquidity reserve base.

### Average Savings Rate (`[Avg Savings Rate %]`)
* **Business Definition**: The proportion of monthly disposable income saved into interest-bearing savings accounts.
* **Formula**: $\frac{\text{monthly\_savings}}{\text{monthly\_income}} \times 100$
* **Source Entity / View**: `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG(savings_rate) * 100 FROM savings;`
* **DAX Source**: `Avg Savings Rate % = AVERAGE(fact_customer_financial[savings_rate])`
* **Table Grain**: Customer Grain
* **Interpretation**: Measures household wealth accumulation discipline (Target $\ge 20\%$).

---

## 5. Debt & Liability KPIs

### Total Portfolio Debt (`[Total Debt]`)
* **Business Definition**: The aggregate sum of all credit card, personal, vehicle, education, and mortgage debt obligations.
* **Formula**: $\sum (\text{credit\_card\_debt} + \text{personal\_loan} + \text{education\_loan} + \text{vehicle\_loan} + \text{mortgage})$
* **Source Entity / View**: `DEBT` table / `vw_customer_financial_profile`
* **SQL Source**: `SELECT SUM(total_debt) FROM debt;`
* **DAX Source**: `Total Debt = SUM(fact_customer_financial[total_debt])`
* **Table Grain**: Customer Grain
* **Interpretation**: Quantifies total credit exposure across the institution.

### Debt-to-Income Ratio (`[Avg Debt to Income Ratio %]`)
* **Business Definition**: The ratio of total debt liabilities to annual gross income.
* **Formula**: $\frac{\text{total\_debt}}{\text{annual\_income}} \times 100$
* **Source Entity / View**: `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG(debt_to_income_ratio) * 100 FROM vw_customer_financial_profile;`
* **DAX Source**: `Avg Debt to Income Ratio % = AVERAGE(fact_customer_financial[debt_to_income_ratio])`
* **Table Grain**: Customer Grain
* **Interpretation**: Solvency indicator; DTI $>43\%$ indicates high leverage default risk.

---

## 6. Credit & Risk KPIs

### Average Credit Score (`[Avg Credit Score]`)
* **Business Definition**: Mean FICO credit score across all portfolio accounts.
* **Formula**: $\frac{\sum \text{credit\_score}}{N}$
* **Source Entity / View**: `CREDIT` table / `vw_customer_financial_profile`
* **SQL Source**: `SELECT AVG(credit_score) FROM credit;`
* **DAX Source**: `Avg Credit Score = AVERAGE(fact_customer_financial[credit_score])`
* **Table Grain**: Customer Grain
* **Interpretation**: Overall portfolio creditworthiness metric.

### Delinquent Rate (`[Delinquent Rate %]`)
* **Business Definition**: The percentage of customers with 3 or more missed payments or classified in 'High'/'Very High' risk categories.
* **Formula**: $\frac{\text{Count of Delinquent Customers}}{N} \times 100$
* **Source Entity / View**: `vw_financial_risk_summary`
* **SQL Source**: `SELECT (COUNT(CASE WHEN missed_payments >= 3 THEN 1 END) * 100.0 / COUNT(*)) FROM credit;`
* **DAX Source**: `Delinquent Rate % = DIVIDE(CALCULATE(COUNTROWS(dim_customer), fact_customer_financial[missed_payments] >= 3), [Total Customers], 0)`
* **Table Grain**: Customer Grain
* **Interpretation**: Core credit loss forecasting metric.

---

## 7. Portfolio Financial Health Index KPI

### Financial Health Score (`[Avg Financial Health Score]`)
* **Business Definition**: A composite index (0–100) combining Savings Rate (30 pts), DTI Ratio (25 pts), Credit Score (25 pts), and Payment Reliability (20 pts).
* **Formula**: $\text{Savings\_Pts}(30) + \text{DTI\_Pts}(25) + \text{Credit\_Pts}(25) + \text{Payment\_Pts}(20)$
* **Source Entity / View**: `fact_customer_financial.csv` / Derived SQL logic
* **SQL Source**: Evaluated in `export_powerbi_tables.py`
* **DAX Source**: `Avg Financial Health Score = AVERAGE(fact_customer_financial[financial_health_score])`
* **Table Grain**: Customer Grain
* **Interpretation**: Macro portfolio resilience metric ($>70$ Healthy, $50-69$ Vulnerable, $<50$ High Risk).
* **Caveats**: Portfolio demonstration index, not a regulated credit rating score.

---

## 8. Transaction & Behavioral KPIs

### Total Spend Volume (`[Total Spend Volume]`)
* **Business Definition**: Sum of all debit and credit card transaction amounts processed.
* **Formula**: $\sum \text{amount}$
* **Source Entity / View**: `TRANSACTIONS` table / `vw_monthly_transaction_summary`
* **SQL Source**: `SELECT SUM(amount) FROM transactions;`
* **DAX Source**: `Total Spend Volume = SUM(fact_transactions[amount])`
* **Table Grain**: Transaction Grain (1 row per transaction)
* **Interpretation**: Total debit/credit monetary outflow volume.

---

## 9. Product & Segmentation KPIs

### Average Products per Customer (`[Avg Products Per Customer]`)
* **Business Definition**: Average number of financial banking products held per customer.
* **Formula**: $\frac{\sum \text{total\_products}}{N}$
* **Source Entity / View**: `vw_product_adoption_summary`
* **SQL Source**: `SELECT AVG(total_products) FROM vw_customer_financial_profile;`
* **DAX Source**: `Avg Products Per Customer = AVERAGE(fact_customer_financial[total_products])`
* **Table Grain**: Customer Grain
* **Interpretation**: Measures product cross-sell penetration and relationship depth.
