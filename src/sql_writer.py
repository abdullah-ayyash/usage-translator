def build_sql_statements(chargeable_rows, domain_pairs):
    """
    Build SQL INSERT statements for chargeable and domains tables.
    Escapes single quotes to ensure SQL safety.
    """
    chargeable_values = []
    for row in chargeable_rows:
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

    return chargeable_sql, domains_sql

def write_sql_output(chargeable_sql, domains_sql):
    """
    Write the generated SQL statements to output.sql file.
    """
    with open("output.sql", "w", encoding="utf-8") as f:
        f.write("-- Chargeable Table Insert\n")
        f.write(chargeable_sql + "\n\n")
        f.write("-- Domains Table Insert\n")
        f.write(domains_sql + "\n")

def print_summary(chargeable_rows, domain_pairs, errors, product_totals):
    """
    Print summary logs: valid/invalid rows, unique domains, and product totals.
    """
    print(f"\nTransformed {len(chargeable_rows)} valid chargeable rows.")
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
