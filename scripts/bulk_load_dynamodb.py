# bulk_load_dynamodb.py (CLEAN)

import boto3
import csv
from decimal import Decimal
from datetime import datetime

TABLE_NAME = "chocoqa-data"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

with open("submission_data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        item = {
            "id": row["submission_id"],
            "productId": row["product"],
            "ingredientId": row["ingredient"],
            "percentage": Decimal(row["post_add_percent_ppm"]),
            "temperature": Decimal(row["temperature_c"]),
            "viscosity": Decimal(row["viscosity"]),
            "specStatus": row["spec_status"],
            "data": row["additional_qa_notes"],
            "timestamp": f"{row['submission_date']}T00:00:00Z"
        }
        table.put_item(Item=item)
