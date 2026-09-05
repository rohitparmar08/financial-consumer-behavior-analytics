-- ====================================================================
-- Analysis 04: Savings Behavior & Emergency Reserve Readiness
-- Path: sql/analysis/04_savings_analysis.sql
-- ====================================================================

-- 1. Savings Behavior Tier Breakdown
SELECT 
    savings_behavior_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_total,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(monthly_savings), 2) AS avg_monthly_savings,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct
FROM vw_customer_financial_profile
GROUP BY savings_behavior_tier
ORDER BY avg_savings_rate_pct DESC;

-- 2. Emergency Fund Preparedness by Employment Status
SELECT 
    employment_status,
    emergency_fund_status,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense
FROM vw_customer_financial_profile
GROUP BY employment_status, emergency_fund_status
ORDER BY employment_status, customer_count DESC;

-- 3. Relationship Between Income Band and Savings Rate
SELECT 
    income_band,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    SUM(CASE WHEN emergency_fund_status = 'Fully Funded' THEN 1 ELSE 0 END) AS fully_funded_count
FROM vw_customer_financial_profile
GROUP BY income_band
ORDER BY avg_savings_rate_pct DESC;
