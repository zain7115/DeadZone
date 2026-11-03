"""
DeadZone Coverage & Signal Strength Analysis Module
Calculates distribution, coverage index, and identifies high-risk areas.
"""
from typing import List, Dict, Any
import statistics

class CoverageAnalyzer:
    @staticmethod
    def analyze_coverage(measurements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates signal distribution, variance, and overall health metrics.
        """
        if not measurements:
            return {"status": "empty", "coverageIndex": 0}

        rssi_list = [float(m["rssi"]) for m in measurements if "rssi" in m]
        if not rssi_list:
            return {"status": "no_rssi", "coverageIndex": 0}

        mean_rssi = statistics.mean(rssi_list)
        stdev_rssi = statistics.stdev(rssi_list) if len(rssi_list) > 1 else 0.0

        good_count = sum(1 for r in rssi_list if r >= -55.0)
        watch_count = sum(1 for r in rssi_list if -67.0 <= r < -55.0)
        weak_count = sum(1 for r in rssi_list if r < -67.0)

        # Coverage index 0 - 100
        coverage_index = int(max(0, min(100, (mean_rssi - (-90.0)) / (-30.0 - (-90.0)) * 100.0)))

        return {
            "totalPoints": len(rssi_list),
            "meanRSSI": round(mean_rssi, 1),
            "stdevRSSI": round(stdev_rssi, 2),
            "distribution": {
                "good": good_count,
                "watch": watch_count,
                "weak": weak_count
            },
            "coverageIndex": coverage_index,
            "overallQuality": "Healthy" if coverage_index >= 75 else "Borderline" if coverage_index >= 55 else "Poor"
        }
