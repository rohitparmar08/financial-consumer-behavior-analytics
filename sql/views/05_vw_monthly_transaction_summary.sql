-- ====================================================================
-- View: Monthly Transaction Performance Summary
-- Path: sql/views/05_vw_monthly_transaction_summary.sql
-- Description: Aggregates transaction counts, spend, category breakdown,
-- and active customer counts by year and month.
-- ====================================================================

DROP VIEW IF EXISTS vw_monthly_transaction_summary;

CREATE VIEW vw_monthly_transaction_summary AS
SELECT 
    STRFTIME('%Y-%m', transaction_date) AS year_month,
    STRFTIME('%Y', transaction_date) AS txn_year,
    STRFTIME('%m', transaction_date) AS txn_month,
    category,
    COUNT(transaction_id) AS total_transactions,
    COUNT(DISTINCT customer_id) AS active_transacting_customers,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_transaction_amount,
    SUM(CASE WHEN transaction_type = 'Debit' THEN 1 ELSE 0 END) AS debit_count,
    SUM(CASE WHEN transaction_type = 'Credit' THEN 1 ELSE 0 END) AS credit_count,
    ROUND(SUM(CASE WHEN transaction_type = 'Debit' THEN amount ELSE 0 END), 2) AS total_debit_amount,
    ROUND(SUM(CASE WHEN transaction_type = 'Credit' THEN amount ELSE 0 END), 2) AS total_credit_amount
FROM transactions
GROUP BY STRFTIME('%Y-%m', transaction_date), category;
