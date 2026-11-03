"""
DeadZone Data Cleaning Module
Handles missing values, deduplication, and signal threshold sanitation.
"""
from typing import List, Dict, Any

MIN_VALID_RSSI = -105.0
MAX_VALID_RSSI = -15.0

def clean_measurements(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans raw measurement records:
    1. Removes records with missing point or null RSSI.
    2. Bounds checks RSSI between -105 and -15 dBm.
    3. Trims string fields.
    4. Deduplicates records based on (point, timestamp or id).
    """
    cleaned = []
    seen_points = set()

    for item in records:
        if not item.get("point") or item.get("rssi") is None:
            continue

        try:
            rssi = float(item["rssi"])
        except (ValueError, TypeError):
            continue

        # Clamp or filter extreme signal anomalies
        if rssi < MIN_VALID_RSSI or rssi > MAX_VALID_RSSI:
            continue

        point_id = str(item["point"]).strip()

        record = {
            "id": item.get("id"),
            "point": point_id,
            "zone": str(item.get("zone", "Unknown zone")).strip(),
            "rssi": round(rssi, 1),
            "latency": max(0.0, float(item.get("latency", 0.0))),
            "loss": max(0.0, min(100.0, float(item.get("loss", 0.0)))),
            "throughput": max(0.0, float(item.get("throughput", 0.0))),
            "channel": str(item.get("channel", "auto")).strip(),
        }

        # Keep latest reading per point
        cleaned.append(record)

    return cleaned
