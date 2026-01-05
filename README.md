# Chocolate Factory QA Post-Add Platform (MVP)

A portfolio project demonstrating an end-to-end data pipeline for manufacturing QA in a fictitious company, **The Chocolate Factory**.  
The system captures batch QA measurements and post-add adjustments, enriches them with product master data (SKU/WPG/specs), stores transactions for traceability, lands raw events in an S3 data lake, enables SQL analytics in Athena, and visualizes KPIs in Power BI.

## Why this project
Manufacturers rely on controlled specifications, traceability, and continuous improvement. This project simulates a real QA workflow and shows modern data engineering + analytics patterns using AWS.

---

## MVP Architecture
**Web Form (S3)** → **API Gateway** → **Lambda (validate/enrich)** →  
**DynamoDB (master + submissions)** + **S3 (raw data lake)** →  
**Athena (SQL)** → **Power BI (dashboards)**

> Diagram: see `/docs/architecture.png`

---

## Key Features (MVP)
- Product master data (fictitious SKU, WPG, spec ranges) served via API
- QA intake web form populated from master data
- Serverless ingestion with validation + enrichment
- Transaction storage in DynamoDB for batch traceability
- Raw event landing zone in S3 with partitioned folder structure
- Athena SQL queries for KPI calculations
- Power BI dashboard for quality insights (FAIL rate, trends, averages)

---

## Tech Stack
- Frontend: HTML/JS static form hosted on S3
- Auth (optional in MVP): Amazon Cognito
- API: Amazon API Gateway
- Compute: AWS Lambda (Node.js)
- Storage: DynamoDB (MasterData + Submissions), S3 (raw data lake)
- Analytics: Athena (+ optional Glue Data Catalog)
- BI: Power BI

---

## Data Model (MVP)

### Master Data (DynamoDB: `ChocoQA-MasterData`)
Each product includes:
- `productNo`, `productName`, `productType`
- `wpg`
- `specTempMin/Max`, `specViscosityMin/Max`

### Transactions (DynamoDB: `ChocoQA-Submissions`)
Each submission stores:
- batch identifiers (batchId, line/tank, timestamp)
- measured QA values (temp, viscosity)
- post-add action (type, amount)
- computed quality status (`OK/WARN/FAIL`)
- pointer to raw S3 JSON (`s3RawKey`)

---

## S3 Data Lake Layout (MVP)
s3://chocoqa-data/
└── qa-submissions/
└── year=YYYY/
└── month=MM/
└── day=DD/
└── submission-<uuid>.json
