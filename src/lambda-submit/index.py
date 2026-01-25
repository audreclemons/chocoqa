import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

def handler(event, context):
    table_name = os.environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)

    try:
        body = json.loads(event.get("body", "{}"))

        item = {
            "id": f"{body.get('productId', 'UNKNOWN')}-{datetime.utcnow().isoformat()}",
            "productId": body.get("productId"),
            "ingredientId": body.get("ingredientId", ""),
            "percentage": body.get("percentage", 0),
            "data": body.get("data", ""),
            "timestamp": body.get("timestamp", datetime.utcnow().isoformat())
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Success"})
        }

    except Exception:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Internal server error"})
        }
