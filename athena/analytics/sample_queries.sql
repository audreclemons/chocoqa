-- ChocoQA Athena Analytics Queries

-- 1. Basic data validation
SELECT COUNT(*) as total_records 
FROM chocoqa_analytics.qa_submissions;

-- 2. Failure rate by product type
SELECT 
  product,
  COUNT(*) as total_batches,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as failures,
  ROUND(SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fail_rate_percent
FROM chocoqa_analytics.qa_submissions
GROUP BY product
ORDER BY fail_rate_percent DESC;

-- 3. Quality trends by year
SELECT 
  year,
  COUNT(*) as total_submissions,
  SUM(CASE WHEN specStatus = 'OK' THEN 1 ELSE 0 END) as ok_count,
  SUM(CASE WHEN specStatus = 'WARN' THEN 1 ELSE 0 END) as warn_count,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as fail_count,
  ROUND(SUM(CASE WHEN specStatus = 'OK' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as ok_percentage
FROM chocoqa_analytics.qa_submissions
GROUP BY year
ORDER BY year;

-- 4. Temperature analysis by product
SELECT 
  product,
  ROUND(AVG(temperature), 2) as avg_temp,
  ROUND(MIN(temperature), 2) as min_temp,
  ROUND(MAX(temperature), 2) as max_temp,
  COUNT(*) as sample_count
FROM chocoqa_analytics.qa_submissions
GROUP BY product
ORDER BY avg_temp DESC;

-- 5. Viscosity distribution
SELECT 
  CASE 
    WHEN viscosity < 1300 THEN 'Low (< 1300)'
    WHEN viscosity BETWEEN 1300 AND 1800 THEN 'Normal (1300-1800)'
    WHEN viscosity > 1800 THEN 'High (> 1800)'
  END as viscosity_range,
  COUNT(*) as batch_count,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM chocoqa_analytics.qa_submissions), 1) as percentage
FROM chocoqa_analytics.qa_submissions
GROUP BY 1
ORDER BY batch_count DESC;

-- 6. Ingredient usage analysis
SELECT 
  ingredient,
  COUNT(*) as usage_count,
  ROUND(AVG(percentage), 2) as avg_percentage,
  ROUND(MIN(percentage), 2) as min_percentage,
  ROUND(MAX(percentage), 2) as max_percentage
FROM chocoqa_analytics.qa_submissions
GROUP BY ingredient
ORDER BY usage_count DESC;

-- 7. Monthly quality performance (2025 focus)
SELECT 
  month,
  COUNT(*) as batches,
  SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) as failures,
  ROUND(AVG(temperature), 1) as avg_temp,
  ROUND(AVG(viscosity), 0) as avg_viscosity
FROM chocoqa_analytics.qa_submissions
WHERE year = '2025'
GROUP BY month
ORDER BY month;

-- 8. Process improvement analysis (2025 vs 2026)
SELECT 
  year,
  product,
  COUNT(*) as batches,
  ROUND(SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as fail_rate,
  ROUND(AVG(temperature), 1) as avg_temp,
  ROUND(AVG(viscosity), 0) as avg_viscosity
FROM chocoqa_analytics.qa_submissions
WHERE year IN ('2025', '2026')
GROUP BY year, product
ORDER BY year, product;