# bulk_load_s3.py (CLEAN)

import boto3
import csv
import json

sts = boto3.client("sts")
account_id = sts.get_caller_identity()["Account"]
bucket = f"chocoqa-data-{account_id}"

s3 = boto3.client("s3")

with open("submission_data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        payload = {
            "id": row["submission_id"],
            "productId": row["product"],
            "ingredientId": row["ingredient"],
            "percentage": float(row["post_add_percent_ppm"]),
            "temperature": float(row["temperature_c"]),
            "viscosity": int(row["viscosity"]),
            "specStatus": row["spec_status"],
            "timestamp": f"{row['submission_date']}T00:00:00Z"
        }

        key = (
            f"analytics/year={row['year']}/"
            f"month={row['month']}/"
            f"day={row['day']}/"
            f"product={row['product']}/"
            f"{row['submission_id']}.json"
        )

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(payload),
            ContentType="application/json"
        )
