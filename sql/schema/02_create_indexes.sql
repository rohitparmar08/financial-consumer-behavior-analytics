-- ====================================================================
-- Performance Indexes: Financial / Consumer Behavior Analytics
-- Optimizes analytical queries, aggregations, joins, and filtering
-- ====================================================================

-- Foreign Key Indexes
CREATE INDEX IF NOT EXISTS idx_income_customer_id ON income(customer_id);
CREATE INDEX IF NOT EXISTS idx_expenses_customer_id ON expenses(customer_id);
CREATE INDEX IF NOT EXISTS idx_savings_customer_id ON savings(customer_id);
CREATE INDEX IF NOT EXISTS idx_debt_customer_id ON debt(customer_id);
CREATE INDEX IF NOT EXISTS idx_credit_customer_id ON credit(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_customer_id ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_products_customer_id ON financial_products(customer_id);

-- Analytical Search & Filtering Indexes
CREATE INDEX IF NOT EXISTS idx_customers_demographics ON customers(city_tier, employment_status, education);
CREATE INDEX IF NOT EXISTS idx_credit_risk ON credit(credit_risk_category, credit_score);
CREATE INDEX IF NOT EXISTS idx_transactions_date_cat ON transactions(transaction_date, category);
CREATE INDEX IF NOT EXISTS idx_products_status_type ON financial_products(product_type, product_status);
