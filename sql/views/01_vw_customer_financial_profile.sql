-- ====================================================================
-- View: Master Customer Analytical Profile
-- Path: sql/views/01_vw_customer_financial_profile.sql
-- Description: Master analytical customer dataset combining demographics,
-- earnings, expenses, savings, debt, credit, transaction aggregations,
-- product holdings, and derived behavioral classifications.
-- Multiplicity: Exactly ONE row per customer (15,000 rows).
-- ====================================================================

DROP VIEW IF EXISTS vw_customer_financial_profile;

CREATE VIEW vw_customer_financial_profile AS
WITH transaction_summary AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_transactions,
        ROUND(SUM(amount), 2) AS total_transaction_amount,
        ROUND(AVG(amount), 2) AS avg_transaction_amount,
        MAX(transaction_date) AS last_transaction_date
    FROM transactions
    GROUP BY customer_id
),
product_summary AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_products,
        SUM(CASE WHEN product_status = 'Active' THEN 1 ELSE 0 END) AS active_products
    FROM financial_products
    GROUP BY customer_id
)
SELECT 
    -- 1. Base Demographics
    c.customer_id,
    c.age,
    CASE 
        WHEN c.age < 25 THEN '18-24'
        WHEN c.age < 35 THEN '25-34'
        WHEN c.age < 50 THEN '35-49'
        WHEN c.age < 65 THEN '50-64'
        ELSE '65+'
    END AS age_group,
    c.gender,
    c.education,
    c.employment_status,
    c.marital_status,
    c.city_tier,
    c.occupation,
    c.customer_since,
    ROUND((JULIANDAY('2025-12-31') - JULIANDAY(c.customer_since)) / 365.25, 2) AS customer_tenure_years,

    -- 2. Income Metrics
    i.income_id,
    i.monthly_income,
    i.annual_income,
    i.income_source,
    i.income_stability,
    CASE 
        WHEN i.monthly_income < 2500 THEN 'Low (<$2.5k)'
        WHEN i.monthly_income < 6000 THEN 'Middle ($2.5k-$6k)'
        WHEN i.monthly_income < 10000 THEN 'Upper-Middle ($6k-$10k)'
        ELSE 'High (>$10k)'
    END AS income_band,

    -- 3. Expense Metrics
    e.expense_id,
    e.housing_expense,
    e.food_expense,
    e.transportation_expense,
    e.healthcare_expense,
    e.entertainment_expense,
    e.utilities_expense,
    e.other_expense,
    e.total_monthly_expense,
    ROUND(e.total_monthly_expense / i.monthly_income, 4) AS expense_to_income_ratio,
    ROUND(i.monthly_income - e.total_monthly_expense, 2) AS disposable_income,

    -- 4. Savings Metrics
    s.savings_id,
    s.monthly_savings,
    s.savings_balance,
    s.savings_rate,
    s.emergency_fund_status,
    ROUND(i.monthly_income - e.total_monthly_expense - s.monthly_savings, 2) AS net_savings_capacity,
    CASE 
        WHEN s.savings_rate >= 0.20 AND s.emergency_fund_status = 'Fully Funded' THEN 'Excellent Saver'
        WHEN s.savings_rate >= 0.15 THEN 'Healthy Saver'
        WHEN s.savings_rate >= 0.05 THEN 'Moderate Saver'
        ELSE 'Low Saver'
    END AS savings_behavior_tier,

    -- 5. Debt Metrics
    d.debt_id,
    d.credit_card_debt,
    d.personal_loan,
    d.education_loan,
    d.vehicle_loan,
    d.mortgage,
    d.total_debt,
    d.debt_to_income_ratio,

    -- 6. Credit Metrics
    cr.credit_id,
    cr.credit_score,
    cr.payment_behavior,
    cr.missed_payments,
    cr.credit_utilization,
    cr.credit_risk_category,
    CASE 
        WHEN cr.credit_score < 580 OR cr.missed_payments >= 3 OR d.debt_to_income_ratio >= 0.50 THEN 'Critical Risk'
        WHEN cr.credit_score < 670 OR cr.missed_payments >= 1 OR d.debt_to_income_ratio >= 0.35 THEN 'High Risk'
        WHEN cr.credit_score < 740 THEN 'Moderate Risk'
        ELSE 'Low Risk'
    END AS debt_risk_tier,

    -- 7. Transaction Aggregations (Non-Duplicating)
    COALESCE(t.total_transactions, 0) AS total_transactions,
    COALESCE(t.total_transaction_amount, 0.0) AS total_transaction_amount,
    COALESCE(t.avg_transaction_amount, 0.0) AS avg_transaction_amount,
    t.last_transaction_date,

    -- 8. Product Holdings (Non-Duplicating)
    COALESCE(p.total_products, 0) AS total_products,
    COALESCE(p.active_products, 0) AS active_products,

    -- 9. Primary Business Customer Segment
    CASE 
        WHEN i.monthly_income >= 6000 AND cr.credit_score >= 740 AND d.debt_to_income_ratio < 0.35 AND s.savings_rate >= 0.15 THEN 'Financially Strong'
        WHEN i.monthly_income >= 7500 AND (e.total_monthly_expense / i.monthly_income) >= 0.70 AND s.savings_rate < 0.15 THEN 'High-Income High-Spenders'
        WHEN i.monthly_income < 6000 AND s.savings_rate >= 0.20 AND s.emergency_fund_status = 'Fully Funded' THEN 'Disciplined Savers'
        WHEN d.debt_to_income_ratio >= 0.45 OR d.total_debt >= 50000 THEN 'Debt-Burdened'
        WHEN cr.credit_score < 580 OR cr.missed_payments >= 3 OR cr.credit_risk_category = 'Very High Risk' THEN 'Credit-Risk Customers'
        WHEN COALESCE(t.total_transactions, 0) <= 3 AND COALESCE(p.total_products, 0) <= 1 THEN 'Low-Engagement Customers'
        ELSE 'Emerging Customers'
    END AS customer_segment

FROM customers c
INNER JOIN income i ON c.customer_id = i.customer_id
INNER JOIN expenses e ON c.customer_id = e.customer_id
INNER JOIN savings s ON c.customer_id = s.customer_id
INNER JOIN debt d ON c.customer_id = d.customer_id
INNER JOIN credit cr ON c.customer_id = cr.customer_id
LEFT JOIN transaction_summary t ON c.customer_id = t.customer_id
LEFT JOIN product_summary p ON c.customer_id = p.customer_id;
