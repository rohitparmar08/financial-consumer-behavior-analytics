# Executive Business Insights Report

## Financial / Consumer Behavior Analytics

---

## 1. Executive Summary

This report delivers strategic insights synthesized from empirical queries against our 15,000-customer retail banking analytics data warehouse (`database/financial_analytics.db`).

### Key Findings Summary

1. **High Debt Concentration in Mortgages & Secured Loans**
   - **Evidence**: Total liabilities across the portfolio reach **$1.221 Billion** (avg $81,430.60 per customer), exceeding total liquid deposits ($781.39M). The **Debt-Burdened** segment represents 3,042 customers (20.28% of base) with an average debt of $258,504.45.
   - **Business Implication**: Debt is heavily concentrated in real estate and secured loans. Cross-selling debt consolidation or automated mortgage refinancing programs can mitigate interest default risk.

2. **Severe Single-Product Retention Whitespace**
   - **Evidence**: 4,564 customers (30.43% of base) maintain only 1 product (Savings Account), while 6,042 customers (40.28%) hold 2 products. Investment account penetration stands at only 18.23% (2,735 customers).
   - **Business Implication**: A massive cross-sell opportunity exists to convert single-product account holders into multi-product wealth and credit customers.

3. **High Income, High Spend Ratio Segment Risk**
   - **Evidence**: The **High-Income High-Spenders** segment (1,724 customers) boasts an average annual income of $119,989.35 but carries an average expense ratio $\ge 70\%$ and maintains moderate liquid savings ($61,358.92).
   - **Business Implication**: Despite high top-line earnings, these customers have lower savings buffers, making them prime candidates for automated wealth management and premium rewards credit cards.

4. **Concentration of At-Risk and Vulnerable Profiles**
   - **Evidence**: 1,493 customers (9.95%) have a Financial Health Score $< 50$ (High Risk), and 2,606 customers (17.37%) score between 50–69 (Vulnerable).
   - **Business Implication**: Early-intervention financial counseling and flexible payment restructuring can prevent credit score degradation and default losses.

5. **Essential vs Discretionary Transaction Outlay**
   - **Evidence**: Out of $30.31M in total transaction volume, **Transfer** ($8.79M), **Education** ($6.56M), and **Travel** ($5.50M) account for 68.8% of total dollar spend.
   - **Business Implication**: High transaction velocity in tuition and travel indicates key lifecycle spending events suitable for targeted credit lines and travel reward cards.

---

## 2. Customer Portfolio Overview

- **Total Active Customer Base**: 15,000 customers.
- **Demographic Distribution**:
  - Age Range: 18 to 85 years (Average age: 44.2 years).
  - Income Distribution: Mean annual income is **$72,629.52** across the portfolio, with total annual gross earnings of **$1.089 Billion**.
  - City Tiers: Balanced coverage across Tier 1, Tier 2, and Tier 3 metropolitan areas.

---

## 3. Portfolio Financial Health

- **Total Portfolio Wealth & Deposits**:
  - Total Liquid Savings: **$781.39 Million** (Avg $52,092.85 per customer).
  - Total Liabilities & Debt: **$1.221 Billion** (Avg $81,430.60 per customer).
  - Portfolio Average Debt-to-Income (DTI): **17.68%**.
  - Portfolio Average Savings Rate: **16.04%**.
  - Mean FICO Credit Score: **692.2**.
- **Financial Health Score Index (0–100 Index)**:
  - **Portfolio Average Health Score**: **76.09 / 100**.
  - **Healthy Segment ($\ge 70$)**: 10,901 customers (**72.67%**).
  - **Vulnerable Segment ($50–69$)**: 2,606 customers (**17.37%**).
  - **High Risk Segment ($< 50$)**: 1,493 customers (**9.95%**).

---

## 4. Consumer Behavior & Spending Patterns

- **Transaction Volume**: 75,744 total transactions executed across 10 spending categories.
- **Total Portfolio Transaction Outlay**: **$30,307,811.88** (Avg transaction ticket: $400.13).
- **Category Breakdown by Volume & Dollar Amount**:
  1. **Transfer**: 7,576 transactions | **$8,786,582.49** (Avg ticket: $1,159.79)
  2. **Education**: 7,618 transactions | **$6,556,385.27** (Avg ticket: $860.64)
  3. **Travel**: 7,575 transactions | **$5,498,687.76** (Avg ticket: $725.90)
  4. **Healthcare**: 7,632 transactions | **$2,288,919.35** (Avg ticket: $299.91)
  5. **Shopping**: 7,414 transactions | **$1,766,724.04** (Avg ticket: $238.30)
  6. **Utilities**: 7,633 transactions | **$1,448,143.30** (Avg ticket: $189.72)
  7. **Groceries**: 7,557 transactions | **$1,144,897.39** (Avg ticket: $151.50)
  8. **Entertainment**: 7,584 transactions | **$897,310.37** (Avg ticket: $118.32)
  9. **Dining**: 7,627 transactions | **$701,615.18** (Avg ticket: $91.99)
  10. **Subscription**: 7,528 transactions | **$231,648.48** (Avg ticket: $30.77)

---

## 5. Customer Behavioral Segmentation

Analytics classifies the 15,000 customers into 7 distinct business segments:

| Segment Name | Customer Count | Share (%) | Avg Annual Income | Avg Total Debt | Avg Savings Balance |
|---|---|---|---|---|---|
| **Emerging Customers** | 6,173 | 41.15% | $61,191.09 | $14,573.26 | $41,184.80 |
| **Debt-Burdened** | 3,042 | 20.28% | $75,811.31 | $258,504.45 | $55,013.42 |
| **Disciplined Savers** | 1,747 | 11.65% | $47,442.61 | $70,241.67 | $54,185.80 |
| **High-Income High-Spenders** | 1,724 | 11.49% | $119,989.35 | $101,737.59 | $61,358.92 |
| **Financially Strong** | 1,219 | 8.13% | $105,397.22 | $24,321.12 | $97,458.08 |
| **Credit-Risk Customers** | 594 | 3.96% | $53,927.69 | $17,865.91 | $32,990.55 |
| **Low-Engagement Customers** | 501 | 3.34% | $61,549.09 | $13,493.35 | $41,846.27 |

---

## 6. RFM (Recency, Frequency, Monetary) Cohort Analysis

Using quintile `NTILE(5)` scoring across transaction activity, customers are grouped into 8 RFM cohorts:

- **Needs Attention**: 3,154 customers (21.03%) — Moderate spend history with declining transaction recency.
- **Loyal Customers**: 2,999 customers (19.99%) — Highly frequent spenders with stable transaction patterns.
- **Potential Loyalists**: 2,463 customers (16.42%) — Recent shoppers with rising frequency.
- **Champions**: 2,138 customers (14.25%) — Top 15% recency, frequency, and monetary spend.
- **Lost**: 1,910 customers (12.73%) — Inactive for extended periods.
- **New Customers**: 1,661 customers (11.07%) — High recency but low transaction count history.
- **Promising**: 345 customers (2.30%) — Recent buyers with moderate spend.
- **At Risk**: 330 customers (2.20%) — Previously high spenders who haven't transacted recently.

---

## 7. Risk, Credit & Default Analysis

- **Credit Bureau Risk Tier Distribution**:
  - **Medium Risk / Moderate Debt**: 4,626 customers (30.84%).
  - **Low Risk / Low Debt**: 2,689 customers (17.93%).
  - **Medium Risk / High Debt**: 2,477 customers (16.51%).
  - **High Risk / Critical Debt**: 2,029 customers (13.53%).
  - **High Risk / High Debt**: 1,233 customers (8.22%).
  - **Very High Risk / Critical Debt**: 1,129 customers (7.53%).
  - **Medium Risk / Low Debt**: 598 customers (3.99%).
  - **Low Risk / High Debt**: 149 customers (0.99%).
  - **Medium Risk / Critical Debt**: 70 customers (0.47%).

---

## 8. Product Adoption & Whitespace Opportunities

- **Product Penetration Breakdown**:
  - All 15,000 customers hold a primary Savings Account (100% active).
  - Secondary product holding distribution:
    - **Investment Accounts**: 2,735 adopted (1,993 active, 742 closed).
    - **Retirement Accounts**: 2,733 adopted (2,045 active, 688 closed).
    - **Auto Loans**: 2,720 adopted (2,010 active, 710 closed).
    - **Personal Loans**: 2,703 adopted (2,018 active, 685 closed).
    - **Mortgages**: 2,697 adopted (1,995 active, 702 closed).
    - **Credit Cards**: 2,686 adopted (2,034 active, 652 closed).
- **Product Breadth per Customer**:
  - **1 Product**: 4,564 customers (**30.43%**)
  - **2 Products**: 6,042 customers (**40.28%**)
  - **3 Products**: 2,950 customers (**19.67%**)
  - **4 Products**: 1,444 customers (**9.63%**)

---

## 9. Key Business Takeaways

1. **Massive Cross-Sell Opportunity**: Over 70% of the customer base holds 2 or fewer products, representing high potential for targeted credit card, personal loan, and investment conversion campaigns.
2. **Wealth Management Expansion**: 1,219 **Financially Strong** customers hold average savings of $97,458.08 and an income of $105,397.22 but exhibit low investment product penetration.
3. **Targeted Risk Mitigation**: 3,158 customers fall into High/Very High Risk tiers with Critical Debt burdens, requiring preemptive credit line monitoring.
