# DeadZone — Module 03: Data Processing

## 👤 Module Information
- **Module Name:** `03_Data_Processing`
- **Responsible Member:** Member 3 (Data Processing Developer)
- **Git Branch:** `data-processing`
- **Technology Stack:** Python 3.12+, Pandas, NumPy, Pydantic, Pytest

---

## 🎯 Overview & Responsibilities
The Data Processing module is responsible for loading, sanitizing, validating, and transforming raw Wi-Fi survey measurements. It converts raw network telemetry into structured records, computes environmental health summaries, and generates the spatial heatmap matrix.

### Core Capabilities
1. **Data Ingestion (`data_loader.py`):** Loads measurement sets from CSV or JSON survey files.
2. **Data Cleaning & Filtering (`cleaner.py`):** Filters corrupt readings, handles missing values, sanitizes strings, and clamps RSSI between valid physical bounds (-105 dBm to -15 dBm).
3. **Data Validation (`validator.py`):** Enforces Pydantic schema validation on incoming telemetry before storage.
4. **Signal Classification (`transformer.py`):**
   - **Good:** $\text{RSSI} \ge -55\text{ dBm}$
   - **Watch:** $-67\text{ dBm} \le \text{RSSI} < -55\text{ dBm}$
   - **Weak / Dead Zone:** $\text{RSSI} < -67\text{ dBm}$
5. **Spatial Heatmap Generation (`heatmap_generator.py`):** Computes the 7×12 (84 cells) grid using Inverse Distance Weighting (IDW) interpolation from measured floor plan points.

---

## 🚀 Getting Started & Local Development

### Prerequisites
- Python 3.12+

### Installation
```bash
cd 03_Data_Processing
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Running Automated Tests
```bash
pytest test_data_processing.py -v
```

---

## 📂 File Structure & Modification Guide

### 🟢 Files You Are Expected to Modify
| File | Responsibility |
| :--- | :--- |
| `data_loader.py` | CSV/JSON survey readers and custom batch loaders. |
| `cleaner.py` | Outlier detection, noise reduction, and filtering logic. |
| `validator.py` | Telemetry schemas, field constraints, type validators. |
| `transformer.py` | Metric aggregation, summary statistics, normalization formulas. |
| `heatmap_generator.py` | Interpolation algorithms (IDW, Kriging, Gaussian smoothing). |
| `dataset/` | Reference datasets and calibration test files. |
| `test_data_processing.py` | Test cases verifying cleaning and transformation accuracy. |

### 🔴 Files That Should NOT Be Independently Modified
| File / Spec | Reason |
| :--- | :--- |
| RSSI Classification Thresholds (`-55`, `-67`) | Modifying these thresholds alters the definition of "Weak" across `01_Backend`, `02_Frontend`, and `04_Algorithms`. |
| Heatmap Grid Dimensions ($7 \times 12$) | The frontend CSS grid is specifically rendered as 7 rows by 12 columns. Changing grid dimensions requires frontend coordination. |
| Core Measurement Field Names | `point`, `rssi`, `latency`, `loss`, `throughput`, `channel` must remain consistent with the database and API. |

---

## 🤝 Dependencies on Other Modules
1. **Module 01 (Backend):** The backend calls `cleaner.py` and `validator.py` when saving new measurements from `/api/surveys/measurements` and uses `heatmap_generator.py` for `/api/surveys/active`.
2. **Module 02 (Frontend):** Consumes the generated 84-cell heatmap array and relies on status colors ('Good'/'Watch'/'Weak').
3. **Module 04 (Algorithms):** Receives cleaned and classified points to run dead zone graph clustering and AP optimization.
