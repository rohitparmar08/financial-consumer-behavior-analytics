-- ====================================================================
-- View: RFM Segmentation View
-- Path: sql/views/04_vw_rfm_segments.sql
-- Description: Calculates Recency, Frequency, Monetary (RFM) metrics,
-- assigns NTILE(5) scores (1-5 scale), and maps customers to RFM segments.
-- Reference Analysis Date: 2025-12-31
-- ====================================================================

DROP VIEW IF EXISTS vw_rfm_segments;

CREATE VIEW vw_rfm_segments AS
WITH rfm_raw AS (
    SELECT 
        c.customer_id,
        CAST(JULIANDAY('2025-12-31') - JULIANDAY(MAX(t.transaction_date)) AS INTEGER) AS recency_days,
        COUNT(t.transaction_id) AS frequency,
        ROUND(COALESCE(SUM(t.amount), 0.0), 2) AS monetary_value
    FROM customers c
    LEFT JOIN transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM rfm_raw
)
SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    r_score,
    f_score,
    m_score,
    (r_score * 100 + f_score * 10 + m_score) AS rfm_score_code,
    ROUND((r_score + f_score + m_score) / 3.0, 2) AS rfm_composite_score,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN f_score >= 4 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Potential Loyalists'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score >= 3 AND m_score >= 3 THEN 'Promising'
        WHEN r_score = 2 AND f_score >= 2 THEN 'Needs Attention'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
        WHEN r_score = 1 AND f_score <= 2 THEN 'Lost'
        ELSE 'Needs Attention'
    END AS rfm_segment
FROM rfm_scores;
