import re

def clean_account_guid(guid):
    if not guid:
        return ""
    return re.sub(r'[^a-zA-Z0-9]', '', guid)[:32]

def transform_rows(rows, typemap, skip_partners, unit_factors):
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

            if not part_number:
                errors.append(f"Row {i}: Missing PartNumber, skipped.")
                continue

            if item_count <= 0:
                errors.append(f"Row {i}: itemCount <= 0, skipped.")
                continue

            if partner_id in skip_partners:
                continue

            product = typemap.get(part_number)
            if not product:
                errors.append(f"Row {i}: Unknown PartNumber {part_number}, skipped.")
                continue

            cleaned_guid = clean_account_guid(account_guid)
            usage = item_count // unit_factors.get(part_number, 1)

            product_totals[product] = product_totals.get(product, 0) + item_count

            transformed_chargeable_rows.append({
                "partnerID": partner_id,
                "product": product,
                "partnerPurchasedPlanID": cleaned_guid,
                "plan": plan,
                "usage": usage
            })

            domain_pairs.add((cleaned_guid, domain))

        except Exception as e:
            errors.append(f"Row {i}: Exception {str(e)}")

    return transformed_chargeable_rows, domain_pairs, product_totals, errors
