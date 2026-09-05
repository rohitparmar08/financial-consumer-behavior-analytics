-- ====================================================================
-- View: Financial Risk & Delinquency Matrix Summary
-- Path: sql/views/07_vw_financial_risk_summary.sql
-- Description: Aggregates risk metrics across Credit Risk Categories and Debt Risk Tiers.
-- ====================================================================

DROP VIEW IF EXISTS vw_financial_risk_summary;

CREATE VIEW vw_financial_risk_summary AS
SELECT 
    credit_risk_category,
    debt_risk_tier,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_of_total,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(missed_payments), 2) AS avg_missed_payments,
    ROUND(AVG(credit_utilization) * 100, 2) AS avg_credit_utilization_pct,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    SUM(CASE WHEN emergency_fund_status = 'None' OR emergency_fund_status = 'No Fund' THEN 1 ELSE 0 END) AS unbuffered_customers
FROM vw_customer_financial_profile
GROUP BY credit_risk_category, debt_risk_tier;
