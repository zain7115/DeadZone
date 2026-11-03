"""
DeadZone Data Loader Module
Reads measurement datasets from JSON or CSV files.
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Any

def load_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Loads measurements list from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Loads measurements list from a CSV file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    records = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = dict(row)
            if "rssi" in record:
                record["rssi"] = float(record["rssi"])
            if "latency" in record:
                record["latency"] = float(record["latency"])
            if "loss" in record:
                record["loss"] = float(record["loss"])
            if "throughput" in record:
                record["throughput"] = float(record["throughput"])
            records.append(record)
    return records
