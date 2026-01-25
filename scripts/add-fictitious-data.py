# add-fictitious-data.py (CLEAN)

import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "submission_data.csv"

PRODUCTS = ["CHOC001", "CHOC002", "CHOC003"]
INGREDIENTS = ["ING-001", "ING-002", "ING-003", "ING-004", "ING-006"]
STATUSES = ["OK", "WARN", "FAIL"]

start_date = datetime(2025, 1, 1)

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "submission_id", "product", "ingredient",
        "post_add_percent_ppm", "temperature_c",
        "viscosity", "spec_status",
        "submission_date", "year", "month", "day",
        "additional_qa_notes"
    ])

    for i in range(1, 51):
        date = start_date + timedelta(days=random.randint(0, 365))
        writer.writerow([
            f"S{i:03}",
            random.choice(PRODUCTS),
            random.choice(INGREDIENTS),
            round(random.uniform(0.05, 0.5), 3),
            round(random.uniform(38, 52), 1),
            random.randint(1200, 1800),
            random.choice(STATUSES),
            date.date().isoformat(),
            date.year,
            f"{date.month:02d}",
            f"{date.day:02d}",
            "Automated QA test record"
        ])
