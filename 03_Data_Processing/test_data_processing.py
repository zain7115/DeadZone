"""
DeadZone Data Processing Test Suite
Tests data loading, cleaning, validation, transformation, and heatmap interpolation.
"""
import pytest
from pathlib import Path
from data_loader import load_from_json, load_from_csv
from cleaner import clean_measurements
from validator import validate_dataset, WiFIReadingSchema
from transformer import classify_signal_status, calculate_summary_metrics, enrich_with_status
from heatmap_generator import generate_heatmap_cells

DATASET_DIR = Path(__file__).parent / "dataset"

def test_load_sample_json():
    json_path = DATASET_DIR / "sample_measurements.json"
    records = load_from_json(str(json_path))
    assert len(records) >= 5
    assert records[0]["point"] == "P-041"

def test_load_sample_csv():
    csv_path = DATASET_DIR / "sample_measurements.csv"
    records = load_from_csv(str(csv_path))
    assert len(records) >= 5
    assert isinstance(records[0]["rssi"], float)

def test_signal_status_classification():
    assert classify_signal_status(-45.0) == "Good"
    assert classify_signal_status(-55.0) == "Good"
    assert classify_signal_status(-60.0) == "Watch"
    assert classify_signal_status(-67.0) == "Watch"
    assert classify_signal_status(-75.0) == "Weak"

def test_clean_measurements_outliers():
    dirty = [
        {"point": "P-001", "rssi": -50.0},
        {"point": "P-002", "rssi": -999.0},  # Extreme outlier
        {"point": "", "rssi": -60.0},        # Missing point
        {"point": "P-004", "rssi": None},     # Missing rssi
    ]
    cleaned = clean_measurements(dirty)
    assert len(cleaned) == 1
    assert cleaned[0]["point"] == "P-001"

def test_summary_metrics():
    sample = [
        {"point": "P-1", "rssi": -50.0, "latency": 20.0},
        {"point": "P-2", "rssi": -80.0, "latency": 60.0},
    ]
    metrics = calculate_summary_metrics(sample)
    assert metrics["totalSampled"] == 2
    assert metrics["averageRssi"] == -65.0
    assert metrics["weakZoneCount"] == 1
    assert 0 <= metrics["coverageIndex"] <= 100

def test_heatmap_generation():
    map_points = [
        {"id": "P-1", "x": 20, "y": 20},
        {"id": "P-2", "x": 80, "y": 80}
    ]
    measurements = [
        {"point": "P-1", "rssi": -45.0},
        {"point": "P-2", "rssi": -80.0}
    ]
    cells = generate_heatmap_cells(map_points, measurements, rows=7, cols=12)
    assert len(cells) == 84
    assert all(0 <= c <= 100 for c in cells)
