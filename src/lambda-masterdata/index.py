import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")

def handler(event, context):
    table_name = os.environ.get("MASTER_TABLE_NAME")
    table = dynamodb.Table(table_name)

    path = event.get("path") or event.get("rawPath", "")

    try:
        if path == "/master/ingredients":
            response = table.scan(
                FilterExpression=Attr("PK").begins_with("ING#")
            )

            ingredients = [
                {
                    "ingredientId": item.get("ingredientId"),
                    "ingredientName": item.get("ingredientName"),
                    "category": item.get("category"),
                    "allergens": item.get("allergens", []),
                    "defaultUnit": item.get("defaultUnit"),
                    "status": item.get("status")
                }
                for item in response.get("Items", [])
            ]

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"ingredients": ingredients})
            }

        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Resource not found"})
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
