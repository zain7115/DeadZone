# DeadZone — Module 04: Algorithms

## 👤 Module Information
- **Module Name:** `04_Algorithms`
- **Responsible Member:** Member 4 (Algorithm Developer)
- **Git Branch:** `algorithms`
- **Technology Stack:** Python 3.12+, NetworkX, NumPy, Pytest (with C# DSA integration seam)

---

## 🎯 Overview & Responsibilities
The Algorithms module implements the core computational logic for DeadZone. It analyzes wireless coverage, detects and clusters contiguous physical dead zones, and executes multi-criteria graph optimization to recommend and rank optimal Access Point (AP) placement locations.

### Core Mathematical & Algorithmic Models
1. **Graph Representation (`graph.py`):** Represents floor plan survey points as vertices $V$ and traversable paths as weighted edges $E$. Implements **Dijkstra’s algorithm** to discover shortest paths between measurement coordinates.
2. **Dead Zone Detection (`deadzone_detector.py`):** Identifies points where $\text{RSSI} < -67\text{ dBm}$ and groups adjacent weak points into contiguous clusters using **Breadth-First Search (BFS)** connected component analysis.
3. **Coverage Analysis (`coverage_analyzer.py`):** Computes signal distribution, standard deviation, and health index.
4. **AP Placement Optimization (`ap_optimizer.py`):** Evaluates candidate AP locations using the project's multi-criteria scoring function:

$$\text{Score} = (0.4 \times \text{CoverageGap}) + (0.3 \times \text{MeasuredRSSI}) + (0.2 \times \text{ChannelOverlap}) + (0.1 \times \text{InstallConstraints})$$

---

## 🚀 Getting Started & Local Development

### Prerequisites
- Python 3.12+

### Installation
```bash
cd 04_Algorithms
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Running Automated Tests
```bash
pytest test_algorithms.py -v
```

---

## 📂 File Structure & Modification Guide

### 🟢 Files You Are Expected to Modify
| File | Responsibility |
| :--- | :--- |
| `ap_optimizer.py` | AP candidate selection logic, scoring criteria, and lift percentage estimation. |
| `deadzone_detector.py` | Dead zone clustering heuristics, severity classification, and boundary analysis. |
| `graph.py` | Graph representations, edge weighting methods, and pathfinding algorithms. |
| `coverage_analyzer.py` | Statistical signal distribution models and coverage scoring. |
| `models.py` | Algorithm dataclasses and entity schemas. |
| `test_algorithms.py` | Pytest test cases verifying algorithmic correctness and performance. |

### 🔴 Files That Should NOT Be Independently Modified
| File / Spec | Reason |
| :--- | :--- |
| `CandidateAP` Output Schema | Fields (`rank`, `label`, `score`, `lift`, `constraints`, `tone`, `graph_path`) are consumed directly by `01_Backend` and rendered by `02_Frontend`. |
| Algorithm Seam Endpoint (`POST /api/optimization/run`) | The input `{ coordinates: [...] }` and output schema must remain coordinated with the backend. |

---

## 🤝 Dependencies on Other Modules
1. **Module 01 (Backend):** The backend's `POST /api/optimization/run` endpoint directly calls `ap_optimizer.py` to obtain candidate rankings.
2. **Module 03 (Data Processing):** Supplies clean telemetry readings and signal classifications.
3. **Module 02 (Frontend):** Visualizes the ranked candidate cards, score bars, and traversal paths on the `/optimize` page.
