import json
import csv

def load_typemap(path):
    """
    Load the JSON typemap file that maps PartNumber to product value.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading typemap: {e}")
        return {}

def load_csv_data(path):
    """
    Load CSV usage report and return list of rows as dictionaries.
    """
    rows = []
    try:
        with open(path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return rows
