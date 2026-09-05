# Power BI Dashboard Visual Specifications

## Executive Overview

This document provides complete layout grids, visual configurations, filtering logic, and interactive specifications for all 6 pages of the **Financial & Consumer Behavior Analytics** Power BI report. Designed following financial industry reporting standards, the layout utilizes standard grid alignment, accessible color palettes (navy/teal corporate theme), clear visual hierarchies, and actionable drill-through pathways.

---

## Page 1: Executive Overview & Financial Health Summary

### 1. Page Purpose & Audience
* **Target Audience**: Executive Leadership, Chief Risk Officer (CRO), VP of Consumer Banking.
* **Business Purpose**: Provide a high-level macroeconomic and portfolio-wide snapshot of customer wealth, income distribution, total deposits, debt exposure, and overall Financial Health Score.

### 2. Header & Top KPI Band (KPI Cards)
* **Card 1: Total Customers**
  * Measure: `[Total Customers]`
  * Format: `#,##0` (e.g., `15,000`)
  * Target / Comparison: YoY Customer Growth (`[Customer Count YoY Change %]`)
* **Card 2: Total Portfolio Net Worth**
  * Measure: `[Total Net Worth]`
  * Format: `$#,##0.0M` (e.g., `$1,450.2M`)
  * Sub-text: Average Net Worth (`[Avg Net Worth]`)
* **Card 3: Total Portfolio Deposits**
  * Measure: `[Total Liquid Assets]`
  * Format: `$#,##0.0M`
  * Sub-text: Avg Savings Rate (`[Avg Savings Rate %]`)
* **Card 4: Total Portfolio Debt**
  * Measure: `[Total Debt]`
  * Format: `$#,##0.0M`
  * Sub-text: Avg Debt-to-Income (`[Avg Debt to Income Ratio %]`)
* **Card 5: Portfolio Financial Health Index**
  * Measure: `[Avg Financial Health Score]`
  * Format: `0.0 / 100` (e.g., `64.2`)
  * Visual Indicator: Color status badge (Green >=70, Yellow 50-69, Red <50)

### 3. Layout Grid & Visual Specifications

```
+-----------------------------------------------------------------------------------+
| [ Header: Executive Overview | Slicers: Date Range, Region, Age Group, Income Tier]|
+-----------------------------------------------------------------------------------+
| [ KPI 1 ]  |  [ KPI 2 ]  |  [ KPI 3 ]  |  [ KPI 4 ]  |  [ KPI 5: Health Score ]    |
+-----------------------------------------------------------------------------------+
| Visual 1: Portfolio Health Distribution    | Visual 2: Net Worth & Income by Tier  |
| (Donut Chart / Treemap)                   | (Clustered Column & Line Chart)       |
+-------------------------------------------------------+---------------------------+
| Visual 3: Monthly Net Cash Flow & Transaction Volume  | Visual 4: Segment Breakdown|
| (Combo Chart - Bar + Line over Time)                  | (Matrix with Heatmap Bar) |
+-----------------------------------------------------------------------------------+
```

#### Visual 1: Financial Health Score Tier Distribution
* **Visual Type**: Donut Chart / Treemap
* **Legend / Details**: `dim_customer[financial_health_category]` (Healthy, Vulnerable, High Risk)
* **Values**: `[Total Customers]`
* **Tooltips**: `[Avg Net Worth]`, `[Avg Debt to Income Ratio %]`, `[Late Payment Rate %]`
* **Color Palette**: Healthy (`#059669` Emerald Green), Vulnerable (`#D97706` Amber), High Risk (`#DC2626` Crimson).

#### Visual 2: Income vs Net Worth by Age Group
* **Visual Type**: Clustered Column and Line Chart
* **Shared Axis**: `dim_customer[age_group]`
* **Column Values**: `[Avg Annual Income]` (Light Navy `#3B82F6`)
* **Line Values**: `[Avg Net Worth]` (Dark Navy `#1E3A8A`)
* **Secondary Line**: `[Avg Debt]` (Crimson `#DC2626`)

#### Visual 3: Cash Flow Trend (Inflow vs Outflow) over Time
* **Visual Type**: Combo Chart (Stacked Column & Line)
* **X-Axis**: `dim_date[YearMonth]` (Sorted chronologically)
* **Column 1**: `[Total Credit Inflow]` (Green `#10B981`)
* **Column 2**: `[Total Debit Outflow]` (Orange `#F59E0B`)
* **Line Axis**: `[Net Portfolio Cash Flow]` (Navy `#1E293B`)

#### Visual 4: Business Segment Summary Matrix
* **Visual Type**: Matrix Visual
* **Rows**: `dim_segment[segment_name]`
* **Values**: `[Total Customers]`, `[Total Net Worth]`, `[Avg Savings Rate %]`, `[Avg Financial Health Score]`, `[Delinquent Rate %]`
* **Formatting**: Conditional color gradients on `[Avg Financial Health Score]` and `[Delinquent Rate %]`.

### 4. Interactive Filters & Page Slicers
* **Global Slicers**: `dim_date[Year]` (Dropdown), `dim_customer[region]` (Tile/Multi-select), `dim_customer[income_tier]` (Dropdown).

---

## Page 2: Consumer Spending & Behavioral Patterns

### 1. Page Purpose & Audience
* **Target Audience**: Head of Retail Payments, Product Managers, Marketing Analytics Team.
* **Business Purpose**: Analyze customer discretionary vs non-discretionary spending, merchant category breakdown, channel preferences (Online vs POS vs ATM), and monthly transaction velocity.

### 2. Header & KPI Band
* **Card 1: Total Spend Volume**: `[Total Spend Volume]` (`$#,##0.0M`)
* **Card 2: Avg Monthly Spend / Cust**: `[Avg Spend Per Customer]` (`$#,##0`)
* **Card 3: Discretionary Spend Ratio**: `[Discretionary Spend Ratio %]` (`0.0%`)
* **Card 4: Digital Channel adoption**: `[Digital Transaction Ratio %]` (`0.0%`)
* **Card 5: Avg Transaction Count**: `[Avg Monthly Transaction Count]` (`0.0`)

### 3. Visual Layout Specifications

#### Visual 1: Merchant Category Breakdown (Waterfall / Bar Chart)
* **Visual Type**: Horizontal Horizontal Clustered Bar Chart
* **Y-Axis**: `dim_product[category]` / Transaction Category
* **X-Axis**: `[Total Spend Volume]`
* **Color Formatting**: Conditional split based on Discretionary (Teal `#0EA5E9`) vs Essential (Slate `#64748B`).

#### Visual 2: Spending Trend by Channel over Time
* **Visual Type**: 100% Stacked Area Chart
* **X-Axis**: `dim_date[YearMonth]`
* **Y-Axis**: `[Total Spend Volume]`
* **Legend**: `fact_transactions[channel]` (Online, POS, ATM, Mobile)

#### Visual 3: Day-of-Week & Hour Spending Heatmap
* **Visual Type**: Matrix Heatmap
* **Rows**: `dim_date[DayOfWeek]`
* **Columns**: Hour of Day (00:00 to 23:00)
* **Values**: `[Total Transaction Count]`
* **Color Scale**: White to Dark Indigo `#312E81`.

#### Visual 4: High-Spender vs Budget-Conscious Profile Comparison
* **Visual Type**: Scatter Plot
* **X-Axis**: `[Avg Monthly Income]`
* **Y-Axis**: `[Avg Monthly Discretionary Spend]`
* **Bubble Size**: `[Total Net Worth]`
* **Legend**: `dim_customer[income_tier]`

---

## Page 3: Financial Health & Balance Sheet Resilience

### 1. Page Purpose & Audience
* **Target Audience**: Financial Wellness Team, Wealth Management Advisors, Retail Risk.
* **Business Purpose**: Deep dive into customer solvency, liquid reserve adequacy (emergency fund coverage months), savings habits, and overall wealth accumulation profiles.

### 2. Header & KPI Band
* **Card 1: Avg Financial Health Score**: `[Avg Financial Health Score]` (`0.0`)
* **Card 2: Healthy Customers Count**: `[Healthy Customers Count]` (`#,##0`)
* **Card 3: Avg Emergency Reserves**: `[Avg Emergency Fund Months]` (`0.0 Months`)
* **Card 4: High DTI Debt Ratio**: `[High DTI Customer %]` (`0.0%`)
* **Card 5: Liquid Reserves Coverage**: `[Avg Savings Rate %]` (`0.0%`)

### 3. Visual Layout Specifications

#### Visual 1: Financial Health Score Breakdown (Box Plot / Distribution Histogram)
* **Visual Type**: Clustered Column Chart (Binned Health Score)
* **X-Axis**: Health Score Bins (0-20, 21-40, 41-60, 61-80, 81-100)
* **Y-Axis**: `[Total Customers]`
* **Legend**: `dim_customer[financial_health_category]`

#### Visual 2: Emergency Reserve Adequacy Matrix
* **Visual Type**: Donut Chart
* **Legend**: `fact_customer_financial[emergency_fund_status]` (Adequate >=6mo, Partial 3-6mo, Low 1-3mo, None <1mo)
* **Values**: `[Total Customers]`
* **Color Palette**: Adequate (`#10B981`), Partial (`#FBBF24`), Low (`#F97316`), None (`#EF4444`).

#### Visual 3: Income vs Debt Burden Matrix
* **Visual Type**: Scatter Chart
* **X-Axis**: `[Debt to Income Ratio %]` (Reference line at 43% DTI threshold)
* **Y-Axis**: `[Savings Rate %]` (Reference line at 20% target savings)
* **Legend**: `dim_customer[income_tier]`

#### Visual 4: Wealth Accumulation Corridor by Segment
* **Visual Type**: Stacked Bar Chart
* **Y-Axis**: `dim_segment[segment_name]`
* **X-Axis**: `[Avg Net Worth]`
* **Breakdown**: `[Avg Liquid Assets]` vs `[Avg Investment Assets]` vs `[Avg Real Estate Assets]`

---

## Page 4: Risk, Credit & Default Analysis

### 1. Page Purpose & Audience
* **Target Audience**: Chief Credit Officer, Credit Risk Managers, Loss Forecasting Analysts.
* **Business Purpose**: Monitor delinquency trends, default probabilities, credit score migration, and high-risk customer concentrations across the loan portfolio.

### 2. Header & KPI Band
* **Card 1: Overall Delinquency Rate**: `[Delinquent Rate %]` (`0.0%`)
* **Card 2: High Risk Customers**: `[High Risk Customer Count]` (`#,##0`)
* **Card 3: Total Portfolio Exposure at Risk**: `[Total Debt At Risk]` (`$#,##0.0M`)
* **Card 4: Avg Credit Score**: `[Avg Credit Score]` (`000`)
* **Card 5: Late Payment Frequency**: `[Avg Late Payment Count]` (`0.0`)

### 3. Visual Layout Specifications

#### Visual 1: Credit Score Tier vs Delinquency Rate Matrix
* **Visual Type**: Column & Line Combo Chart
* **X-Axis**: `dim_customer[credit_tier]` (Poor, Fair, Good, Very Good, Excellent)
* **Columns**: `[Total Customers]`
* **Line**: `[Delinquent Rate %]` (Crimson `#DC2626`)

#### Visual 2: Delinquency Rate by Product & Segment (Heatmap Matrix)
* **Visual Type**: Matrix Table with Color Heatmap
* **Rows**: `dim_segment[segment_name]`
* **Columns**: `dim_product[product_name]`
* **Values**: `[Delinquent Rate %]`
* **Color Formatting**: White to Deep Red based on risk level (>5% highlighted red).

#### Visual 3: High DTI & Low Reserve Risk Matrix (Risk Matrix Scatter Plot)
* **Visual Type**: Scatter Plot
* **X-Axis**: `[Debt to Income Ratio %]`
* **Y-Axis**: `[Late Payment Rate %]`
* **Bubble Size**: `[Total Debt]`
* **Quadrant Reference Lines**: DTI = 43%, Late Payment = 10%

#### Visual 4: Delinquency & Default Vintage Trend over Time
* **Visual Type**: Line Chart
* **X-Axis**: `dim_date[YearMonth]`
* **Y-Axis**: `[Delinquent Rate %]`
* **Legend**: `dim_risk[risk_tier]`

---

## Page 5: Customer Segmentation & RFM Clustering

### 1. Page Purpose & Audience
* **Target Audience**: Customer Lifecycle Lead, CRM Managers, Growth Marketing Strategy.
* **Business Purpose**: Classify customers using RFM (Recency, Frequency, Monetary) scores and value-based behavioral clusters to tailor retention and cross-sell programs.

### 2. Header & KPI Band
* **Card 1: Active Segments Count**: `7 Segments`
* **Card 2: High-Value VIP Customers**: `[VIP Champions Count]` (`#,##0`)
* **Card 3: At-Risk Customer Count**: `[At-Risk Customers Count]` (`#,##0`)
* **Card 4: Average RFM Composite Score**: `[Avg RFM Score]` (`0.0`)
* **Card 5: Portfolio Concentration (Top 20%)**: `[Top 20% Net Worth Contribution %]` (`0.0%`)

### 3. Visual Layout Specifications

#### Visual 1: RFM Segment Size & Net Worth Share (Treemap)
* **Visual Type**: Treemap
* **Group**: `dim_segment[segment_name]`
* **Values**: `[Total Net Worth]`
* **Color Details**: `dim_segment[segment_name]`

#### Visual 2: RFM Segment Characteristics Matrix
* **Visual Type**: Table / Matrix
* **Rows**: `dim_segment[segment_name]`
* **Columns / Values**: `[Total Customers]`, `[Avg Recency Days]`, `[Avg Monthly Tx Frequency]`, `[Avg Spend Per Customer]`, `[Avg Financial Health Score]`

#### Visual 3: Recency vs Frequency Behavioral Cluster
* **Visual Type**: Scatter Chart
* **X-Axis**: `[Avg Days Since Last Transaction]`
* **Y-Axis**: `[Avg Monthly Transaction Count]`
* **Bubble Size**: `[Total Spend Volume]`
* **Color Grouping**: `dim_segment[segment_name]`

#### Visual 4: Customer Migration & Churn Risk Table
* **Visual Type**: Formatted Grid / Table
* **Columns**: Customer ID, Name, Segment, Credit Tier, Net Worth, Financial Health Score, Delinquency Risk.
* **Filter**: Top At-Risk Customers with high spend history.

---

## Page 6: Product Holdings & Cross-Sell Opportunities

### 1. Page Purpose & Audience
* **Target Audience**: Retail Banking Sales Leads, Cross-Sell Relationship Managers.
* **Business Purpose**: Map product penetration rates (Checking, Savings, Credit Card, Personal Loan, Mortgage, Investment, Auto Loan), discover cross-sell gaps, and calculate wallet share.

### 2. Header & KPI Band
* **Card 1: Avg Products per Customer**: `[Avg Products Per Customer]` (`0.0`)
* **Card 2: Single-Product Customers**: `[Single Product Customers]` (`#,##0`)
* **Card 3: Investment Product Penetration**: `[Investment Product Penetration %]` (`0.0%`)
* **Card 4: Total Mortgage Balance**: `[Total Mortgage Balance]` (`$#,##0.0M`)
* **Card 5: Cross-Sell Opportunity Pool**: `[Cross-Sell Target Customer Count]` (`#,##0`)

### 3. Visual Layout Specifications

#### Visual 1: Product Penetration Rates Across Customer Base
* **Visual Type**: Horizontal Bar Chart
* **Y-Axis**: `dim_product[product_name]`
* **X-Axis**: `[Product Penetration Rate %]`
* **Data Labels**: Percentage display (`0.0%`)

#### Visual 2: Product Co-Occurrence & Holding Count Distribution
* **Visual Type**: Clustered Column Chart
* **X-Axis**: Product Holdings Count (1, 2, 3, 4, 5, 6, 7 Products)
* **Y-Axis**: `[Total Customers]`
* **Legend**: `dim_customer[income_tier]`

#### Visual 3: Cross-Sell Opportunity matrix (High Income / Low Product Diversity)
* **Visual Type**: Matrix Table
* **Rows**: `dim_customer[income_tier]`
* **Columns**: `dim_product[product_name]`
* **Values**: `[Cross-Sell Gap Opportunity Count]`

#### Visual 4: Average Balance per Product Type
* **Visual Type**: Treemap / Bar Chart
* **Category**: `dim_product[product_name]`
* **Values**: `[Total Product Balance]`
* **Tooltips**: `[Avg Product Balance per Customer]`, `[Active Product Count]`

---

## Drill-Through & Navigation Architecture

* **Drill-Through Page 1 -> Page 3**: Right-clicking any Segment or Customer Tier navigates directly to Page 3 (Financial Health Detail) filtered for that segment.
* **Drill-Through Page 4 -> Customer Risk Profile**: Right-clicking High-Risk clusters filters for targeted individual customer accounts.
* **Button Navigation**: Top navigation header allows 1-click navigation between Executive, Behavior, Health, Risk, Segments, and Products pages.
