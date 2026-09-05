-- ====================================================================
-- Initial Validation SQL Queries: Financial / Consumer Behavior Analytics
-- Verifies database row counts, total financial metrics, customer segmentation,
-- credit risk distributions, and foreign key integrity.
-- ====================================================================

-- 1. High-Level Entity Counts & Summary Financial Totals
SELECT 
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM transactions) AS total_transactions,
    (SELECT COUNT(*) FROM financial_products) AS total_financial_products,
    (SELECT ROUND(SUM(annual_income), 2) FROM income) AS aggregate_annual_income,
    (SELECT ROUND(SUM(total_monthly_expense * 12), 2) FROM expenses) AS aggregate_annual_expenses,
    (SELECT ROUND(SUM(savings_balance), 2) FROM savings) AS aggregate_savings_balance,
    (SELECT ROUND(SUM(total_debt), 2) FROM debt) AS aggregate_total_debt,
    (SELECT ROUND(AVG(credit_score), 1) FROM credit) AS avg_credit_score;

-- 2. Customer Counts by Employment Status and Education Level
SELECT 
    education,
    employment_status,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total
FROM customers
GROUP BY education, employment_status
ORDER BY education, customer_count DESC;

-- 3. Income & Savings Summary by City Tier
SELECT 
    c.city_tier,
    COUNT(c.customer_id) AS customer_count,
    ROUND(AVG(i.monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(e.total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(s.savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(s.savings_rate) * 100, 2) AS avg_savings_rate_pct
FROM customers c
JOIN income i ON c.customer_id = i.customer_id
JOIN expenses e ON c.customer_id = e.customer_id
JOIN savings s ON c.customer_id = s.customer_id
GROUP BY c.city_tier
ORDER BY avg_monthly_income DESC;

-- 4. Debt & Credit Risk Distribution by Customer Risk Tier
SELECT 
    cr.credit_risk_category,
    COUNT(cr.customer_id) AS customer_count,
    ROUND(AVG(cr.credit_score), 1) AS avg_credit_score,
    ROUND(AVG(cr.credit_utilization) * 100, 2) AS avg_credit_util_pct,
    ROUND(AVG(d.total_debt), 2) AS avg_total_debt,
    ROUND(AVG(d.debt_to_income_ratio), 4) AS avg_dti_ratio
FROM credit cr
JOIN debt d ON cr.customer_id = d.customer_id
GROUP BY cr.credit_risk_category
ORDER BY avg_credit_score DESC;

-- 5. Top Spending Categories by Volume & Transaction Amount
SELECT 
    category,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_transaction_amount
FROM transactions
GROUP BY category
ORDER BY total_amount DESC;

-- 6. Foreign Key Integrity Check (Returns 0 rows if 100% clean)
SELECT 'income' AS child_table, COUNT(*) AS orphaned_records 
FROM income WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'expenses', COUNT(*) FROM expenses WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'savings', COUNT(*) FROM savings WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'debt', COUNT(*) FROM debt WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'credit', COUNT(*) FROM credit WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions WHERE customer_id NOT IN (SELECT customer_id FROM customers)
UNION ALL
SELECT 'financial_products', COUNT(*) FROM financial_products WHERE customer_id NOT IN (SELECT customer_id FROM customers);
