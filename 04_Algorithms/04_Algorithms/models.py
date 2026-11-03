"""
DeadZone Algorithm Domain Models
Dataclasses for graph structures, candidate APs, and detected dead zones.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class NodeCoordinate:
    id: str
    x: float
    y: float
    rssi: float = 0.0
    zone: str = ""

@dataclass
class DeadZoneCluster:
    cluster_id: str
    points: List[str]
    average_rssi: float
    severity: str  # 'Critical', 'Moderate', 'Watch'
    zone_names: List[str]

@dataclass
class CandidateAP:
    rank: str
    label: str
    zone: str
    score: int
    lift: str
    constraints: str
    tone: str
    graph_path: List[str]
    algorithm: str = "weighted-shortest-path"
