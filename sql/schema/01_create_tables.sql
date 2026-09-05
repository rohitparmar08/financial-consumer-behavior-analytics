-- ====================================================================
-- Database Schema DDL: Financial / Consumer Behavior Analytics
-- Database Engine: SQLite3
-- Enforces Primary Keys, Foreign Keys, and Column Constraints
-- ====================================================================

PRAGMA foreign_keys = ON;

-- --------------------------------------------------------------------
-- 1. CUSTOMERS TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    age INTEGER NOT NULL CHECK(age >= 18 AND age <= 100),
    gender TEXT NOT NULL,
    education TEXT NOT NULL,
    employment_status TEXT NOT NULL,
    marital_status TEXT NOT NULL,
    city_tier TEXT NOT NULL,
    occupation TEXT NOT NULL,
    customer_since TEXT NOT NULL
);

-- --------------------------------------------------------------------
-- 2. INCOME TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS income (
    income_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    monthly_income REAL NOT NULL CHECK(monthly_income > 0),
    annual_income REAL NOT NULL CHECK(annual_income > 0),
    income_source TEXT NOT NULL,
    income_stability TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 3. EXPENSES TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS expenses (
    expense_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    housing_expense REAL NOT NULL CHECK(housing_expense >= 0),
    food_expense REAL NOT NULL CHECK(food_expense >= 0),
    transportation_expense REAL NOT NULL CHECK(transportation_expense >= 0),
    healthcare_expense REAL NOT NULL CHECK(healthcare_expense >= 0),
    entertainment_expense REAL NOT NULL CHECK(entertainment_expense >= 0),
    utilities_expense REAL NOT NULL CHECK(utilities_expense >= 0),
    other_expense REAL NOT NULL CHECK(other_expense >= 0),
    total_monthly_expense REAL NOT NULL CHECK(total_monthly_expense >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 4. SAVINGS TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS savings (
    savings_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    monthly_savings REAL NOT NULL CHECK(monthly_savings >= 0),
    savings_balance REAL NOT NULL CHECK(savings_balance >= 0),
    savings_rate REAL NOT NULL CHECK(savings_rate >= 0 AND savings_rate <= 1),
    emergency_fund_status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 5. DEBT TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS debt (
    debt_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    credit_card_debt REAL NOT NULL CHECK(credit_card_debt >= 0),
    personal_loan REAL NOT NULL CHECK(personal_loan >= 0),
    education_loan REAL NOT NULL CHECK(education_loan >= 0),
    vehicle_loan REAL NOT NULL CHECK(vehicle_loan >= 0),
    mortgage REAL NOT NULL CHECK(mortgage >= 0),
    total_debt REAL NOT NULL CHECK(total_debt >= 0),
    debt_to_income_ratio REAL NOT NULL CHECK(debt_to_income_ratio >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 6. CREDIT TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS credit (
    credit_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL UNIQUE,
    credit_score INTEGER NOT NULL CHECK(credit_score >= 300 AND credit_score <= 850),
    payment_behavior TEXT NOT NULL,
    missed_payments INTEGER NOT NULL CHECK(missed_payments >= 0),
    credit_utilization REAL NOT NULL CHECK(credit_utilization >= 0 AND credit_utilization <= 1),
    credit_risk_category TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 7. TRANSACTIONS TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    payment_method TEXT NOT NULL,
    merchant_type TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- --------------------------------------------------------------------
-- 8. FINANCIAL_PRODUCTS TABLE
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS financial_products (
    product_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    product_type TEXT NOT NULL,
    product_status TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);
