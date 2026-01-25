-- ChocoQA Analytics Tables for Athena

-- Create database
CREATE DATABASE IF NOT EXISTS chocoqa_analytics;

-- QA Submissions table with partitions
CREATE EXTERNAL TABLE IF NOT EXISTS chocoqa_analytics.qa_submissions (
  id string,
  product_id string,
  ingredient_id string,
  percentage double,
  temperature double,
  viscosity double,
  spec_status string,
  notes string,
  event_timestamp string
)
PARTITIONED BY (
  year string,
  month string,
  day string,
  product string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'true'
)
LOCATION 's3://chocoqa-data/analytics/'
TBLPROPERTIES (
  'projection.enabled' = 'false'
);

-- Load partitions after data is present
-- MSCK REPAIR TABLE chocoqa_analytics.qa_submissions;
