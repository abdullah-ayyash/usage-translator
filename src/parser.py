import json
import csv

def load_typemap(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading typemap: {e}")
        return {}

def load_csv_data(path):
    rows = []
    try:
        with open(path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return rows
