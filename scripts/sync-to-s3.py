# sync-to-s3.py (CLEAN)

import boto3
import json
import os
from datetime import datetime

sts = boto3.client("sts")
account_id = os.environ.get("AWS_ACCOUNT_ID") or sts.get_caller_identity()["Account"]
bucket = f"chocoqa-data-{account_id}"

s3 = boto3.client("s3")

with open("dynamodb-data.json") as f:
    records = json.load(f)["Items"]

for item in records:
    record = {
        "id": item["id"]["S"],
        "productId": item["productId"]["S"],
        "ingredientId": item.get("ingredientId", {}).get("S", ""),
        "percentage": float(item.get("percentage", {}).get("N", 0)),
        "temperature": float(item["temperature"]["N"]) if "temperature" in item else None,
        "viscosity": float(item["viscosity"]["N"]) if "viscosity" in item else None,
        "specStatus": item["specStatus"]["S"],
        "timestamp": item["timestamp"]["S"]
    }

    dt = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
    key = (
        f"analytics/year={dt.year}/"
        f"month={dt.month:02d}/"
        f"day={dt.day:02d}/"
        f"product={record['productId']}/"
        f"{record['id']}.json"
    )

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(record),
        ContentType="application/json"
    )
