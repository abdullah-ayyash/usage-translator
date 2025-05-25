import os
import json
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    config = {
        "CSV_PATH": os.getenv("CSV_PATH"),
        "TYPEmap_PATH": os.getenv("TYPEmap_PATH"),
        "SKIP_PARTNERS": set(map(int, os.getenv("SKIP_PARTNERS", "").split(","))),
    }

    raw_unit_factors = os.getenv("UNIT_FACTORS", "{}")
    try:
        config["UNIT_FACTORS"] = {k: int(v) for k, v in json.loads(raw_unit_factors).items()}
    except json.JSONDecodeError:
        print("Error: UNIT_FACTORS is not valid JSON in .env file.")
        config["UNIT_FACTORS"] = {}

    return config
