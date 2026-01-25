-- Power BI Dashboard Queries for ChocoQA Analytics

-- 1. FAIL Rate by Product
SELECT 
  product,
  COUNT(*) as total_submissions,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as failures,
  ROUND(SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fail_rate_percent
FROM chocoqa_analytics.qa_submissions
GROUP BY product
ORDER BY fail_rate_percent DESC;

-- 2. Submission Trends Over Time (Updated with proper date formatting)
SELECT 
  date_parse(
    concat(year, '-', lpad(month, 2, '0'), '-', lpad(day, 2, '0')),
    '%Y-%m-%d'
  ) AS submission_date,
  COUNT(*) AS daily_submissions,
  AVG(temperature) AS avg_temperature,
  AVG(viscosity) AS avg_viscosity,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) AS daily_failures,
  ROUND(
    SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
    2
  ) AS daily_fail_rate
FROM chocoqa_analytics.qa_submissions
WHERE temperature IS NOT NULL
  AND viscosity IS NOT NULL
GROUP BY year, month, day
ORDER BY submission_date;

-- 3. Raw Data Query for Detailed Analysis
SELECT
  timestamp as eventTime,
  productId,
  temperature,
  viscosity,
  specStatus
FROM chocoqa_analytics.qa_submissions;

-- 4. Average Viscosity vs Spec by Product
SELECT 
  productId,
  AVG(viscosity) as avg_viscosity,
  COUNT(*) as sample_count,
  SUM(CASE WHEN specStatus = 'OK' THEN 1 ELSE 0 END) as in_spec_count,
  SUM(CASE WHEN specStatus = 'WARN' THEN 1 ELSE 0 END) as warn_count,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as fail_count
FROM chocoqa_analytics.qa_submissions
WHERE viscosity IS NOT NULL
GROUP BY productId;