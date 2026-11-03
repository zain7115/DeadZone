"""
DeadZone Backend Services & Business Logic
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import SurveyModel, MeasurementModel, MapPointModel
from schemas import MeasurementCreate, OptimizationCandidate

DEFAULT_HEAT_CELLS = [
    82,88,91,86,79,69,60,44,38,45,57,71,
    89,94,96,92,83,74,67,52,42,47,62,78,
    86,90,93,87,81,70,64,48,34,41,58,76,
    78,84,87,82,75,66,54,39,28,36,51,69,
    72,79,81,77,69,59,47,34,24,31,46,63,
    66,72,76,71,63,52,43,31,22,27,41,58,
    59,65,68,64,57,47,37,29,21,25,38,54,
    53,59,62,57,50,41,33,26,19,24,34,48,
]

def seed_initial_data(db: Session):
    """Seed SQLite database with initial survey records if empty."""
    survey = db.query(SurveyModel).filter(SurveyModel.id == "DZ-2026-10-14").first()
    if not survey:
        survey = SurveyModel(id="DZ-2026-10-14", building="North Block", floor="2nd floor", points_total=48)
        db.add(survey)
        db.commit()

        initial_measurements = [
            {"id": "M-041", "point": "P-041", "zone": "Lab corridor", "rssi": -48, "latency": 18, "loss": 0.2, "throughput": 87, "channel": "36 / 5 GHz", "status": "Good"},
            {"id": "M-040", "point": "P-040", "zone": "Data lab", "rssi": -61, "latency": 27, "loss": 0.8, "throughput": 61, "channel": "36 / 5 GHz", "status": "Watch"},
            {"id": "M-039", "point": "P-039", "zone": "Stairwell B", "rssi": -74, "latency": 46, "loss": 3.4, "throughput": 28, "channel": "11 / 2.4 GHz", "status": "Weak"},
            {"id": "M-038", "point": "P-038", "zone": "Seminar room", "rssi": -56, "latency": 21, "loss": 0.5, "throughput": 72, "channel": "44 / 5 GHz", "status": "Good"},
            {"id": "M-037", "point": "P-037", "zone": "Faculty office", "rssi": -67, "latency": 34, "loss": 1.9, "throughput": 42, "channel": "11 / 2.4 GHz", "status": "Watch"},
        ]
        for m in initial_measurements:
            db.add(MeasurementModel(survey_id="DZ-2026-10-14", **m))

        initial_points = [
            {"id": "P-041", "x": 23, "y": 25, "tone": "good", "zone": "Lab corridor"},
            {"id": "P-040", "x": 47, "y": 33, "tone": "watch", "zone": "Data lab"},
            {"id": "P-039", "x": 74, "y": 59, "tone": "weak", "zone": "Stairwell B"},
            {"id": "P-038", "x": 33, "y": 68, "tone": "good", "zone": "Seminar room"},
            {"id": "P-037", "x": 58, "y": 78, "tone": "watch", "zone": "Faculty office"},
        ]
        for p in initial_points:
            db.add(MapPointModel(**p))

        db.commit()

def calculate_status(rssi: float) -> str:
    """Derive status from RSSI value."""
    if rssi >= -55:
        return "Good"
    elif rssi >= -67:
        return "Watch"
    else:
        return "Weak"

def add_measurement(db: Session, measurement_in: MeasurementCreate) -> MeasurementModel:
    """Save new measurement record to database."""
    total_count = db.query(MeasurementModel).count()
    new_id = f"M-{str(total_count + 37).zfill(3)}"
    status = calculate_status(measurement_in.rssi)

    db_item = MeasurementModel(
        id=new_id,
        survey_id="DZ-2026-10-14",
        point=measurement_in.point,
        zone=measurement_in.zone or "Unknown zone",
        rssi=measurement_in.rssi,
        latency=measurement_in.latency or 0.0,
        loss=measurement_in.loss or 0.0,
        throughput=measurement_in.throughput or 0.0,
        channel=measurement_in.channel or "auto",
        status=status
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def run_optimization(coordinates: list) -> List[OptimizationCandidate]:
    """
    Simulation of the Access Point Candidate optimization engine.
    Integrates with Module 04 (Algorithms).
    """
    candidates = [
        OptimizationCandidate(
            rank="01",
            label="AP-C04",
            zone="Stairwell B / north landing",
            score=91,
            lift="+24%",
            constraints="Power nearby • clear sightline",
            tone="cyan",
            graphPath=["P-039", "P-040", "P-041"],
            algorithm="weighted-shortest-path"
        ),
        OptimizationCandidate(
            rank="02",
            label="AP-C02",
            zone="Seminar room / east wall",
            score=84,
            lift="+18%",
            constraints="Needs ceiling drop • low overlap",
            tone="amber",
            graphPath=["P-038", "P-040"],
            algorithm="weighted-shortest-path"
        ),
        OptimizationCandidate(
            rank="03",
            label="AP-C07",
            zone="Data lab / south aisle",
            score=76,
            lift="+12%",
            constraints="High channel overlap",
            tone="slate",
            graphPath=["P-037", "P-040"],
            algorithm="weighted-shortest-path"
        )
    ]
    return candidates
