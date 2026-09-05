-- ====================================================================
-- Analysis 07: Financial Product Adoption & Cross-Sell Opportunities
-- Path: sql/analysis/07_financial_product_analysis.sql
-- ====================================================================

-- 1. Product Penetration Distribution (0, 1, 2, 3+ Products)
SELECT 
    total_products,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customers,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile
GROUP BY total_products
ORDER BY total_products ASC;

-- 2. Product Status Breakdown by Product Type
SELECT 
    product_type,
    SUM(CASE WHEN product_status = 'Active' THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN product_status = 'Closed' THEN 1 ELSE 0 END) AS closed_count,
    SUM(CASE WHEN product_status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN product_status = 'Churned' THEN 1 ELSE 0 END) AS churned_count,
    COUNT(*) AS total_holdings,
    ROUND(SUM(CASE WHEN product_status = 'Active' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS active_rate_pct
FROM financial_products
GROUP BY product_type
ORDER BY total_holdings DESC;

-- 3. Product Adoption by Income Band
SELECT 
    income_band,
    ROUND(AVG(total_products), 2) AS avg_products_held,
    ROUND(AVG(active_products), 2) AS avg_active_products
FROM vw_customer_financial_profile
GROUP BY income_band
ORDER BY avg_products_held DESC;
