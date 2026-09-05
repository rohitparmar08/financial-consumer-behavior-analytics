-- ====================================================================
-- View: Customer Business Segments Summary
-- Path: sql/views/03_vw_customer_segments.sql
-- Description: Aggregates metrics and percentages across the 7 business segments.
-- ====================================================================

DROP VIEW IF EXISTS vw_customer_segments;

CREATE VIEW vw_customer_segments AS
SELECT 
    customer_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_of_total_customers,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(savings_rate) * 100, 2) AS avg_savings_rate_pct,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(debt_to_income_ratio), 4) AS avg_dti_ratio,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(total_transactions), 1) AS avg_transactions_per_customer,
    ROUND(AVG(total_transaction_amount), 2) AS avg_transaction_amount_per_customer,
    ROUND(AVG(active_products), 2) AS avg_active_products
FROM vw_customer_financial_profile
GROUP BY customer_segment;
