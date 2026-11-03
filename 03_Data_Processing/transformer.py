"""
DeadZone Data Transformation Module
Classifies signal levels and computes survey aggregate metrics.
"""
from typing import List, Dict, Any

# Core classification thresholds defined across DeadZone
RSSI_GOOD_THRESHOLD = -55.0
RSSI_WATCH_THRESHOLD = -67.0

def classify_signal_status(rssi: float) -> str:
    """
    Classify signal condition based on RSSI:
    - Good: >= -55 dBm (Strong, robust throughput)
    - Watch: >= -67 dBm and < -55 dBm (Borderline, monitor)
    - Weak: < -67 dBm (Poor coverage / Dead zone candidate)
    """
    if rssi >= RSSI_GOOD_THRESHOLD:
        return "Good"
    elif rssi >= RSSI_WATCH_THRESHOLD:
        return "Watch"
    else:
        return "Weak"

def enrich_with_status(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich each measurement dictionary with its computed status."""
    enriched = []
    for r in records:
        copy_r = dict(r)
        copy_r["status"] = classify_signal_status(float(copy_r["rssi"]))
        enriched.append(copy_r)
    return enriched

def calculate_summary_metrics(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes statistical overview of surveyed environment:
    - Average RSSI
    - Average latency
    - Weak zone count
    - Overall coverage score index (0 - 100)
    """
    if not records:
        return {
            "totalSampled": 0,
            "averageRssi": 0.0,
            "averageLatency": 0.0,
            "weakZoneCount": 0,
            "coverageIndex": 0
        }

    rssi_vals = [float(r["rssi"]) for r in records]
    latency_vals = [float(r.get("latency", 0.0)) for r in records]
    weak_count = sum(1 for r in rssi_vals if r < RSSI_WATCH_THRESHOLD)

    avg_rssi = sum(rssi_vals) / len(rssi_vals)
    avg_latency = sum(latency_vals) / len(latency_vals)

    # Coverage Index calculation: normalizes average RSSI from [-90, -30] into [0, 100]
    normalized_score = int(max(0, min(100, (avg_rssi - (-90)) / (-30 - (-90)) * 100)))

    return {
        "totalSampled": len(records),
        "averageRssi": round(avg_rssi, 1),
        "averageLatency": round(avg_latency, 1),
        "weakZoneCount": weak_count,
        "coverageIndex": normalized_score
    }
