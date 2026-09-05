# Power BI DAX Measure Library

This document provides the complete DAX (Data Analysis Expressions) measure library definitions, syntax, descriptions, and dynamic formatting rules for the **Financial / Consumer Behavior Analytics** Power BI semantic data model.

---

## 1. Customer & Demographic KPIs

```dax
// Total unique customer count
Total Customers = 
COUNTROWS(dim_customer)

// Active transacting customer count
Active Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[total_transactions] > 0
)

// Customers with active banking product holdings
Customers with Products = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[total_products] > 0
)

// Percentage of customers holding 2 or more products
Multi-Product Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(dim_customer), fact_customer_financial[total_products] >= 2),
    [Total Customers],
    0
)
```

---

## 2. Income & Earnings KPIs

```dax
// Total annual gross earnings across customer population
Total Annual Income = 
SUM(fact_customer_financial[annual_income])

// Average annual income per customer
Average Annual Income = 
AVERAGE(fact_customer_financial[annual_income])

// Median annual income per customer
Median Annual Income = 
MEDIAN(fact_customer_financial[annual_income])

// Average monthly gross income
Average Monthly Income = 
AVERAGE(fact_customer_financial[monthly_income])
```

---

## 3. Expense & Discretionary Income KPIs

```dax
// Total monthly household outlays
Total Monthly Expenses = 
SUM(fact_customer_financial[total_monthly_expense])

// Average monthly expenses per customer
Average Monthly Expenses = 
AVERAGE(fact_customer_financial[total_monthly_expense])

// Ratio of expenses to income
Expense to Income Ratio % = 
AVERAGE(fact_customer_financial[expense_to_income_ratio])

// Average monthly net disposable income remaining after expenses
Average Disposable Income = 
AVERAGE(fact_customer_financial[disposable_income])
```

---

## 4. Savings & Liquidity KPIs

```dax
// Total liquid savings balances
Total Savings Balance = 
SUM(fact_customer_financial[savings_balance])

// Average savings balance per customer
Average Savings Balance = 
AVERAGE(fact_customer_financial[savings_balance])

// Average savings rate percentage
Average Savings Rate % = 
AVERAGE(fact_customer_financial[savings_rate])

// Count of customers meeting Healthy or Excellent saver thresholds
High Saver Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[savings_behavior_tier] IN {"Excellent Saver", "Healthy Saver"}
)
```

---

## 5. Debt & Liabilities KPIs

```dax
// Total aggregate principal debt liabilities
Total Debt Liabilities = 
SUM(fact_customer_financial[total_debt])

// Average debt balance per customer
Average Customer Debt = 
AVERAGE(fact_customer_financial[total_debt])

// Average Debt-to-Income (DTI) ratio
Average DTI Ratio = 
AVERAGE(fact_customer_financial[debt_to_income_ratio])

// High debt burden customers (DTI >= 45%)
High Debt Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[debt_to_income_ratio] >= 0.45
)
```

---

## 6. Credit Bureau Risk KPIs

```dax
// Average FICO credit score
Average Credit Score = 
AVERAGE(fact_customer_financial[credit_score])

// Average revolving credit limit utilization
Average Credit Utilization % = 
AVERAGE(fact_customer_financial[credit_utilization])

// High credit risk customers (FICO < 670 or High Risk tier)
High Risk Credit Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[credit_risk_category] IN {"High Risk", "Very High Risk"}
)

// Customers with 1 or more missed payments in 24 months
Missed Payment Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[missed_payments] > 0
)
```

---

## 7. Transaction Velocity KPIs

```dax
// Total log transactions count
Total Transactions = 
COUNTROWS(fact_transactions)

// Total aggregate dollar volume spent across transactions
Total Transaction Spend = 
SUM(fact_transactions[amount])

// Average dollar amount per individual transaction
Average Transaction Value = 
AVERAGE(fact_transactions[amount])

// Average transaction spend per customer
Average Spend per Customer = 
DIVIDE([Total Transaction Spend], [Total Customers], 0)

// Average transaction velocity per customer
Average Transactions per Customer = 
DIVIDE([Total Transactions], [Total Customers], 0)
```

---

## 8. Financial Product Adoption KPIs

```dax
// Aggregate product holdings across institution
Total Product Holdings = 
COUNTROWS(fact_product_holdings)

// Total active product holdings
Active Product Holdings = 
CALCULATE(
    COUNTROWS(fact_product_holdings),
    fact_product_holdings[is_active] = 1
)

// Product active rate percentage
Product Active Rate % = 
DIVIDE([Active Product Holdings], [Total Product Holdings], 0)

// Average products held per customer
Average Products per Customer = 
DIVIDE([Total Product Holdings], [Total Customers], 0)
```

---

## 9. Customer Business Segmentation & RFM KPIs

```dax
// Customer share of segment
Segment Customer Share % = 
DIVIDE(
    COUNTROWS(fact_customer_financial),
    CALCULATE(COUNTROWS(fact_customer_financial), ALL(dim_customer)),
    0
)

// Champions RFM Segment Count
Champions Count = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[rfm_segment] = "Champions"
)

// At Risk RFM Segment Count
At Risk Customers Count = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[rfm_segment] = "At Risk"
)
```

---

## 10. Financial Health Score Index

```dax
// Average composite Financial Health Score (0-100 index)
Average Financial Health Score = 
AVERAGE(fact_customer_financial[financial_health_score])

// Vulnerable customer count (Health Score < 40)
Financially Vulnerable Customers = 
CALCULATE(
    COUNTROWS(dim_customer),
    fact_customer_financial[financial_health_score] < 40
)
```

---

## 11. Time Intelligence DAX Measures

```dax
// Transaction spend in previous calendar month
Previous Month Spend = 
CALCULATE(
    [Total Transaction Spend],
    PREVIOUSMONTH(dim_date[date])
)

// Month-over-Month transaction spend growth percentage
MoM Spend Growth % = 
VAR PrevSpend = [Previous Month Spend]
RETURN
DIVIDE([Total Transaction Spend] - PrevSpend, PrevSpend, 0)

// Year-to-Date cumulative transaction spend
YTD Spend = 
CALCULATE(
    [Total Transaction Spend],
    DATESYTD(dim_date[date])
)

// Year-to-Date active transacting customers
YTD Active Customers = 
CALCULATE(
    [Active Customers],
    DATESYTD(dim_date[date])
)
```
