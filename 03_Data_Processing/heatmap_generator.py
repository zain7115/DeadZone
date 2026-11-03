"""
DeadZone Heatmap Generator Module
Generates a 7x12 (84 cell) or 8x12 (96 cell) interpolated spatial matrix.
Matches the heatCells array required by the React frontend and Backend API.
"""
import math
from typing import List, Dict, Any

GRID_ROWS = 7
GRID_COLS = 12

def generate_heatmap_cells(
    map_points: List[Dict[str, Any]],
    measurements: List[Dict[str, Any]],
    rows: int = GRID_ROWS,
    cols: int = GRID_COLS
) -> List[int]:
    """
    Computes spatial heatmap values (0 to 100) using Inverse Distance Weighting (IDW).
    - map_points provides {id, x, y} coordinates (0 to 100 %).
    - measurements provides {point, rssi} signal readings.
    Returns 1D array of length rows * cols.
    """
    # Map points to signal strength
    lookup = {m["point"]: float(m["rssi"]) for m in measurements if "point" in m and "rssi" in m}
    sampled_points = []
    for p in map_points:
        pid = p.get("id")
        if pid in lookup:
            # Normalize RSSI (-90 dBm -> 0, -30 dBm -> 100)
            val = max(0.0, min(100.0, (lookup[pid] - (-90.0)) / (-30.0 - (-90.0)) * 100.0))
            sampled_points.append((float(p["x"]), float(p["y"]), val))

    # If no valid sampled points, return baseline default grid
    if not sampled_points:
        return [50] * (rows * cols)

    cells = []
    for r in range(rows):
        cy = (r + 0.5) / rows * 100.0
        for c in range(cols):
            cx = (c + 0.5) / cols * 100.0

            numerator = 0.0
            denominator = 0.0
            exact_match = None

            for px, py, pval in sampled_points:
                dist = math.hypot(cx - px, cy - py)
                if dist < 1.0:
                    exact_match = pval
                    break
                weight = 1.0 / (dist ** 2)
                numerator += weight * pval
                denominator += weight

            if exact_match is not None:
                val = int(round(exact_match))
            elif denominator > 0:
                val = int(round(numerator / denominator))
            else:
                val = 50

            cells.append(max(0, min(100, val)))

    return cells
