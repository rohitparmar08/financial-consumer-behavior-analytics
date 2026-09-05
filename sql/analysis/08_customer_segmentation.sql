-- ====================================================================
-- Analysis 08: Customer Business Segmentation Framework
-- Path: sql/analysis/08_customer_segmentation.sql
-- ====================================================================

-- 1. Detailed Customer Count & Financial Profiling Across 7 Segments
SELECT 
    customer_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_total_customers,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(total_transactions), 1) AS avg_transactions,
    ROUND(AVG(active_products), 2) AS avg_active_products
FROM vw_customer_financial_profile
GROUP BY customer_segment
ORDER BY avg_monthly_income DESC;

-- 2. Demographic Composition of Key Business Segments
SELECT 
    customer_segment,
    city_tier,
    education,
    COUNT(customer_id) AS customer_count
FROM vw_customer_financial_profile
GROUP BY customer_segment, city_tier, education
ORDER BY customer_segment, customer_count DESC;
