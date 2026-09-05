-- ====================================================================
-- Analysis 02: Customer Financial Profile Overview & Demographics
-- Path: sql/analysis/02_customer_financial_profile.sql
-- ====================================================================

-- 1. High-Level Summary Totals
SELECT 
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(age), 1) AS avg_age,
    ROUND(SUM(annual_income), 2) AS total_annual_income,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(total_monthly_expense * 12), 2) AS avg_annual_expense,
    ROUND(AVG(disposable_income * 12), 2) AS avg_annual_disposable_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile;

-- 2. Customer Breakdown by Age Group & Gender
SELECT 
    age_group,
    gender,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_total,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- 3. Customer Distribution by City Tier & Occupation
SELECT 
    city_tier,
    occupation,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct
FROM vw_customer_financial_profile
GROUP BY city_tier, occupation
ORDER BY city_tier, customer_count DESC;
