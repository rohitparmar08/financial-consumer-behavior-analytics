"""
Synthetic Data Generation Engine for Financial Consumer Behavior Analytics.
Generates correlated synthetic financial entities across 8 relational tables.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from datetime import datetime, timedelta
import random

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("data_generation")


class SyntheticDataGenerator:
    """
    Generates reproducible synthetic financial and consumer behavior data.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.seed = self.config.random_seed
        self.num_customers = self.config.num_customers
        self._set_seed()

    def _set_seed(self):
        np.random.seed(self.seed)
        random.seed(self.seed)

    def generate_customers(self) -> pd.DataFrame:
        """Generates the CUSTOMERS entity table."""
        logger.info(f"Generating {self.num_customers} customer demographic records...")

        customer_ids = [f"CUST-{i+1:05d}" for i in range(self.num_customers)]
        ages = np.random.randint(18, 76, size=self.num_customers)
        genders = np.random.choice(["Male", "Female", "Non-Binary"], size=self.num_customers, p=[0.48, 0.48, 0.04])
        
        education_levels = ["High School", "Associate", "Bachelor's", "Master's", "Doctorate"]
        education_probs = [0.25, 0.15, 0.40, 0.15, 0.05]
        educations = np.random.choice(education_levels, size=self.num_customers, p=education_probs)

        # Employment status logic based on age
        employment_statuses = []
        occupations = []
        for i in range(self.num_customers):
            age = ages[i]
            if age < 22 and np.random.rand() < 0.6:
                emp = "Student"
                occ = "Student"
            elif age >= 65 and np.random.rand() < 0.7:
                emp = "Retired"
                occ = "Retired"
            else:
                emp = np.random.choice(["Employed", "Self-Employed", "Unemployed"], p=[0.80, 0.15, 0.05])
                if emp == "Unemployed":
                    occ = "Unemployed"
                else:
                    occ = np.random.choice([
                        "Software/Tech", "Healthcare", "Finance/Banking", "Education",
                        "Retail/Hospitality", "Trades/Manufacturing", "Management/Executive", "Other"
                    ], p=[0.20, 0.18, 0.15, 0.12, 0.12, 0.10, 0.08, 0.05])
            employment_statuses.append(emp)
            occupations.append(occ)

        marital_statuses = np.random.choice(
            ["Single", "Married", "Divorced", "Widowed"],
            size=self.num_customers,
            p=[0.38, 0.47, 0.11, 0.04]
        )
        city_tiers = np.random.choice(["Tier 1", "Tier 2", "Tier 3"], size=self.num_customers, p=[0.35, 0.45, 0.20])

        # Customer since dates between 2018-01-01 and 2024-12-31
        start_date = datetime(2018, 1, 1)
        end_date = datetime(2024, 12, 31)
        days_range = (end_date - start_date).days
        customer_since_list = [
            (start_date + timedelta(days=int(np.random.randint(0, days_range)))).strftime("%Y-%m-%d")
            for _ in range(self.num_customers)
        ]

        df = pd.DataFrame({
            "customer_id": customer_ids,
            "age": ages,
            "gender": genders,
            "education": educations,
            "employment_status": employment_statuses,
            "marital_status": marital_statuses,
            "city_tier": city_tiers,
            "occupation": occupations,
            "customer_since": customer_since_list
        })
        return df

    def generate_income(self, df_customers: pd.DataFrame) -> pd.DataFrame:
        """Generates the INCOME entity table correlated with demographics."""
        logger.info("Generating correlated INCOME records...")
        
        income_ids = [f"INC-{i+1:05d}" for i in range(self.num_customers)]
        customer_ids = df_customers["customer_id"].values
        educations = df_customers["education"].values
        occupations = df_customers["occupation"].values
        employment_statuses = df_customers["employment_status"].values
        ages = df_customers["age"].values

        monthly_incomes = []
        income_sources = []
        income_stabilities = []

        for i in range(self.num_customers):
            edu = educations[i]
            occ = occupations[i]
            emp = employment_statuses[i]
            age = ages[i]

            # Base income multipliers
            base_income = 2500.0
            if edu == "High School":
                base_income *= 1.0
            elif edu == "Associate":
                base_income *= 1.2
            elif edu == "Bachelor's":
                base_income *= 1.6
            elif edu == "Master's":
                base_income *= 2.1
            elif edu == "Doctorate":
                base_income *= 2.6

            # Occupation boost
            if occ in ["Software/Tech", "Finance/Banking", "Management/Executive"]:
                base_income *= 1.4
            elif occ in ["Healthcare", "Trades/Manufacturing"]:
                base_income *= 1.15
            elif occ in ["Student", "Unemployed"]:
                base_income *= 0.3

            # Age experience factor
            exp_factor = 1.0 + min((age - 18) * 0.015, 0.6)
            base_income *= exp_factor

            # Random variance
            noise = np.random.lognormal(mean=0, sigma=0.25)
            final_monthly = float(np.round(max(500.0, base_income * noise), 2))
            monthly_incomes.append(final_monthly)

            # Income source
            if emp == "Employed":
                src = "Salary"
                stab = np.random.choice(["High", "Medium"], p=[0.75, 0.25])
            elif emp == "Self-Employed":
                src = np.random.choice(["Business", "Freelance"], p=[0.6, 0.4])
                stab = np.random.choice(["Medium", "Low"], p=[0.6, 0.4])
            elif emp == "Retired":
                src = np.random.choice(["Pension/Government", "Investment"], p=[0.7, 0.3])
                stab = "High"
            elif emp == "Student":
                src = np.random.choice(["Government Support", "Freelance", "Family"], p=[0.4, 0.3, 0.3])
                stab = "Low"
            else:  # Unemployed
                src = "Government Support"
                stab = "Low"

            income_sources.append(src)
            income_stabilities.append(stab)

        df = pd.DataFrame({
            "income_id": income_ids,
            "customer_id": customer_ids,
            "monthly_income": monthly_incomes,
            "annual_income": np.round(np.array(monthly_incomes) * 12, 2),
            "income_source": income_sources,
            "income_stability": income_stabilities
        })
        return df

    def generate_expenses(self, df_customers: pd.DataFrame, df_income: pd.DataFrame) -> pd.DataFrame:
        """Generates the EXPENSES entity table based on income & city tier."""
        logger.info("Generating correlated EXPENSES records...")

        expense_ids = [f"EXP-{i+1:05d}" for i in range(self.num_customers)]
        customer_ids = df_customers["customer_id"].values
        city_tiers = df_customers["city_tier"].values
        monthly_incomes = df_income["monthly_income"].values

        housing_expenses = []
        food_expenses = []
        transport_expenses = []
        healthcare_expenses = []
        entertainment_expenses = []
        utilities_expenses = []
        other_expenses = []
        total_monthly_expenses = []

        for i in range(self.num_customers):
            inc = monthly_incomes[i]
            ct = city_tiers[i]

            # Housing ratio (higher in Tier 1 cities)
            housing_ratio = 0.35 if ct == "Tier 1" else (0.28 if ct == "Tier 2" else 0.22)
            housing = max(150.0, inc * housing_ratio * np.random.uniform(0.85, 1.15))

            # Food, Utilities, Transport
            food = max(100.0, inc * 0.15 * np.random.uniform(0.8, 1.2))
            transport = max(50.0, inc * 0.08 * np.random.uniform(0.7, 1.3))
            utilities = max(40.0, inc * 0.06 * np.random.uniform(0.8, 1.2))
            healthcare = max(30.0, inc * 0.05 * np.random.uniform(0.6, 1.4))
            entertainment = max(20.0, inc * 0.07 * np.random.uniform(0.5, 1.5))
            other = max(20.0, inc * 0.04 * np.random.uniform(0.5, 1.5))

            tot = housing + food + transport + healthcare + entertainment + utilities + other

            # Cap expense so high earners don't automatically spend 100%
            if tot > inc * 0.95 and inc > 2000:
                tot = inc * np.random.uniform(0.65, 0.85)
                ratio = tot / (housing + food + transport + healthcare + entertainment + utilities + other)
                housing *= ratio
                food *= ratio
                transport *= ratio
                healthcare *= ratio
                entertainment *= ratio
                utilities *= ratio
                other *= ratio

            housing_expenses.append(round(housing, 2))
            food_expenses.append(round(food, 2))
            transport_expenses.append(round(transport, 2))
            healthcare_expenses.append(round(healthcare, 2))
            entertainment_expenses.append(round(entertainment, 2))
            utilities_expenses.append(round(utilities, 2))
            other_expenses.append(round(other, 2))
            total_monthly_expenses.append(round(tot, 2))

        df = pd.DataFrame({
            "expense_id": expense_ids,
            "customer_id": customer_ids,
            "housing_expense": housing_expenses,
            "food_expense": food_expenses,
            "transportation_expense": transport_expenses,
            "healthcare_expense": healthcare_expenses,
            "entertainment_expense": entertainment_expenses,
            "utilities_expense": utilities_expenses,
            "other_expense": other_expenses,
            "total_monthly_expense": total_monthly_expenses
        })
        return df

    def generate_savings(self, df_customers: pd.DataFrame, df_income: pd.DataFrame, df_expenses: pd.DataFrame) -> pd.DataFrame:
        """Generates SAVINGS entity table."""
        logger.info("Generating correlated SAVINGS records...")

        savings_ids = [f"SAV-{i+1:05d}" for i in range(self.num_customers)]
        customer_ids = df_customers["customer_id"].values
        since_dates = pd.to_datetime(df_customers["customer_since"]).values
        ref_date = pd.to_datetime("2025-12-31")

        monthly_incomes = df_income["monthly_income"].values
        total_expenses = df_expenses["total_monthly_expense"].values

        monthly_savings_list = []
        savings_balances = []
        savings_rates = []
        emergency_statuses = []

        for i in range(self.num_customers):
            inc = monthly_incomes[i]
            exp = total_expenses[i]

            disposable = inc - exp
            if disposable > 0:
                sav = disposable * np.random.uniform(0.4, 0.85)
            else:
                sav = max(0.0, inc * np.random.uniform(0.0, 0.05))

            sav_rate = round(sav / inc if inc > 0 else 0.0, 4)

            # Months active
            days_active = float((ref_date - since_dates[i]) / np.timedelta64(1, 'D'))
            tenure_months = max(1, int(days_active / 30.4375))
            balance = sav * tenure_months * np.random.uniform(0.7, 1.3) + np.random.exponential(500)
            balance = round(max(0.0, balance), 2)

            # Emergency fund status
            months_covered = balance / exp if exp > 0 else 0
            if months_covered >= 6:
                status = "Fully Funded"
            elif months_covered >= 3:
                status = "Partially Funded"
            elif months_covered >= 1:
                status = "Low"
            else:
                status = "No Fund"

            monthly_savings_list.append(round(sav, 2))
            savings_balances.append(balance)
            savings_rates.append(sav_rate)
            emergency_statuses.append(status)

        df = pd.DataFrame({
            "savings_id": savings_ids,
            "customer_id": customer_ids,
            "monthly_savings": monthly_savings_list,
            "savings_balance": savings_balances,
            "savings_rate": savings_rates,
            "emergency_fund_status": emergency_statuses
        })
        return df

    def generate_debt(self, df_customers: pd.DataFrame, df_income: pd.DataFrame) -> pd.DataFrame:
        """Generates DEBT entity table."""
        logger.info("Generating correlated DEBT records...")

        debt_ids = [f"DEBT-{i+1:05d}" for i in range(self.num_customers)]
        customer_ids = df_customers["customer_id"].values
        ages = df_customers["age"].values
        educations = df_customers["education"].values
        annual_incomes = df_income["annual_income"].values
        monthly_incomes = df_income["monthly_income"].values

        cc_debts = []
        personal_loans = []
        education_loans = []
        vehicle_loans = []
        mortgages = []
        total_debts = []
        dti_ratios = []

        for i in range(self.num_customers):
            age = ages[i]
            edu = educations[i]
            annual_inc = annual_incomes[i]
            monthly_inc = monthly_incomes[i]

            # Credit Card Debt (70% of customers have CC debt)
            has_cc = np.random.rand() < 0.70
            cc = round(np.random.uniform(200, 8000) * (annual_inc / 50000.0) if has_cc else 0.0, 2)

            # Personal Loan (25% probability)
            has_pl = np.random.rand() < 0.25
            pl = round(np.random.uniform(1000, 25000) if has_pl else 0.0, 2)

            # Education Loan (higher for younger & higher educated)
            has_el = (age < 40 and edu in ["Bachelor's", "Master's", "Doctorate"]) and (np.random.rand() < 0.45)
            el = round(np.random.uniform(5000, 45000) if has_el else 0.0, 2)

            # Vehicle Loan (35% probability)
            has_vl = np.random.rand() < 0.35
            vl = round(np.random.uniform(4000, 35000) if has_vl else 0.0, 2)

            # Mortgage (40% of customers age 28-65 with income > $35k)
            has_mg = (28 <= age <= 65 and annual_inc > 35000) and (np.random.rand() < 0.40)
            mg = round(np.random.uniform(80000, 450000) if has_mg else 0.0, 2)

            tot_debt = round(cc + pl + el + vl + mg, 2)
            
            # Debt-to-Income ratio: (estimated monthly debt payment) / monthly income
            # Estimated monthly debt payment approx 1% of total debt
            est_monthly_debt_payment = tot_debt * 0.012
            dti = round(min(2.5, est_monthly_debt_payment / monthly_inc) if monthly_inc > 0 else 0.0, 4)

            cc_debts.append(cc)
            personal_loans.append(pl)
            education_loans.append(el)
            vehicle_loans.append(vl)
            mortgages.append(mg)
            total_debts.append(tot_debt)
            dti_ratios.append(dti)

        df = pd.DataFrame({
            "debt_id": debt_ids,
            "customer_id": customer_ids,
            "credit_card_debt": cc_debts,
            "personal_loan": personal_loans,
            "education_loan": education_loans,
            "vehicle_loan": vehicle_loans,
            "mortgage": mortgages,
            "total_debt": total_debts,
            "debt_to_income_ratio": dti_ratios
        })
        return df

    def generate_credit(self, df_customers: pd.DataFrame, df_savings: pd.DataFrame, df_debt: pd.DataFrame) -> pd.DataFrame:
        """Generates CREDIT entity table correlated with financial health."""
        logger.info("Generating correlated CREDIT records...")

        credit_ids = [f"CRED-{i+1:05d}" for i in range(self.num_customers)]
        customer_ids = df_customers["customer_id"].values
        savings_rates = df_savings["savings_rate"].values
        dti_ratios = df_debt["debt_to_income_ratio"].values

        credit_scores = []
        payment_behaviors = []
        missed_payments_list = []
        credit_utilizations = []
        risk_categories = []

        for i in range(self.num_customers):
            sr = savings_rates[i]
            dti = dti_ratios[i]

            # Base score 680
            base_score = 680.0
            # Higher savings rate increases score
            base_score += sr * 300
            # Higher DTI decreases score
            base_score -= dti * 200
            # Noise
            score = int(np.clip(base_score + np.random.normal(0, 40), 300, 850))

            if score >= 750:
                behavior = "On-Time"
                missed = int(np.random.choice([0, 1], p=[0.95, 0.05]))
                util = round(np.random.uniform(0.05, 0.25), 2)
                risk = "Low Risk"
            elif score >= 670:
                behavior = np.random.choice(["On-Time", "Occasional Late"], p=[0.7, 0.3])
                missed = int(np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1]))
                util = round(np.random.uniform(0.20, 0.50), 2)
                risk = "Medium Risk"
            elif score >= 580:
                behavior = np.random.choice(["Occasional Late", "Frequently Late"], p=[0.5, 0.5])
                missed = int(np.random.randint(1, 5))
                util = round(np.random.uniform(0.45, 0.85), 2)
                risk = "High Risk"
            else:
                behavior = np.random.choice(["Frequently Late", "Default Risk"], p=[0.4, 0.6])
                missed = int(np.random.randint(4, 12))
                util = round(np.random.uniform(0.70, 0.99), 2)
                risk = "Very High Risk"

            credit_scores.append(score)
            payment_behaviors.append(behavior)
            missed_payments_list.append(missed)
            credit_utilizations.append(util)
            risk_categories.append(risk)

        df = pd.DataFrame({
            "credit_id": credit_ids,
            "customer_id": customer_ids,
            "credit_score": credit_scores,
            "payment_behavior": payment_behaviors,
            "missed_payments": missed_payments_list,
            "credit_utilization": credit_utilizations,
            "credit_risk_category": risk_categories
        })
        return df

    def generate_transactions(self, df_customers: pd.DataFrame, df_income: pd.DataFrame) -> pd.DataFrame:
        """Generates granular TRANSACTIONS log table."""
        logger.info("Generating granular TRANSACTIONS records...")

        avg_txns = self.config.avg_transactions_per_customer
        customer_ids = df_customers["customer_id"].values
        since_dates = df_customers["customer_since"].values
        monthly_incomes = df_income["monthly_income"].values

        txns_list = []
        txn_counter = 1

        categories = [
            "Groceries", "Dining", "Shopping", "Utilities", "Travel",
            "Healthcare", "Entertainment", "Education", "Subscription", "Transfer"
        ]
        payment_methods = ["Credit Card", "Debit Card", "Bank Transfer", "Digital Wallet", "Cash"]
        merchant_types = [
            "Supermarket", "Online Retail", "Restaurant", "Service Provider",
            "Electronics", "Gas Station", "Apparel", "Healthcare"
        ]

        for i in range(self.num_customers):
            c_id = customer_ids[i]
            since = datetime.strptime(since_dates[i], "%Y-%m-%d")
            income = monthly_incomes[i]

            # Generate 3 to 8 transactions per customer
            num_txns = int(np.random.poisson(avg_txns))
            num_txns = max(2, min(12, num_txns))

            for _ in range(num_txns):
                t_id = f"TXN-{txn_counter:07d}"
                txn_counter += 1

                # Date between customer_since and 2025-12-31
                max_days = (datetime(2025, 12, 31) - since).days
                if max_days <= 1:
                    days_offset = 0
                else:
                    days_offset = int(np.random.randint(0, max_days))
                txn_date = (since + timedelta(days=days_offset)).strftime("%Y-%m-%d %H:%M:%S")

                cat = np.random.choice(categories)
                t_type = "Credit" if cat == "Transfer" and np.random.rand() < 0.3 else "Debit"

                # Transaction amount scaling
                if cat == "Groceries":
                    amt = np.random.uniform(20, 250)
                elif cat == "Dining":
                    amt = np.random.uniform(15, 150)
                elif cat == "Shopping":
                    amt = np.random.uniform(25, 400)
                elif cat == "Utilities":
                    amt = np.random.uniform(40, 300)
                elif cat == "Travel":
                    amt = np.random.uniform(100, 1200)
                elif cat == "Healthcare":
                    amt = np.random.uniform(30, 500)
                elif cat == "Entertainment":
                    amt = np.random.uniform(10, 200)
                elif cat == "Education":
                    amt = np.random.uniform(50, 1500)
                elif cat == "Subscription":
                    amt = np.random.uniform(5, 50)
                else:  # Transfer
                    amt = np.random.uniform(50, 2000)

                # Scale slightly with income
                amt = amt * (1.0 + (income / 10000.0) * 0.2)
                amt = round(max(1.0, amt), 2)

                method = np.random.choice(payment_methods)
                merchant = np.random.choice(merchant_types)

                txns_list.append({
                    "transaction_id": t_id,
                    "customer_id": c_id,
                    "transaction_date": txn_date,
                    "transaction_type": t_type,
                    "category": cat,
                    "amount": amt,
                    "payment_method": method,
                    "merchant_type": merchant
                })

        df = pd.DataFrame(txns_list)

        # Inject minor duplicates for cleaning validation testing (e.g. 50 duplicate rows)
        if len(df) > 100:
            dup_indices = np.random.choice(df.index, size=50, replace=False)
            duplicates = df.loc[dup_indices].copy()
            df = pd.concat([df, duplicates], ignore_index=True)

        return df

    def generate_financial_products(self, df_customers: pd.DataFrame, df_income: pd.DataFrame) -> pd.DataFrame:
        """Generates FINANCIAL_PRODUCTS entity table."""
        logger.info("Generating FINANCIAL_PRODUCTS adoption records...")

        customer_ids = df_customers["customer_id"].values
        since_dates = df_customers["customer_since"].values

        products_list = []
        prod_counter = 1

        product_types = [
            "Savings Account", "Credit Card", "Personal Loan",
            "Mortgage", "Investment Account", "Auto Loan", "Retirement Account"
        ]

        for i in range(self.num_customers):
            c_id = customer_ids[i]
            since = datetime.strptime(since_dates[i], "%Y-%m-%d")

            # Every customer has at least a Savings Account
            p_id = f"PROD-{prod_counter:05d}"
            prod_counter += 1
            products_list.append({
                "product_id": p_id,
                "customer_id": c_id,
                "product_type": "Savings Account",
                "product_status": "Active",
                "signup_date": since.strftime("%Y-%m-%d")
            })

            # Additional products based on random adoption
            extra_count = int(np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1]))
            chosen_types = np.random.choice(product_types[1:], size=extra_count, replace=False)

            for p_type in chosen_types:
                p_id = f"PROD-{prod_counter:05d}"
                prod_counter += 1

                days_offset = int(np.random.randint(0, max(1, (datetime(2025, 12, 31) - since).days)))
                signup = (since + timedelta(days=days_offset)).strftime("%Y-%m-%d")
                status = np.random.choice(["Active", "Closed", "Pending", "Churned"], p=[0.75, 0.15, 0.05, 0.05])

                products_list.append({
                    "product_id": p_id,
                    "customer_id": c_id,
                    "product_type": p_type,
                    "product_status": status,
                    "signup_date": signup
                })

        df = pd.DataFrame(products_list)
        return df

    def inject_controlled_noise(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Injects controlled missing values and casing inconsistencies into raw data
        so that the data cleaning pipeline has realistic imperfections to process.
        """
        logger.info("Injecting controlled noise/imperfections into raw dataset...")

        rate = self.config.missing_value_rate

        # Customers: casing whitespace issues
        df_cust = data_dict["customers"].copy()
        mask_emp = np.random.rand(len(df_cust)) < 0.03
        df_cust.loc[mask_emp, "employment_status"] = df_cust.loc[mask_emp, "employment_status"].str.upper() + "  "

        # Income: missing income_stability
        df_inc = data_dict["income"].copy()
        mask_inc = np.random.rand(len(df_inc)) < rate
        df_inc.loc[mask_inc, "income_stability"] = None

        # Transactions: missing merchant_type
        df_txn = data_dict["transactions"].copy()
        mask_txn = np.random.rand(len(df_txn)) < rate
        df_txn.loc[mask_txn, "merchant_type"] = None

        data_dict["customers"] = df_cust
        data_dict["income"] = df_inc
        data_dict["transactions"] = df_txn

        return data_dict

    def generate_all(self, output_dir: Path = None) -> Dict[str, pd.DataFrame]:
        """
        Executes full generation process and saves raw CSV files.
        """
        output_dir = output_dir or self.config.raw_data_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting synthetic dataset generation (Seed: {self.seed})...")

        df_cust = self.generate_customers()
        df_inc = self.generate_income(df_cust)
        df_exp = self.generate_expenses(df_cust, df_inc)
        df_sav = self.generate_savings(df_cust, df_inc, df_exp)
        df_debt = self.generate_debt(df_cust, df_inc)
        df_cred = self.generate_credit(df_cust, df_sav, df_debt)
        df_txn = self.generate_transactions(df_cust, df_inc)
        df_prod = self.generate_financial_products(df_cust, df_inc)

        data_dict = {
            "customers": df_cust,
            "income": df_inc,
            "expenses": df_exp,
            "savings": df_sav,
            "debt": df_debt,
            "credit": df_cred,
            "transactions": df_txn,
            "financial_products": df_prod
        }

        # Inject controlled noise for cleaning pipeline testing
        data_dict = self.inject_controlled_noise(data_dict)

        logger.info(f"Saving raw datasets to {output_dir}...")
        for name, df in data_dict.items():
            filepath = output_dir / f"{name}.csv"
            df.to_csv(filepath, index=False)
            logger.info(f"Wrote raw {name}.csv with {len(df)} rows.")

        return data_dict


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    generator.generate_all()
