import re

def clean_account_guid(guid):
    """
    Clean a GUID by removing non-alphanumeric characters and trimming to 32 characters.
    """
    if not guid:
        return ""
    return re.sub(r'[^a-zA-Z0-9]', '', guid)[:32]

def transform_rows(rows, typemap, skip_partners, unit_factors):
    """
    Validate and transform each row from the CSV.
    Returns: valid chargeable rows, unique domain pairs, product totals, and error logs.
    """
    transformed_chargeable_rows = []
    domain_pairs = set()
    product_totals = {}
    errors = []

    for i, row in enumerate(rows):
        try:
            partner_id = int(row["PartnerID"])
            part_number = row["PartNumber"].strip()
            account_guid = row["accountGuid"].strip()
            item_count = int(row["itemCount"])
            domain = row.get("domains", "").strip()
            plan = row.get("plan", "").strip()
            # Validate required fields
            if not part_number:
                errors.append(f"Line {i}: Missing PartNumber, skipped. (Row {i+2} in CSV)")
                continue

            if item_count <= 0:
                errors.append(f"Row {i}: itemCount <= 0, skipped. (Row {i+2} in CSV)")
                continue

            if partner_id in skip_partners:
                continue  # silently skip

            # Map PartNumber to product value
            product = typemap.get(part_number)
            if not product:
                errors.append(f"Row {i}: Unknown PartNumber {part_number}, skipped.  (Row {i+2} in CSV)")
                continue

            # Clean and normalize account GUID
            cleaned_guid = clean_account_guid(account_guid)

            # Apply unit reduction rule if needed
            usage = item_count // unit_factors.get(part_number, 1)

            # Save totals (itemCount before reduction)
            product_totals[product] = product_totals.get(product, 0) + item_count

            # Save transformed row for SQL
            transformed_chargeable_rows.append({
                "partnerID": partner_id,
                "product": product,
                "partnerPurchasedPlanID": cleaned_guid,
                "plan": plan,
                "usage": usage
            })

            # Track unique domain entries
            domain_pairs.add((cleaned_guid, domain))

        except Exception as e:
            errors.append(f"Row {i}: Exception {str(e)}")

    return transformed_chargeable_rows, domain_pairs, product_totals, errors
