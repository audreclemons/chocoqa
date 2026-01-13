# Chocolate Factory QA Post-Add Platform (MVP)

A portfolio project demonstrating an end-to-end data pipeline for manufacturing QA in a fictitious company, **The Chocolate Factory**.  
The system captures batch QA measurements and post-add adjustments, enriches them with product master data (SKU/WPG/specs), stores transactions for traceability, lands raw events in an S3 data lake, enables SQL analytics in Athena, and visualizes KPIs in Power BI.

## MVP (Minimum Viable Product):** This repository represents a functional first release
 that delivers core QA ingestion, validation, and analytics capabilities, with additional
 enhancements planned in future phases.

## Why this project
Manufacturers rely on controlled specifications, traceability, and continuous improvement. This project simulates a real QA workflow and shows modern data engineering + analytics patterns using AWS.

---

## MVP Architecture
**Web Form (S3)** → **API Gateway** → **Lambda (validate/enrich)** →  
**DynamoDB (master + submissions)** + **S3 (raw data lake)** →  
**Athena (SQL)** → **Power BI (dashboards)**

## Architecture Diagram:
![MVP Architecture](docs/architecture.png)

## System Architecture:
![System Architecture](docs/architecture.png)

## Data Flow:
![Data Flow](docs/Data-Flow.png)

## QA Validation Logic:
![QA Logic](docs/QA-Validation-Logic.png)

🔐 **Security Architecture:
![Security Architecture](docs/security-architecture.png)
---
## Key Features (MVP)
- Ingredient master data served via API (dropdown-driven UI)
- QA intake web form hosted on S3
- Serverless ingestion with validation and enrichment
- Transaction storage in DynamoDB for batch traceability
- Live end-to-end flow: form → API → Lambda → DynamoDB
- Foundation for analytics and BI (raw S3 landing in progress)

---

## Delivery Plan (Sprints)

This project is intentionally delivered in sprints to demonstrate incremental, production-style development.

### Sprint 1 — MVP Foundation ✅ (Completed)
- S3 static website hosting for QA web form
- API Gateway with CORS configuration
- DynamoDB MasterData table created and seeded (ingredients)
- Lambda seeder function
- API endpoints:
  - `GET /master/ingredients`
  - `POST /submit`
- Ingredient dropdown populated from live API
- End-to-end submission flow verified (data stored in DynamoDB)

### Sprint 2 — Product Specs & In/Out-of-Spec Logic ✅ (Completed)
- Add Products/SKUs master data (productNo, WPG, spec ranges)
- Endpoints:
  - `GET /master/products`
  - `GET /master/products/{productNo}`
- Update `/submit` Lambda to:
  - fetch product specs
  - compute `specStatus` (OK / WARN / FAIL)
- Update web form to:
  - include product selection
  - display spec ranges read-only
  - enforce spec-driven validation

### Sprint 3 — Analytics Enablement ✅ (Completed)
- Land raw submission events to S3 with partitions (year/month/day/product)
- Create Athena tables (or Glue crawler)
- Enable SQL analytics over QA submissions
- Build Power BI dashboards:
  - FAIL rate by product
  - Submission trends over time
  - Average viscosity vs spec

## Sprint 4 — Governance & AI Enhancements 🟣 (Phase 2 / Planned)

**Goal:**  
Introduce governance, automation, security, and AI-driven insights to support
enterprise-grade quality analytics and decision-making.

**Planned Scope:**
- Workflow orchestration using Apache Airflow for data pipelines
- Data contract validation using Great Expectations or Soda
- Quarantine handling for invalid records
- Curated analytics datasets stored in Parquet format
- Alerting via Amazon SNS for pipeline and quality failures
- Authentication and access control using Amazon Cognito
  - Secure QA submission access
  - Role-based access for analytics and administration
- AI/ML-driven insights, including:
  - Anomaly detection on QA metrics
  - Natural-language explanations (e.g., *“Why did this batch fail?”*) using Amazon Bedrock

**Status:** Planned

---

## Tech Stack
- **Frontend:** HTML / JavaScript (S3 Static Website)
- **API:** Amazon API Gateway
- **Compute:** AWS Lambda (Node.js)
- **Databases:** Amazon DynamoDB (MasterData + Submissions)
- **Data Lake:** Amazon S3
- **Analytics:** Amazon Athena (Glue optional)
- **BI:** Power BI
- **Infrastructure:** AWS SAM (CloudFormation)

---

## Data Model (MVP)

### Master Data (DynamoDB: `ChocoQA-MasterData`)
**Ingredients**
- ingredientId
- ingredientName
- category
- allergens
- defaultUnit
- status

**Products (Sprint 2)**
- productNo
- productName
- productType
- WPG
- specTempMin / specTempMax
- specViscosityMin / specViscosityMax

---

### Transactions (DynamoDB: `ChocoQA-Submissions`)
Each submission stores:
- batchId, line/tank, timestamp
- measured QA values (temperature, viscosity)
- post-add action (ingredient, amount, unit)
- computed quality status (`OK / WARN / FAIL`)
- pointer to raw S3 JSON (`s3RawKey`)

---

## S3 Data Lake Layout 

```text
s3://chocoqa-data/
└── raw/
    └── year=YYYY/
        └── month=MM/
            └── day=DD/
                └── product=<productNo>/
                    └── submission-<id>.json



