# Power BI + Athena Setup Guide

## Step 1: Install Amazon Athena ODBC Driver (64-bit)

**Download and install:**
- Simba Amazon Athena ODBC Driver (64-bit)
- URL: https://docs.aws.amazon.com/athena/latest/ug/connect-with-odbc.html

## Step 2: Create 64-bit System DSN

1. **Open:** Start Menu → "ODBC Data Sources (64-bit)"
2. **System DSN tab** → Add
3. **Choose:** Simba Amazon Athena ODBC Driver
4. **Configure:**
   - **Name:** Athena-ChocoQA
   - **Region:** us-east-1
   - **Workgroup:** primary (or your workgroup)
   - **S3 Output Location:** s3://chocoqa-data-675774797158/athena-results/
   - **Authentication:** Use your AWS Access Key + Secret Key

## Step 3: Set Athena Query Result Location

In Athena Console:
1. **Settings** → **Manage**
2. **Query result location:** s3://chocoqa-data-675774797158/athena-results/
3. **Save**

## Step 4: Connect Power BI

1. **Get Data** → Search "Athena"
2. **Choose:** Amazon Athena
3. **DSN:** Athena-ChocoQA
4. **Data Connectivity:** Import
5. **Select Database:** chocoqa_analytics
6. **Select Table:** qa_submissions

## Step 5: Create Power BI Dashboards

Use these queries in Power BI:

### FAIL Rate by Product
```sql
SELECT 
  product,
  COUNT(*) as total_submissions,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as failures,
  ROUND(SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fail_rate_percent
FROM chocoqa_analytics.qa_submissions
GROUP BY product
ORDER BY fail_rate_percent DESC
```

### Submission Trends
```sql
SELECT 
  CONCAT(year, '-', month, '-', day) as submission_date,
  COUNT(*) as daily_submissions,
  AVG(temperature) as avg_temperature,
  AVG(viscosity) as avg_viscosity,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as daily_failures
FROM chocoqa_analytics.qa_submissions
WHERE temperature IS NOT NULL AND viscosity IS NOT NULL
GROUP BY year, month, day
ORDER BY year, month, day
```

### Viscosity Analysis
```sql
SELECT 
  productId,
  AVG(viscosity) as avg_viscosity,
  COUNT(*) as sample_count,
  SUM(CASE WHEN specStatus = 'OK' THEN 1 ELSE 0 END) as in_spec_count,
  SUM(CASE WHEN specStatus = 'WARN' THEN 1 ELSE 0 END) as warn_count,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as fail_count
FROM chocoqa_analytics.qa_submissions
WHERE viscosity IS NOT NULL
GROUP BY productId
```

## Troubleshooting

- **64-bit vs 32-bit:** Ensure you use 64-bit ODBC driver and DSN
- **S3 Permissions:** Verify write access to athena-results bucket
- **IAM Permissions:** Ensure athena:*, glue:*, s3:* permissions
- **Workgroup:** Use the correct Athena workgroup

## Architecture

✅ **Correct:** Power BI ↔ Athena (via ODBC) ↔ S3 Data
❌ **Avoid:** Power BI ↔ API Gateway (for BI queries)