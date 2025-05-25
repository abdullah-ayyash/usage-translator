from config import load_config
from parser import load_csv_data, load_typemap
from transformer import transform_rows
from sql_writer import build_sql_statements, write_sql_output, print_summary

def main():
    config = load_config()
    typemap = load_typemap(config["TYPEmap_PATH"])
    csv_rows = load_csv_data(config["CSV_PATH"])

    chargeable_rows, domain_pairs, product_totals, errors = transform_rows(
        csv_rows,
        typemap,
        config["SKIP_PARTNERS"],
        config["UNIT_FACTORS"]
    )

    chargeable_sql, domains_sql = build_sql_statements(chargeable_rows, domain_pairs)
    write_sql_output(chargeable_sql, domains_sql)
    print_summary(chargeable_rows, domain_pairs, errors, product_totals)

if __name__ == "__main__":
    main()
