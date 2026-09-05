-- ====================================================================
-- Analysis 06: Transaction Patterns, Channels & Category Breakdown
-- Path: sql/analysis/06_transaction_analysis.sql
-- ====================================================================

-- 1. Total Volume & Spend by Category
SELECT 
    category,
    COUNT(*) AS total_transactions,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) AS pct_txn_volume,
    ROUND(SUM(amount), 2) AS total_spend,
    ROUND(AVG(amount), 2) AS avg_transaction_amount
FROM transactions
GROUP BY category
ORDER BY total_spend DESC;

-- 2. Payment Method Preferences by City Tier
SELECT 
    c.city_tier,
    t.payment_method,
    COUNT(t.transaction_id) AS txn_count,
    ROUND(SUM(t.amount), 2) AS total_amount
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.city_tier, t.payment_method
ORDER BY c.city_tier, txn_count DESC;

-- 3. Customer Transaction Velocity Segmentation
SELECT 
    CASE 
        WHEN total_transactions >= 10 THEN 'Frequent Transactor (10+)'
        WHEN total_transactions >= 5 THEN 'Regular Transactor (5-9)'
        WHEN total_transactions >= 2 THEN 'Occasional Transactor (2-4)'
        ELSE 'Low Engagement (<=1)'
    END AS transaction_velocity_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(total_transaction_amount), 2) AS avg_customer_total_spend,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income
FROM vw_customer_financial_profile
GROUP BY transaction_velocity_tier
ORDER BY avg_customer_total_spend DESC;
