# Power BI M Code Queries - ChocoQA Analytics

## 1. qa_submissions (FAIL Rate by Product)
```m
let
    Source = Odbc.Query(
        "dsn=Athena-ChocoQA",
        "
        SELECT
          product,
          COUNT(*) AS total_submissions,
          SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) AS failures,
          ROUND(
            (SUM(CASE WHEN specStatus = 'FAIL' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
            2
          ) AS fail_rate_percent
        FROM chocoqa_analytics.qa_submissions
        GROUP BY product
        ORDER BY fail_rate_percent DESC
        "
    )
in
    Source
```

## 2. qa_submissions_raw (Raw Data for Analysis)
```m
let
    Source = Odbc.Query(
        "dsn=Athena-ChocoQA",
        "
        SELECT
          timestamp as eventTime,
          productId,
          temperature,
          viscosity,
          specStatus
        FROM chocoqa_analytics.qa_submissions
        "
    )
in
    Source
```

## 3. Trends (Daily Submission Trends)
```m
let
    Source = Odbc.Query(
        "dsn=Athena-ChocoQA",
        "
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
        ORDER BY submission_date
        "
    )
in
    Source
```

## 4. Viscosity Analysis (Optional)
```m
let
    Source = Odbc.Query(
        "dsn=Athena-ChocoQA",
        "
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
        "
    )
in
    Source
```

## Usage Instructions:
1. **New Query** → **Blank Query** → **Advanced Editor**
2. **Paste M code** from above
3. **Done** → **Close & Apply**
4. **Create visualizations** from the imported data

## Key Features:
- ✅ Direct ODBC connection bypassing catalog issues
- ✅ Custom SQL with proper aggregations
- ✅ Real-time data from Athena
- ✅ Optimized for Power BI visualizations