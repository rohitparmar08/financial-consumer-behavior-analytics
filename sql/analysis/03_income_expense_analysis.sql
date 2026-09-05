-- ====================================================================
-- Analysis 03: Income vs. Expense & Spending Capacity
-- Path: sql/analysis/03_income_expense_analysis.sql
-- ====================================================================

-- 1. Income Band Breakdown
SELECT 
    income_band,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_customer_financial_profile), 2) AS pct_total,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(AVG(total_monthly_expense), 2) AS avg_monthly_expense,
    ROUND(AVG(expense_to_income_ratio) * 100, 2) AS avg_expense_ratio_pct,
    ROUND(AVG(disposable_income), 2) AS avg_disposable_income
FROM vw_customer_financial_profile
GROUP BY income_band
ORDER BY avg_monthly_income DESC;

-- 2. Expense Category Contributions Across Income Bands
SELECT 
    income_band,
    ROUND(AVG(housing_expense), 2) AS avg_housing,
    ROUND(AVG(food_expense), 2) AS avg_food,
    ROUND(AVG(transportation_expense), 2) AS avg_transport,
    ROUND(AVG(healthcare_expense), 2) AS avg_healthcare,
    ROUND(AVG(entertainment_expense), 2) AS avg_entertainment,
    ROUND(AVG(utilities_expense), 2) AS avg_utilities,
    ROUND(AVG(other_expense), 2) AS avg_other
FROM vw_customer_financial_profile
GROUP BY income_band
ORDER BY avg_housing DESC;

-- 3. Customers Spending More Than Income / High Expense Burden (>80%)
SELECT 
    customer_id,
    income_band,
    monthly_income,
    total_monthly_expense,
    expense_to_income_ratio,
    disposable_income
FROM vw_customer_financial_profile
WHERE expense_to_income_ratio >= 0.80
ORDER BY expense_to_income_ratio DESC;
