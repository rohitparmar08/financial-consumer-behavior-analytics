-- ====================================================================
-- View: Customer Behavioral Summary by Demographic Dimensions
-- Path: sql/views/02_vw_customer_behavior_summary.sql
-- Description: Aggregates financial performance metrics by city tier,
-- employment status, and education level.
-- ====================================================================

DROP VIEW IF EXISTS vw_customer_behavior_summary;

CREATE VIEW vw_customer_behavior_summary AS
SELECT 
    city_tier,
    employment_status,
    education,
    COUNT(customer_id) AS total_customers,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(disposable_income), 2) AS avg_disposable_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(credit_utilization) * 100, 2) AS avg_credit_utilization_pct,
    ROUND(AVG(total_transactions), 1) AS avg_transactions_per_customer,
    ROUND(AVG(total_transaction_amount), 2) AS avg_transaction_spend,
    ROUND(AVG(active_products), 2) AS avg_active_products
FROM vw_customer_financial_profile
GROUP BY city_tier, employment_status, education;
