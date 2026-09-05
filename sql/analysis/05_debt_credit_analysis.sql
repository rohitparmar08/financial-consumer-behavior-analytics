-- ====================================================================
-- Analysis 05: Debt Liabilities, Credit Risk & Delinquency Analysis
-- Path: sql/analysis/05_debt_credit_analysis.sql
-- ====================================================================

-- 1. Debt Type Distribution Across Credit Risk Categories
SELECT 
    credit_risk_category,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(credit_card_debt), 2) AS avg_cc_debt,
    ROUND(AVG(personal_loan), 2) AS avg_personal_loan,
    ROUND(AVG(education_loan), 2) AS avg_edu_loan,
    ROUND(AVG(vehicle_loan), 2) AS avg_vehicle_loan,
    ROUND(AVG(mortgage), 2) AS avg_mortgage,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti_ratio
FROM vw_customer_financial_profile
GROUP BY credit_risk_category
ORDER BY avg_total_debt DESC;

-- 2. Missed Payment Behavior vs Credit Utilization
SELECT 
    missed_payments,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(credit_utilization) * 100, 2) AS avg_utilization_pct,
    ROUND(AVG(total_debt), 2) AS avg_total_debt
FROM vw_customer_financial_profile
GROUP BY missed_payments
ORDER BY missed_payments ASC;

-- 3. Critical Risk Identification: High Debt + Low Credit Score + Missed Payments
SELECT 
    customer_id,
    age,
    income_band,
    credit_score,
    missed_payments,
    credit_utilization,
    total_debt,
    debt_to_income_ratio,
    debt_risk_tier
FROM vw_customer_financial_profile
WHERE debt_risk_tier = 'Critical Risk'
ORDER BY credit_score ASC, total_debt DESC;
