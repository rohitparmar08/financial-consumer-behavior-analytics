-- ====================================================================
-- Analysis 11: Customer Acquisition Cohort Analysis
-- Path: sql/analysis/11_cohort_analysis.sql
-- Analyzes customer tenure, engagement, and holdings by acquisition cohort year.
-- ====================================================================

-- 1. Acquisition Cohort Performance Summary (Acquisition Year)
SELECT 
    STRFTIME('%Y', customer_since) AS cohort_year,
    COUNT(customer_id) AS cohort_size,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_of_total_customers,
    ROUND(AVG(customer_tenure_years), 2) AS avg_tenure_years,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(savings_balance), 2) AS avg_savings_balance,
    ROUND(AVG(total_debt), 2) AS avg_total_debt,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(total_transactions), 1) AS avg_transactions_per_customer,
    ROUND(AVG(total_transaction_amount), 2) AS avg_spend_per_customer,
    ROUND(AVG(total_products), 2) AS avg_products_held
FROM vw_customer_financial_profile
GROUP BY STRFTIME('%Y', customer_since)
ORDER BY cohort_year ASC;

-- 2. Quarterly Acquisition Retention & Activity Distribution
SELECT 
    STRFTIME('%Y-Q', customer_since) AS cohort_quarter,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(active_products), 2) AS avg_active_products,
    SUM(CASE WHEN total_transactions > 5 THEN 1 ELSE 0 END) AS highly_active_transactors
FROM vw_customer_financial_profile
GROUP BY STRFTIME('%Y-Q', customer_since)
ORDER BY cohort_quarter ASC;
