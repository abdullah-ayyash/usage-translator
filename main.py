import os
import json
from dotenv import load_dotenv
import csv
import re

# Load environment variables
load_dotenv()

# Get file paths
CSV_PATH = os.getenv("CSV_PATH")
TYPEmap_PATH = os.getenv("TYPEmap_PATH")

# Parse SKIP_PARTNERS into a set of integers
raw_skip_partners = os.getenv("SKIP_PARTNERS", "")
SKIP_PARTNERS = set(map(int, raw_skip_partners.split(",")))

# Parse UNIT_FACTORS into a dictionary
raw_unit_factors = os.getenv("UNIT_FACTORS", "{}")
try:
    UNIT_FACTORS = json.loads(raw_unit_factors)
    UNIT_FACTORS = {k: int(v) for k, v in UNIT_FACTORS.items()}
except json.JSONDecodeError:
    print("Error: UNIT_FACTORS is not valid JSON in .env file.")
    UNIT_FACTORS = {}

## Load data files
# Load JSON typemap
with open(TYPEmap_PATH, "r", encoding="utf-8") as f:
    try:
        typemap = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading typemap JSON: {e}")
        typemap = {}

# Load CSV data
csv_rows = []
with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        csv_rows.append(row)

# Turn Guid into alphanumeric string of length 32 and strip any non-alphanumeric
def clean_account_guid(guid):
    if not guid:
        return ""
    
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', guid)
    return cleaned[:32]

transformed_chargeable_rows = []
domain_pairs = set()
product_totals = {}
errors = []

for i, row in enumerate(csv_rows):
    try:
        partner_id = int(row["PartnerID"])
        part_number = row["PartNumber"].strip()
        account_guid = row["accountGuid"].strip()
        item_count = int(row["itemCount"])
        domain = row.get("domains", "").strip()
        plan = row.get("plan", "").strip()

        # Validate required fields
        if not part_number:
            errors.append(f"Row {i}: Missing PartNumber, skipped.")
            continue

        if item_count <= 0:
            errors.append(f"Row {i}: itemCount <= 0, skipped.")
            continue

        if partner_id in SKIP_PARTNERS:
            continue  # silently skip

        # Map PartNumber to product value
        product = typemap.get(part_number)
        if not product:
            errors.append(f"Row {i}: Unknown PartNumber {part_number}, skipped.")
            continue

        cleaned_guid = clean_account_guid(account_guid)
        # Apply unit reduction rule if needed
        usage = item_count // UNIT_FACTORS.get(part_number, 1)

        # Save totals
        product_totals[product] = product_totals.get(product, 0) + item_count

        # Save transformed row
        transformed_chargeable_rows.append({
            "partnerID": partner_id,
            "product": product,
            "partnerPurchasedPlanID": cleaned_guid,
            "plan": plan,
            "usage": usage
        })

        # Save unique domain pair
        domain_pairs.add((cleaned_guid, domain))

    except Exception as e:
        errors.append(f"Row {i}: Exception {str(e)}")


## Build SQL Statements
chargeable_values = []
for row in transformed_chargeable_rows:
    # Escape single quotes to prevent SQL injection or syntax errors
    safe_product = row['product'].replace("'", "''")
    safe_guid = row['partnerPurchasedPlanID'].replace("'", "''")
    safe_plan = row['plan'].replace("'", "''")

    chargeable_values.append(
        f"({row['partnerID']}, '{safe_product}', '{safe_guid}', '{safe_plan}', {row['usage']})"
    )

chargeable_sql = (
    "INSERT INTO chargeable (partnerID, product, partnerPurchasedPlanID, plan, usage) VALUES\n" +
    ",\n".join(chargeable_values) +
    ";"
)

domain_values = []
for guid, domain in domain_pairs:
    # Escape single quotes to prevent SQL injection or syntax errors
    safe_guid = guid.replace("'", "''")
    safe_domain = domain.replace("'", "''")
    domain_values.append(f"('{safe_guid}', '{safe_domain}')")

domains_sql = (
    "INSERT INTO domains (partnerPurchasedPlanID, domain) VALUES\n" +
    ",\n".join(domain_values) +
    ";"
)

# Write to output.sql file
with open("output.sql", "w", encoding="utf-8") as f:
    f.write("-- Chargeable Table Insert\n")
    f.write(chargeable_sql + "\n\n")
    f.write("-- Domains Table Insert\n")
    f.write(domains_sql + "\n")

print(f"\nTransformed {len(transformed_chargeable_rows)} valid chargeable rows.")
print(f"Found {len(domain_pairs)} unique domain entries.")
print(f"Skipped {len(errors)} rows due to validation issues.")

if errors:
    print("\nValidation errors (first 5 shown):")
    for err in errors[:5]:
        print(" -", err)

print("\nRunning totals of itemCount by product:")
for product, total in product_totals.items():
    print(f" - {product}: {total}")

print("\nSQL statements written to output.sql")

