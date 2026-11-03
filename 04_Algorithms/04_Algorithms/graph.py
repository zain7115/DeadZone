"""
DeadZone Floor-Plan Graph & Spatial Traversal Module
Implements adjacency representations and Dijkstra weighted shortest path.
"""
import math
import heapq
from typing import Dict, List, Tuple, Optional
from models import NodeCoordinate

class FloorPlanGraph:
    """Represents measurement points and physical hallways as a weighted graph."""

    def __init__(self):
        self.nodes: Dict[str, NodeCoordinate] = {}
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: NodeCoordinate):
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = []

    def add_edge(self, u: str, v: str, weight: Optional[float] = None):
        if u not in self.nodes or v not in self.nodes:
            raise KeyError(f"Both nodes {u} and {v} must exist in the graph.")

        if weight is None:
            # Euclidean distance in floor plan % coordinates
            n1, n2 = self.nodes[u], self.nodes[v]
            weight = math.hypot(n1.x - n2.x, n1.y - n2.y)

        self.adjacency[u].append((v, weight))
        self.adjacency[v].append((u, weight))

    def shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        Dijkstra algorithm to find the shortest path between two points.
        Returns (path_nodes, total_weight).
        """
        if start not in self.nodes or end not in self.nodes:
            return ([], float("inf"))

        distances = {node: float("inf") for node in self.nodes}
        previous = {node: None for node in self.nodes}
        distances[start] = 0.0

        pq = [(0.0, start)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)

            if curr_node == end:
                break

            if curr_dist > distances[curr_node]:
                continue

            for neighbor, weight in self.adjacency.get(curr_node, []):
                new_dist = curr_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = curr_node
                    heapq.heappush(pq, (new_dist, neighbor))

        # Reconstruct path
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        if not path or path[0] != start:
            return ([], float("inf"))

        return (path, distances[end])
