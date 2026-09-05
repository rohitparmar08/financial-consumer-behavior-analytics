-- ====================================================================
-- Analysis 10: Advanced SQL Window Functions
-- Path: sql/analysis/10_window_function_analysis.sql
-- Demonstrates ROW_NUMBER, RANK, DENSE_RANK, NTILE, SUM/AVG OVER(), LAG/LEAD
-- ====================================================================

-- 1. Rank Top Earners Within Each Occupation (ROW_NUMBER, RANK, DENSE_RANK)
WITH ranked_earners AS (
    SELECT 
        customer_id,
        occupation,
        city_tier,
        monthly_income,
        ROW_NUMBER() OVER (PARTITION BY occupation ORDER BY monthly_income DESC) AS row_num,
        RANK() OVER (PARTITION BY occupation ORDER BY monthly_income DESC) AS rank_num,
        DENSE_RANK() OVER (PARTITION BY occupation ORDER BY monthly_income DESC) AS dense_rank_num
    FROM vw_customer_financial_profile
)
SELECT * FROM ranked_earners
WHERE rank_num <= 3
ORDER BY occupation, rank_num;

-- 2. Customer Spend Share & Cumulative Spend (SUM OVER)
WITH customer_spend AS (
    SELECT 
        customer_id,
        customer_segment,
        total_transaction_amount,
        SUM(total_transaction_amount) OVER (PARTITION BY customer_segment) AS segment_total_spend,
        ROUND(total_transaction_amount * 100.0 / SUM(total_transaction_amount) OVER (PARTITION BY customer_segment), 4) AS pct_share_of_segment
    FROM vw_customer_financial_profile
)
SELECT * FROM customer_spend
WHERE pct_share_of_segment > 0.5
ORDER BY customer_segment, total_transaction_amount DESC;

-- 3. Customer Savings Rate vs City Tier Average (AVG OVER)
SELECT 
    customer_id,
    city_tier,
    savings_rate,
    ROUND(AVG(savings_rate) OVER (PARTITION BY city_tier), 4) AS city_tier_avg_savings_rate,
    ROUND(savings_rate - AVG(savings_rate) OVER (PARTITION BY city_tier), 4) AS savings_rate_diff_from_avg
FROM vw_customer_financial_profile
LIMIT 20;

-- 4. Income Deciles (NTILE)
SELECT 
    customer_id,
    monthly_income,
    NTILE(10) OVER (ORDER BY monthly_income DESC) AS income_decile
FROM vw_customer_financial_profile
LIMIT 20;

-- 5. Monthly Transaction Spend Growth Trend (LAG & LEAD)
WITH monthly_trend AS (
    SELECT 
        year_month,
        ROUND(SUM(total_amount), 2) AS monthly_spend
    FROM vw_monthly_transaction_summary
    GROUP BY year_month
)
SELECT 
    year_month,
    monthly_spend,
    LAG(monthly_spend, 1) OVER (ORDER BY year_month) AS prev_month_spend,
    ROUND(monthly_spend - LAG(monthly_spend, 1) OVER (ORDER BY year_month), 2) AS mom_spend_change,
    ROUND((monthly_spend - LAG(monthly_spend, 1) OVER (ORDER BY year_month)) * 100.0 / NULLIF(LAG(monthly_spend, 1) OVER (ORDER BY year_month), 0), 2) AS mom_spend_pct_change
FROM monthly_trend
ORDER BY year_month;
