# Analytics & Segmentation Methodology

This document details the analytical frameworks, KPI definitions, mathematical formulas, classification thresholds, RFM scoring logic, and business opportunity criteria applied across the **Financial / Consumer Behavior Analytics** platform.

---

## 1. Key Performance Indicator (KPI) Definitions

| Metric Name | Mathematical Formula / Calculation | Business Definition & Purpose |
|---|---|---|
| **Disposable Income** | `monthly_income - total_monthly_expense` | Monthly liquid income remaining after essential household expenses. |
| **Expense-to-Income Ratio** | `total_monthly_expense / monthly_income` | Ratio measuring total expense burden against monthly earnings. |
| **Savings Rate** | `monthly_savings / monthly_income` | Percentage of gross monthly earnings directed to savings. |
| **Emergency Reserve Coverage** | `savings_balance / total_monthly_expense` | Estimated number of months of expenses covered by liquid savings balance. |
| **Debt-to-Income (DTI) Ratio** | `est_monthly_debt_service / monthly_income` | Ratio measuring monthly debt obligations relative to monthly income. |
| **Customer Tenure** | `(2025-12-31 - customer_since) / 365.25` | Duration of customer relationship in years as of reference date. |

---

## 2. Savings Behavior Classification Rules

Customers are assigned to 4 savings behavior tiers based on savings rate and emergency fund status:

- **Excellent Saver**: Savings Rate $\ge 20\%$ AND Emergency Fund = `'Fully Funded'` ($\ge 6$ months expenses).
- **Healthy Saver**: Savings Rate $\ge 15\%$.
- **Moderate Saver**: Savings Rate $\ge 5\%$.
- **Low Saver**: Savings Rate $< 5\%$.

---

## 3. Financial Debt Risk Classification Rules

Customers are categorized into 4 financial risk tiers:

- **Critical Risk**: Credit Score $< 580$ OR Missed Payments $\ge 3$ OR Debt-to-Income Ratio $\ge 0.50$.
- **High Risk**: Credit Score $< 670$ OR Missed Payments $\ge 1$ OR Debt-to-Income Ratio $\ge 0.35$.
- **Moderate Risk**: Credit Score $< 740$.
- **Low Risk**: Credit Score $\ge 740$, Missed Payments $= 0$, DTI $< 0.35$.

---

## 4. Customer Business Segmentation Framework (7 Segments)

The primary business segmentation classifies every customer into 1 of 7 mutually exclusive segments:

1. **Financially Strong**: Monthly Income $\ge \$6,000$, Credit Score $\ge 740$, DTI $< 0.35$, Savings Rate $\ge 15\%$.
2. **High-Income High-Spenders**: Monthly Income $\ge \$7,500$, Expense-to-Income Ratio $\ge 70\%$, Savings Rate $< 15\%$.
3. **Disciplined Savers**: Monthly Income $< \$6,000$, Savings Rate $\ge 20\%$, Emergency Fund = `'Fully Funded'`.
4. **Debt-Burdened**: DTI Ratio $\ge 0.45$ OR Total Debt $\ge \$50,000$.
5. **Credit-Risk Customers**: Credit Score $< 580$ OR Missed Payments $\ge 3$ OR Credit Risk Category = `'Very High Risk'`.
6. **Low-Engagement Customers**: Total Transactions $\le 3$ AND Total Products Held $\le 1$.
7. **Emerging Customers**: All remaining customer profiles.

---

## 5. Recency, Frequency, Monetary (RFM) Model

- **Reference Analysis Date**: `2025-12-31` (derived from dataset max timestamp).
- **Recency ($R$)**: Days since last transaction (`2025-12-31 - MAX(transaction_date)`).
- **Frequency ($F$)**: Aggregate transaction count per customer.
- **Monetary ($M$)**: Aggregate dollar sum of transactions per customer.
- **Scoring**: `NTILE(5)` quintile rank ($1$ to $5$ scale).
  - $R$ Score: $5$ = most recent ($0-30$ days), $1$ = least recent.
  - $F$ Score: $5$ = highest frequency, $1$ = lowest frequency.
  - $M$ Score: $5$ = highest monetary spend, $1$ = lowest spend.

### RFM Segment Definitions

| Segment Label | Logic Criteria | Strategic Meaning |
|---|---|---|
| **Champions** | $R \ge 4, F \ge 4, M \ge 4$ | Highest engagement, highest spenders, highly active. |
| **Loyal Customers** | $F \ge 4, M \ge 3$ | Consistent transactors with steady monetary value. |
| **Potential Loyalists** | $R \ge 3, F \ge 3$ | Recent active transactors with growth potential. |
| **New Customers** | $R \ge 4, F \le 2$ | Recently acquired transactors with low transaction history. |
| **Promising** | $R \ge 3, M \ge 3$ | High spenders with moderate transaction frequency. |
| **Needs Attention** | $R = 2, F \ge 2$ | Moderately inactive customers needing re-engagement. |
| **At Risk** | $R \le 2, F \ge 3, M \ge 3$ | Historically high-value transactors at risk of churn. |
| **Lost** | $R = 1, F \le 2$ | Inactive, low-value customers. |

---

## 6. Business Opportunity Rules

1. **Cross-Sell Opportunity**: Transaction count $\ge 5$, tenure $\ge 1.0$ year, but holding $\le 1$ product.
2. **Savings Opportunity**: Monthly income $\ge \$5,000$, but savings rate $< 10\%$.
3. **Credit Growth Opportunity**: Credit score $\ge 720$, DTI $< 0.25$, credit utilization $< 30\%$, no personal loan.
4. **Risk Mitigation Target**: Credit score $< 580$ OR missed payments $\ge 2$ OR DTI $\ge 0.50$.
5. **Premium Wealth Opportunity**: Monthly income $\ge \$8,000$, credit score $\ge 750$, savings rate $\ge 15\%$.

---

## 7. Known Limitations

- **Synthetic Observational Data**: All relationships are synthetic and should not be interpreted as real causal evidence.
- **Fixed Reference Date**: The RFM analysis relies on `2025-12-31` as a fixed reference date to maintain reproducibility across runs.
