import os
import json
from dotenv import load_dotenv

def load_config():
    # Load environment variables
    load_dotenv()

    # Get file paths
    config = {
        "CSV_PATH": os.getenv("CSV_PATH"),
        "TYPEmap_PATH": os.getenv("TYPEmap_PATH"),
        # Parse SKIP_PARTNERS into a set of integers
        "SKIP_PARTNERS": set(map(int, os.getenv("SKIP_PARTNERS", "").split(","))),
    }

    # Parse UNIT_FACTORS into a dictionary
    raw_unit_factors = os.getenv("UNIT_FACTORS", "{}")
    try:
        config["UNIT_FACTORS"] = {k: int(v) for k, v in json.loads(raw_unit_factors).items()}
    except json.JSONDecodeError:
        print("Error: UNIT_FACTORS is not valid JSON in .env file.")
        config["UNIT_FACTORS"] = {}

    return config
