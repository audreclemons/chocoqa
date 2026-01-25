# ChocoQA Platform - Troubleshooting Guide

## Issue 0: Initial Project Setup on Network Drive
**Error**: Various npm, Python, and AWS CLI issues on Z:\ drive
**Cause**: Network drives cause path resolution and permission issues
**Resolution**: Work directly on network drive but use inline Lambda code in SAM template

## Issue 1: NPM Build Failures on Network Drive
**Error**: `npm ERR! Invalid file: URL, must be absolute if // present`
**Cause**: Python virtual environments and npm don't work reliably on Windows UNC/network paths
**Resolution**: 
- Use inline Lambda code in SAM template instead of external files
- Or move project to local drive (C:\) for development

## Issue 2: AWS SDK Module Not Found in Lambda
**Error**: `Cannot find module 'aws-sdk'`
**Cause**: Node.js 18.x runtime doesn't include AWS SDK v2 by default
**Resolution**: Use AWS SDK v3 syntax:
```javascript
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand } = require('@aws-sdk/lib-dynamodb');
```

## Issue 3: DynamoDB Query Syntax Error
**Error**: `Query key condition not supported`
**Cause**: Incorrect KeyConditionExpression with `begins_with()`
**Resolution**: Use ScanCommand with FilterExpression for prefix matching:
```javascript
const result = await dynamodb.send(new ScanCommand({
    TableName: process.env.MASTER_TABLE_NAME,
    FilterExpression: 'begins_with(PK, :pk)',
    ExpressionAttributeValues: { ':pk': 'ING#' }
}));
```

## Issue 4: CORS Errors from Browser
**Error**: `net::ERR_FAILED` on POST requests
**Cause**: Missing CORS configuration in API Gateway
**Resolution**: Add global CORS in SAM template:
```yaml
Globals:
  Api:
    Cors:
      AllowMethods: "'GET,POST,OPTIONS'"
      AllowHeaders: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
      AllowOrigin: "'*'"
```

## Issue 5: File:// Origin Blocking HTTPS Requests
**Error**: `net::ERR_FAILED` when loading from `file://` URL
**Cause**: Browsers block file:// origins from making HTTPS API calls
**Resolution**: 
- Serve files via HTTP server: `python -m http.server 8000`
- Or deploy to S3 static website hosting

## Issue 6: S3 Block Public Access Preventing Website Hosting
**Error**: Cannot access S3 website, bucket policy denied
**Cause**: S3 Block Public Access settings prevent public website hosting
**Resolution**: 
1. In S3 Console → Bucket → Permissions → Block public access
2. Click "Edit" and uncheck all 4 boxes
3. Save changes and confirm
4. Apply bucket policy for public read access
5. Enable static website hosting

## Issue 7: Lambda Function Name Resolution
**Error**: `Function not found: chocolate-SeederFunction`
**Cause**: SAM generates unique suffixes for function names
**Resolution**: Use AWS CLI to find actual function names:
```bash
aws lambda list-functions --query "Functions[?contains(FunctionName, 'chocolate')].FunctionName"
```

## Issue 8: @smithy/util-base64 toBase64 Type Error
**Error**: `toBase64 encoder function only accepts string | Uint8Array`
**Cause**: Passing incompatible data types (Buffer, Object, ArrayBuffer) to toBase64
**Resolution**: Convert to accepted types:
```javascript
// Buffer to Uint8Array
const encoded = toBase64(new Uint8Array(buffer));
// Object to string
const encoded = toBase64(JSON.stringify(data));
// ArrayBuffer to Uint8Array
const encoded = toBase64(new Uint8Array(arrayBuffer));
```

## Issue 9: Stack Deletion Breaking Project
**Error**: All AWS resources missing after stack deletion
**Cause**: CloudFormation stack deletion removes all provisioned resources
**Resolution**: Redeploy the entire stack:
```bash
cd sam
sam build
sam deploy --guided
```
Then re-seed data and update web app endpoints.

## Issue 10: S3 Bucket ACL Not Supported Error
**Error**: `The bucket does not allow ACLs`
**Cause**: S3 bucket created with ACLs disabled by default
**Resolution**: Upload without ACL flags:
```bash
aws s3 sync web/ s3://bucket-name/
# Instead of: aws s3 sync web/ s3://bucket-name/ --acl public-read
```
Then use bucket policy for public access.

## Issue 11: Athena JSON Table Creation Error
**Error**: `FAILED: SemanticException Unrecognized file format in STORED AS clause: 'JSON'`
**Cause**: Athena doesn't support `STORED AS JSON` syntax for JSON files
**Resolution**: Use JSON SerDe instead:
```sql
CREATE EXTERNAL TABLE table_name (...)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://bucket/path/'
```

## Issue 12: Athena Table Shows Headers But No Data
**Error**: Query returns column headers but empty result set
**Cause**: Incorrect table format for JSON data (using TEXTFILE instead of JSON SerDe)
**Resolution**: 
1. Drop and recreate table with proper JSON SerDe
2. Run `MSCK REPAIR TABLE table_name` to load partitions
3. Verify with `SELECT * FROM table_name LIMIT 5`

## Issue 14: Power BI Cannot See Athena Databases/Tables
**Error**: Empty database list or missing chocoqa_analytics database in Power BI
**Cause**: Insufficient Glue permissions for IAM user to discover databases and tables
**Resolution**: Ensure IAM policy includes complete permissions:
```json
{
  "Effect": "Allow",
  "Action": [
    "athena:ListWorkGroups", "athena:GetWorkGroup", "athena:StartQueryExecution",
    "athena:GetQueryExecution", "athena:GetQueryResults", "athena:ListDataCatalogs",
    "athena:ListDatabases", "athena:ListTableMetadata",
    "glue:GetDatabases", "glue:GetDatabase", "glue:GetTables", 
    "glue:GetTable", "glue:GetPartitions",
    "s3:ListBucket", "s3:GetObject", "s3:PutObject", "s3:GetBucketLocation"
  ],
  "Resource": "*"
}
```

## Power BI + Athena Architecture Flow
```
Power BI Desktop
  → Athena ODBC DSN (Athena-ChocoQA)
      → Athena Workgroup (primary or PostAddFormWorkgroup)
          → Glue Catalog (AwsDataCatalog)
              → Database (chocoqa_analytics)
                  → Table (qa_submissions)
                      → S3-backed data lake
```

**Key Points:**
- Use `primary` workgroup for guaranteed access
- Wait 1-2 minutes after IAM policy updates
- Glue permissions required for database/table discovery
- S3 permissions needed for both data access and query results

---
*Document updated: 2026-01-04*