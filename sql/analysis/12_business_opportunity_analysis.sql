-- ====================================================================
-- Analysis 12: Business Opportunity & Strategic Action Framework
-- Path: sql/analysis/12_business_opportunity_analysis.sql
-- Quantifies cross-sell, savings, credit, risk, retention, and premium targets.
-- ====================================================================

-- 1. Cross-Sell Opportunity (High transaction engagement, active tenure >= 1yr, but <= 1 product)
SELECT 
    'Cross-Sell Opportunity' AS opportunity_type,
    COUNT(customer_id) AS target_customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customer_base,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile
WHERE total_transactions >= 5 AND customer_tenure_years >= 1.0 AND total_products <= 1;

-- 2. Savings Opportunity (High income >= $5k/mo, but low savings rate < 10%)
SELECT 
    'Savings Opportunity' AS opportunity_type,
    COUNT(customer_id) AS target_customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customer_base,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct
FROM vw_customer_financial_profile
WHERE monthly_income >= 5000 AND savings_rate < 0.10;

-- 3. Credit / Loan Growth Opportunity (Credit score >= 720, DTI < 0.25, credit util < 30%, no personal loan)
SELECT 
    'Credit Growth Opportunity' AS opportunity_type,
    COUNT(customer_id) AS target_customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customer_base,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile
WHERE credit_score >= 720 AND debt_to_income_ratio < 0.25 AND credit_utilization < 0.30 AND personal_loan = 0;

-- 4. Risk Mitigation Target (Credit score < 580 OR Missed Payments >= 2 OR DTI >= 0.50)
SELECT 
    'Risk Mitigation Target' AS opportunity_type,
    COUNT(customer_id) AS target_customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customer_base,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(credit_score), 1) AS avg_credit_score
FROM vw_customer_financial_profile
WHERE credit_score < 580 OR missed_payments >= 2 OR debt_to_income_ratio >= 0.50;

-- 5. Premium Wealth Management Opportunity (Income >= $8k/mo, Credit Score >= 750, Savings Rate >= 15%)
SELECT 
    'Premium Wealth Opportunity' AS opportunity_type,
    COUNT(customer_id) AS target_customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_customer_base,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance
FROM vw_customer_financial_profile
WHERE monthly_income >= 8000 AND credit_score >= 750 AND savings_rate >= 0.15;
