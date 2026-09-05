-- ====================================================================
-- Analysis 09: Recency, Frequency, Monetary (RFM) Segmentation
-- Path: sql/analysis/09_rfm_analysis.sql
-- Reference Date: 2025-12-31
-- ====================================================================

-- 1. RFM Segment Distribution & Behavioral Summary
SELECT 
    rfm_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM vw_rfm_segments), 2) AS pct_customers,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary_value), 2) AS avg_monetary_value,
    ROUND(AVG(r_score), 2) AS avg_r_score,
    ROUND(AVG(f_score), 2) AS avg_f_score,
    ROUND(AVG(m_score), 2) AS avg_m_score
FROM vw_rfm_segments
GROUP BY rfm_segment
ORDER BY avg_monetary_value DESC;

-- 2. Top Champions Customers
SELECT 
    r.customer_id,
    p.age,
    p.income_band,
    r.recency_days,
    r.frequency,
    r.monetary_value,
    r.rfm_segment
FROM vw_rfm_segments r
JOIN vw_customer_financial_profile p ON r.customer_id = p.customer_id
WHERE r.rfm_segment = 'Champions'
ORDER BY r.monetary_value DESC
LIMIT 15;

-- 3. At Risk & Lost High-Value Customers
SELECT 
    r.customer_id,
    p.monthly_income,
    r.recency_days,
    r.frequency,
    r.monetary_value,
    r.rfm_segment
FROM vw_rfm_segments r
JOIN vw_customer_financial_profile p ON r.customer_id = p.customer_id
WHERE r.rfm_segment IN ('At Risk', 'Lost') AND r.monetary_value > 500
ORDER BY r.monetary_value DESC;
