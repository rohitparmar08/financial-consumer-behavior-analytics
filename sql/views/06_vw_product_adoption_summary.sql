-- ====================================================================
-- View: Financial Product Adoption & Penetration Summary
-- Path: sql/views/06_vw_product_adoption_summary.sql
-- Description: Summarizes product type distribution, active vs churned status,
-- and adoption penetration across income bands.
-- ====================================================================

DROP VIEW IF EXISTS vw_product_adoption_summary;

CREATE VIEW vw_product_adoption_summary AS
SELECT 
    p.product_type,
    p.product_status,
    c.income_band,
    COUNT(p.product_id) AS total_holdings,
    COUNT(DISTINCT p.customer_id) AS unique_customers,
    ROUND(COUNT(p.product_id) * 100.0 / (SELECT COUNT(*) FROM financial_products), 2) AS pct_of_all_products
FROM financial_products p
JOIN vw_customer_financial_profile c ON p.customer_id = c.customer_id
GROUP BY p.product_type, p.product_status, c.income_band;
