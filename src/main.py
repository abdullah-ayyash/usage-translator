from config import load_config
from parser import load_csv_data, load_typemap
from transformer import transform_rows
from sql_writer import build_sql_statements, write_sql_output, print_summary

def main():
    # Load config values from environment
    config = load_config()

    # Load JSON typemap
    typemap = load_typemap(config["TYPEmap_PATH"])

    # Load CSV data
    csv_rows = load_csv_data(config["CSV_PATH"])

    # Transform and validate each row
    chargeable_rows, domain_pairs, product_totals, errors = transform_rows(
        csv_rows,
        typemap,
        config["SKIP_PARTNERS"],
        config["UNIT_FACTORS"]
    )

    # Build final SQL INSERT statements
    chargeable_sql, domains_sql = build_sql_statements(chargeable_rows, domain_pairs)

    # Write SQL to output file
    write_sql_output(chargeable_sql, domains_sql)

    # Print summary logs and product totals
    print_summary(chargeable_rows, domain_pairs, errors, product_totals)

if __name__ == "__main__":
    main()
