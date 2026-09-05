# Power BI Implementation Package

This directory contains the semantic model assets, DAX measure definitions, theme configurations, and step-by-step instructions for authoring the **Financial / Consumer Behavior Analytics** Power BI report.

---

## 1. Package Contents

- **`dax_measures.md`**: Complete DAX measure library (50+ measures for KPIs, Segmentation, RFM, Time Intelligence, and Financial Health Score).
- **`theme.json`**: Corporate report theme defining color palette, font styles, and visual card formatting.
- **`README.md`**: Power BI import and build instructions.

---

## 2. Power BI Datasets (Source CSV Location)

All clean star-schema datasets are generated under `data/exports/powerbi/`:

1. `dim_customer.csv` (15,000 rows, Customer Dimension)
2. `dim_date.csv` (2,922 rows, Calendar Date Dimension)
3. `dim_product.csv` (7 rows, Product Dimension)
4. `dim_segment.csv` (7 rows, Business Segment Dimension)
5. `dim_risk.csv` (9 rows, Risk Dimension)
6. `fact_transactions.csv` (75,744 rows, Transaction Fact)
7. `fact_customer_financial.csv` (15,000 rows, Customer Financial Snapshot Fact)
8. `fact_product_holdings.csv` (31,274 rows, Product Holdings Fact)

---

## 3. Step-by-Step Power BI Desktop Import Guide

### Step 1: Import CSV Datasets
1. Open **Power BI Desktop**.
2. Click **Get Data -> Text/CSV**.
3. Import all 8 CSV files from `data/exports/powerbi/`.
4. Set encoding to **UTF-8** and delimiter to **Comma**.

### Step 2: Configure Date Table
1. Select `dim_date` table in Model View.
2. Right-click `dim_date` -> **Mark as Date Table**.
3. Select `date` column as the Date column.

### Step 3: Establish Relationships & Cardinality
Create the following 1-to-Many, Single Direction relationships in Model View:

- `dim_customer[customer_id]` (1) ── (1) `fact_customer_financial[customer_id]`
- `dim_customer[customer_id]` (1) ── (M) `fact_transactions[customer_id]`
- `dim_customer[customer_id]` (1) ── (M) `fact_product_holdings[customer_id]`
- `dim_date[date]` (1) ── (M) `fact_transactions[transaction_date_key]`
- `dim_date[date]` (1) ── (M) `fact_product_holdings[signup_date_key]`
- `dim_product[product_type]` (1) ── (M) `fact_product_holdings[product_type]`
- `dim_segment[customer_segment]` (1) ── (M) `fact_customer_financial[customer_segment]`
- `dim_risk[risk_key]` (1) ── (M) `fact_customer_financial[risk_key]`

### Step 4: Apply Theme
1. Navigate to **View -> Themes -> Browse for Themes**.
2. Select `powerbi/theme.json`.

### Step 5: Add DAX Measures
1. Click **New Measure** in Modeling Tab.
2. Copy and paste measures from `powerbi/dax_measures.md`.
