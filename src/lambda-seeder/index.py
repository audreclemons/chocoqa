import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

INGREDIENTS = [
    {"ingredientId": "ING-001", "ingredientName": "Cocoa Liquor", "category": "COCOA", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-002", "ingredientName": "Cocoa Butter", "category": "FAT", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-003", "ingredientName": "Sugar", "category": "SWEETENER", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-004", "ingredientName": "Milk Powder", "category": "DAIRY", "allergens": ["MILK"], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-005", "ingredientName": "Milk Fat", "category": "DAIRY_FAT", "allergens": ["MILK"], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-006", "ingredientName": "Soy Lecithin", "category": "EMULSIFIER", "allergens": ["SOY"], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-007", "ingredientName": "Sunflower Lecithin", "category": "EMULSIFIER", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-008", "ingredientName": "PGPR", "category": "EMULSIFIER", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-009", "ingredientName": "Vanilla Flavor", "category": "FLAVOR", "allergens": [], "defaultUnit": "ppm", "status": "ACTIVE"},
    {"ingredientId": "ING-010", "ingredientName": "Salt", "category": "MINOR_INGREDIENT", "allergens": [], "defaultUnit": "ppm", "status": "ACTIVE"},
    {"ingredientId": "ING-011", "ingredientName": "Almond Pieces", "category": "INCLUSION", "allergens": ["TREE_NUTS"], "defaultUnit": "%", "status": "ACTIVE"},
    {"ingredientId": "ING-012", "ingredientName": "Crisped Rice", "category": "INCLUSION", "allergens": [], "defaultUnit": "%", "status": "ACTIVE"}
]

def handler(event, context):
    table_name = os.environ.get("MASTER_TABLE_NAME")
    table = dynamodb.Table(table_name)

    try:
        for ingredient in INGREDIENTS:
            table.put_item(
                Item={
                    "PK": f"ING#{ingredient['ingredientId']}",
                    "SK": "META",
                    **ingredient
                }
            )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Seeded {len(INGREDIENTS)} ingredients"})
        }

    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Seeding failed"})
        }
