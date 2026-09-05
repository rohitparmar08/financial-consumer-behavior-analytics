# Data Dictionary

This document details the schema, data types, business definitions, allowed values, and relationship constraints for all 8 entities in the **Financial / Consumer Behavior Analytics** relational database model.

---

## 1. CUSTOMERS Table

Primary key entity containing customer demographic profile and relationship tenure.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `customer_id` | TEXT | Primary Key | No | Unique identifier for each customer | `CUST-00001` |
| `age` | INTEGER | - | No | Age of customer in years | `18` to `75` |
| `gender` | TEXT | - | No | Self-identified gender | `Male`, `Female`, `Non-Binary` |
| `education` | TEXT | - | No | Highest level of education completed | `High School`, `Associate`, `Bachelor's`, `Master's`, `Doctorate` |
| `employment_status` | TEXT | - | No | Current employment classification | `Employed`, `Self-Employed`, `Unemployed`, `Retired`, `Student` |
| `marital_status` | TEXT | - | No | Marital status | `Single`, `Married`, `Divorced`, `Widowed` |
| `city_tier` | TEXT | - | No | Geographic tier classification based on cost of living | `Tier 1`, `Tier 2`, `Tier 3` |
| `occupation` | TEXT | - | No | Industry sector or professional domain | `Software/Tech`, `Healthcare`, `Finance/Banking`, etc. |
| `customer_since` | DATE | - | No | Date customer opened initial relationship with institution | `YYYY-MM-DD` (e.g. `2021-04-15`) |

---

## 2. INCOME Table

Financial earnings entity linked 1:1 with Customers.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `income_id` | TEXT | Primary Key | No | Unique identifier for income record | `INC-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `monthly_income` | REAL | - | No | Total monthly gross income ($) | `$500.00` to `$25,000.00+` |
| `annual_income` | REAL | - | No | Annualized income derived as `monthly_income * 12` | `$6,000.00` to `$300,000.00+` |
| `income_source` | TEXT | - | No | Primary source of earnings | `Salary`, `Business`, `Investment`, `Freelance`, `Pension/Government` |
| `income_stability` | TEXT | - | Yes | Assessment of income consistency | `High`, `Medium`, `Low` |

---

## 3. EXPENSES Table

Monthly household expense breakdown linked 1:1 with Customers.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `expense_id` | TEXT | Primary Key | No | Unique identifier for expense record | `EXP-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `housing_expense` | REAL | - | No | Rent or mortgage housing monthly outlay ($) | `$150.00`+ |
| `food_expense` | REAL | - | No | Groceries and food expenditure ($) | `$100.00`+ |
| `transportation_expense` | REAL | - | No | Transit, fuel, car maintenance cost ($) | `$50.00`+ |
| `healthcare_expense` | REAL | - | No | Medical out-of-pocket & premiums ($) | `$30.00`+ |
| `entertainment_expense` | REAL | - | No | Leisure, dining, subscription outlay ($) | `$20.00`+ |
| `utilities_expense` | REAL | - | No | Electricity, water, internet, phone bill ($) | `$40.00`+ |
| `other_expense` | REAL | - | No | Miscellaneous monthly costs ($) | `$20.00`+ |
| `total_monthly_expense` | REAL | - | No | Sum of all monthly expense categories | Derived positive sum ($) |

---

## 4. SAVINGS Table

Accumulated savings and liquid emergency reserves linked 1:1 with Customers.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `savings_id` | TEXT | Primary Key | No | Unique identifier for savings record | `SAV-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `monthly_savings` | REAL | - | No | Net monthly allocation into savings ($) | `$0.00`+ |
| `savings_balance` | REAL | - | No | Total accumulated liquid savings balance ($) | `$0.00` to `$150,000.00+` |
| `savings_rate` | REAL | - | No | Ratio of monthly savings to monthly income | `0.0000` to `0.8500` |
| `emergency_fund_status` | TEXT | - | No | Preparedness tier based on months of expenses saved | `Fully Funded` (>=6m), `Partially Funded` (3-6m), `Low` (1-3m), `None` (<1m) |

---

## 5. DEBT Table

Outstanding liabilities across credit lines linked 1:1 with Customers.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `debt_id` | TEXT | Primary Key | No | Unique identifier for debt record | `DEBT-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `credit_card_debt` | REAL | - | No | Revolving credit card balance ($) | `$0.00` to `$15,000.00` |
| `personal_loan` | REAL | - | No | Unsecured personal loan balance ($) | `$0.00` to `$30,000.00` |
| `education_loan` | REAL | - | No | Student loan principal balance ($) | `$0.00` to `$60,000.00` |
| `vehicle_loan` | REAL | - | No | Auto financing balance ($) | `$0.00` to `$40,000.00` |
| `mortgage` | REAL | - | No | Real estate mortgage balance ($) | `$0.00` to `$500,000.00` |
| `total_debt` | REAL | - | No | Aggregate principal liability balance ($) | Sum of liabilities |
| `debt_to_income_ratio` | REAL | - | No | Estimated monthly debt service / monthly income | `0.0000` to `2.5000` |

---

## 6. CREDIT Table

Credit bureau risk indicators linked 1:1 with Customers.

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `credit_id` | TEXT | Primary Key | No | Unique identifier for credit record | `CRED-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `credit_score` | INTEGER | - | No | Standard credit score (FICO scale) | `300` to `850` |
| `payment_behavior` | TEXT | - | No | Historical repayment behavior flag | `On-Time`, `Occasional Late`, `Frequently Late`, `Default Risk` |
| `missed_payments` | INTEGER | - | No | Count of missed payments in trailing 24 months | `0` to `12` |
| `credit_utilization` | REAL | - | No | Ratio of used credit to total credit limit | `0.00` to `1.00` |
| `credit_risk_category` | TEXT | - | No | Bureau risk tier assignment | `Low Risk` (750+), `Medium Risk` (670-749), `High Risk` (580-669), `Very High Risk` (<580) |

---

## 7. TRANSACTIONS Table

Granular individual transaction log table (1:N with Customers).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `transaction_id` | TEXT | Primary Key | No | Unique identifier for transaction record | `TXN-0000001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `transaction_date` | DATETIME | - | No | Timestamp of transaction | `YYYY-MM-DD HH:MM:SS` |
| `transaction_type` | TEXT | - | No | Cash flow direction | `Debit`, `Credit` |
| `category` | TEXT | - | No | Spending category | `Groceries`, `Dining`, `Shopping`, `Utilities`, `Travel`, `Healthcare`, `Entertainment`, `Education`, `Subscription`, `Transfer` |
| `amount` | REAL | - | No | Transaction dollar magnitude ($) | `$1.00` to `$3,000.00+` |
| `payment_method` | TEXT | - | No | Channel used for payment | `Credit Card`, `Debit Card`, `Bank Transfer`, `Digital Wallet`, `Cash` |
| `merchant_type` | TEXT | - | Yes | Merchant classification | `Supermarket`, `Online Retail`, `Restaurant`, `Service Provider`, `Electronics`, `Gas Station`, `Apparel`, `Healthcare` |

---

## 8. FINANCIAL_PRODUCTS Table

Product relationship and adoption history table (1:N with Customers).

| Column | Data Type | Key Type | Nullable | Description & Business Meaning | Allowed / Example Values |
|---|---|---|---|---|---|
| `product_id` | TEXT | Primary Key | No | Unique identifier for product holding | `PROD-00001` |
| `customer_id` | TEXT | Foreign Key | No | References `CUSTOMERS(customer_id)` | `CUST-00001` |
| `product_type` | TEXT | - | No | Financial product offering type | `Savings Account`, `Credit Card`, `Personal Loan`, `Mortgage`, `Investment Account`, `Auto Loan`, `Retirement Account` |
| `product_status` | TEXT | - | No | Operational status of holding | `Active`, `Closed`, `Pending`, `Churned` |
| `signup_date` | DATE | - | No | Date product was opened | `YYYY-MM-DD` |
