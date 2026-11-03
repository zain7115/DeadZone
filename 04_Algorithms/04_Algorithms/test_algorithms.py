"""
DeadZone Algorithms Test Suite
Verifies graph traversal, dead zone detection, and candidate AP optimization ranking.
"""
import pytest
from models import NodeCoordinate
from graph import FloorPlanGraph
from deadzone_detector import DeadZoneDetector
from coverage_analyzer import CoverageAnalyzer
from ap_optimizer import APOptimizer

@pytest.fixture
def sample_graph():
    graph = FloorPlanGraph()
    # Add nodes matching the active survey North Block 2F
    graph.add_node(NodeCoordinate("P-041", x=23, y=25, rssi=-48, zone="Lab corridor"))
    graph.add_node(NodeCoordinate("P-040", x=47, y=33, rssi=-61, zone="Data lab"))
    graph.add_node(NodeCoordinate("P-039", x=74, y=59, rssi=-74, zone="Stairwell B"))
    graph.add_node(NodeCoordinate("P-038", x=33, y=68, rssi=-56, zone="Seminar room"))
    graph.add_node(NodeCoordinate("P-037", x=58, y=78, rssi=-67, zone="Faculty office"))

    # Connect edges
    graph.add_edge("P-041", "P-040")
    graph.add_edge("P-040", "P-039")
    graph.add_edge("P-040", "P-038")
    graph.add_edge("P-040", "P-037")
    return graph

def test_graph_shortest_path(sample_graph):
    path, dist = sample_graph.shortest_path("P-041", "P-039")
    assert path == ["P-041", "P-040", "P-039"]
    assert dist > 0

def test_deadzone_detection(sample_graph):
    detector = DeadZoneDetector(sample_graph, threshold_dbm=-67.0)
    clusters = detector.find_dead_zones()
    assert len(clusters) >= 1
    # P-039 has RSSI -74 < -67, so it must be detected
    found_points = [p for c in clusters for p in c.points]
    assert "P-039" in found_points

def test_coverage_analyzer():
    readings = [
        {"point": "P-041", "rssi": -48},
        {"point": "P-040", "rssi": -61},
        {"point": "P-039", "rssi": -74},
    ]
    analysis = CoverageAnalyzer.analyze_coverage(readings)
    assert analysis["totalPoints"] == 3
    assert analysis["distribution"]["weak"] == 1
    assert 0 <= analysis["coverageIndex"] <= 100

def test_ap_optimization_ranking(sample_graph):
    optimizer = APOptimizer(sample_graph)
    candidates = optimizer.run_optimization()
    assert len(candidates) == 3
    assert candidates[0].rank == "01"
    assert candidates[0].score >= candidates[1].score >= candidates[2].score
    assert candidates[0].label == "AP-C04"
