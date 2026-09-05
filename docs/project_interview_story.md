# Project Interview Guide & Technical Storytelling

## Financial / Consumer Behavior Analytics

This guide equips you with compelling pitches and technical interview answers for **Data Analyst**, **Data Engineer**, **BI Developer**, and **Analytics Engineer** roles.

---

## 1. Project Pitches

### 30-Second Pitch
> *"I built an end-to-end Financial & Consumer Behavior Analytics platform that processes 15,000 retail banking customer profiles and ~75,000 transactions. It features a Python data pipeline, an SQLite relational data warehouse, advanced SQL analytical models with RFM segmentation, a Power BI Star Schema data model with 50+ DAX measures, and a 21-test automated pytest suite that guarantees 100% data reconciliation."*

### 1-Minute Pitch
> *"In retail banking, decision-makers often struggle to evaluate overall portfolio financial health, default risks, and product cross-sell opportunities due to fragmented data. To address this, I built an end-to-end analytics platform.*
>
> *I used Python to generate and clean a 197,000-record relational dataset across 8 entities. I ingested this into an SQLite database with DDL indexes and 7 analytical views. I then calculated RFM customer clusters using window functions (`NTILE(5)`) and designed a Power BI Star Schema model with 50+ DAX measures—including a composite Financial Health Index (0-100).*
>
> *Finally, I wrote 21 automated pytest unit tests to ensure zero data fan-out or reconciliation errors between SQL and Power BI."*

### 3-Minute Deep Dive
> *"The goal of this project was to construct a production-ready financial analytics system to analyze consumer spending, debt leverage, credit risk, and product penetration across 15,000 retail banking customers.*
>
> *Architecturally, the project follows a medallion-style data flow:*
> 1. **Ingestion & Data Engineering**: Generated 8 correlated relational tables using Python (`Faker`, `NumPy`) and built an automated cleaning engine that imputes missing data and recalculates net savings capacity.
> 2. **Database & SQL Analytics**: Ingested cleaned CSVs into an SQLite data warehouse enforcing strict foreign key constraints. Built 7 analytical SQL views and 12 query modules to categorize customers into 7 business segments and 8 RFM cohorts using SQL window functions (`NTILE(5)`).
> 3. **Power BI Star Schema & DAX**: Designed an export engine creating a 5-dimension, 3-fact Star Schema. Implemented 50+ DAX measures—including time intelligence (YoY spend growth) and a custom 4-pillar Financial Health Index (0-100).
> 4. **Quality & Validation**: Created an automated pytest suite with 21 unit and cross-system reconciliation tests that assert 0 duplicate keys, 0 orphaned records, and exact numeric total matching.
>
> *The resulting analytics identified a $1.22B debt liability pool and highlighted a 30.4% single-product customer base, driving 7 prioritized strategic business recommendations."*

---

## 2. Technical Interview Questions & Answers

### Q1: What was the hardest technical problem you encountered, and how did you solve it?
**Answer**:
> *"The hardest challenge was preventing join multiplication and double-counting when connecting customer-level financial net worth ($1.09B income, $1.22B debt) with transaction-level spend logs (~75k rows).*
>
> *Directly joining transactions to customer financial profiles creates a 5.05x fan-out multiplication. I solved this by designing a pure Star Schema in Power BI where `dim_customer` links 1-to-1 with `fact_customer_financial` (15,000 rows) and 1-to-Many with `fact_transactions` (75,744 rows). In DAX, measures reference the specific fact table appropriate for their grain."*

### Q2: Why did you choose SQLite for your data warehouse?
**Answer**:
> *"SQLite is lightweight, serverless, self-contained, and supports full ANSI SQL features including Common Table Expressions (CTEs), window functions (`NTILE`, `RANK`, `LEAD/LAG`), and foreign key enforcement (`PRAGMA foreign_keys = ON;`). It allowed me to deliver a 100% reproducible database project without requiring complex database server setups."*

### Q3: Why a Star Schema instead of a single flat table for Power BI?
**Answer**:
> *"A single flat table introduces massive data redundancy, bloats memory storage, and degrades VertiPaq engine compression. A Star Schema separates master dimensions (`dim_customer`, `dim_date`, `dim_product`) from event facts (`fact_transactions`, `fact_customer_financial`), allowing efficient 1-to-Many filter propagation, fast DAX aggregation, and clean visuals."*

### Q4: How did you validate your data pipeline?
**Answer**:
> *"I built a two-layer validation framework: a custom assertion validator (`src/validation/validator.py`) integrated into the main CLI pipeline, and an automated `pytest` test suite with 21 unit/reconciliation tests. The test suite verifies primary key uniqueness, foreign key referential integrity, range bounds, and reconciles numeric sums (income, debt, transaction spend) between SQLite and Power BI export CSVs."*

### Q5: How did you implement RFM Customer Segmentation?
**Answer**:
> *"I calculated Recency (days since last transaction relative to reference date `2025-12-31`), Frequency (monthly transaction count), and Monetary value (total spend amount) per customer in SQL. Using `NTILE(5) OVER ()`, I assigned quintile scores (1 to 5) for R, F, and M. I then mapped composite RFM codes into 8 business segments (Champions, Loyal Customers, Potential Loyalists, At Risk, Lost, etc.)."*

### Q6: What would you change if deploying this with real production data at scale?
**Answer**:
> 1. **Infrastructure**: Migrate SQLite to PostgreSQL or Snowflake / BigQuery for distributed SQL analytical processing.
> 2. **Orchestration**: Replace the custom CLI runner with Apache Airflow or Dagster for automated DAG scheduling and alert monitoring.
> 3. **Transformation Layer**: Adopt dbt (data build tool) for SQL transformations, lineage visualization, and automated documentation generation.
> 4. **Data Security**: Implement column-level PII hashing and role-based access control (RBAC).
