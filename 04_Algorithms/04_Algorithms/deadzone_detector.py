"""
DeadZone Detection Algorithm Module
Uses BFS/DFS connected components to detect and cluster contiguous weak-signal regions.
"""
from typing import List, Dict, Set
from collections import deque
from models import NodeCoordinate, DeadZoneCluster
from graph import FloorPlanGraph

DEADZONE_THRESHOLD_DBM = -67.0

class DeadZoneDetector:
    def __init__(self, graph: FloorPlanGraph, threshold_dbm: float = DEADZONE_THRESHOLD_DBM):
        self.graph = graph
        self.threshold = threshold_dbm

    def find_dead_zones(self) -> List[DeadZoneCluster]:
        """
        Detects weak-signal points (RSSI < threshold) and groups adjacent points
        into connected clusters using Breadth-First Search (BFS).
        """
        weak_nodes: Set[str] = {
            node_id for node_id, node in self.graph.nodes.items()
            if node.rssi < self.threshold
        }

        visited: Set[str] = set()
        clusters: List[DeadZoneCluster] = []
        cluster_idx = 1

        for start_node in weak_nodes:
            if start_node in visited:
                continue

            cluster_points = []
            queue = deque([start_node])
            visited.add(start_node)

            while queue:
                current = queue.popleft()
                cluster_points.append(current)

                for neighbor, _ in self.graph.adjacency.get(current, []):
                    if neighbor in weak_nodes and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            # Compute cluster metrics
            rssi_vals = [self.graph.nodes[nid].rssi for nid in cluster_points]
            avg_rssi = sum(rssi_vals) / len(rssi_vals)
            zones = list({self.graph.nodes[nid].zone for nid in cluster_points if self.graph.nodes[nid].zone})

            severity = "Critical" if avg_rssi < -75.0 else "Moderate"

            clusters.append(DeadZoneCluster(
                cluster_id=f"DZ-{str(cluster_idx).zfill(2)}",
                points=cluster_points,
                average_rssi=round(avg_rssi, 1),
                severity=severity,
                zone_names=zones
            ))
            cluster_idx += 1

        return clusters
