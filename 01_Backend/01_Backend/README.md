# DeadZone — Module 01: Backend

## 👤 Module Information
- **Module Name:** `01_Backend`
- **Responsible Member:** Member 1 (Backend Developer)
- **Git Branch:** `backend`
- **Technology Stack:**
  - **Python / FastAPI:** FastAPI, SQLAlchemy, SQLite, Pydantic, Uvicorn
  - **Node.js / Express:** Node.js, Express, CORS (Preserved MVP skeleton)

---

## 🎯 Overview & Responsibilities
The Backend module provides the core data persistence and REST API services for DeadZone. It connects the user actions from the Frontend (`02_Frontend`) with the database and provides integration seams for Data Processing (`03_Data_Processing`) and Algorithms (`04_Algorithms`).

### Preserved Implementations
1. **Existing MVP Backend (`server.js`):** The original Express server that connects seamlessly with the React frontend on port `5000`.
2. **Production FastAPI Backend (`main.py`):** The academic-standard Python FastAPI implementation backed by SQLite and SQLAlchemy as specified in the project documentation and proposal.

---

## 🚀 Getting Started & Local Development

### Option A: Running the FastAPI Backend (Recommended)
1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the FastAPI server on port 5000:**
   ```bash
   uvicorn main:app --reload --port 5000
   ```
4. **Access interactive API docs:**
   - Swagger UI: `http://localhost:5000/docs`
   - ReDoc: `http://localhost:5000/redoc`

### Option B: Running the Existing Express MVP Backend
```bash
npm install
node server.js
```
Runs at: `http://localhost:5000`

---

## 🧪 Running Automated Tests
Run unit tests for all endpoints using pytest:
```bash
pytest test_backend.py -v
```

---

## 📡 API Endpoints Contract

All endpoints run on port `5000` under the `/api` prefix (matched with the Vite proxy in `02_Frontend`):

| Method | Endpoint | Description | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Backend status check | None | `{ status: 'ok', server: 'deadzone-backend', version: '0.1.0' }` |
| `GET` | `/api/surveys/active` | Get active survey, points, heat cells | None | `ActiveSurveyResponse` object |
| `POST` | `/api/surveys/measurements` | Append new signal measurement | `MeasurementCreate` JSON | `{ status: 'success', measurement: ... }` |
| `GET` | `/api/surveys/map-points` | Get 5 core floor-plan coordinate points | None | `{ points: [ { id, x, y, tone, zone }, ... ] }` |
| `POST` | `/api/optimization/run` | Run AP ranking algorithm | `{ coordinates: [...] }` | `OptimizationResponse` with ranked candidates |

---

## 📂 File Structure & Modification Guide

### 🟢 Files You Are Expected to Modify
| File | Responsibility |
| :--- | :--- |
| `main.py` | FastAPI route handlers and middleware. |
| `models.py` | SQLAlchemy database models (`SurveyModel`, `MeasurementModel`, `MapPointModel`). |
| `schemas.py` | Pydantic request and response schemas. |
| `services.py` | Business logic, calculations, and algorithm service hooks. |
| `database.py` | Database session and SQLite engine configuration. |
| `config.py` | Environment settings and port configurations. |
| `test_backend.py` | Pytest test cases. |

### 🔴 Files That Should NOT Be Independently Modified
*Modifications to these require coordination across the team:*
| File | Reason |
| :--- | :--- |
| API Route Names & Request Bodies | Changing `/api/surveys/...` or field names breaks `02_Frontend`. |
| Port Number (`5000`) | The frontend proxy in `02_Frontend\vite.config.ts` specifically targets port `5000`. |
| `server.js` | Preserved reference skeleton for Node/Express compatibility. |

---

## 🤝 Dependencies on Other Modules
1. **Module 02 (Frontend):** Consumes all `/api/*` endpoints. Keep response JSON structure strictly compliant.
2. **Module 03 (Data Processing):** Provides data cleaning and validation logic to be called before saving measurements.
3. **Module 04 (Algorithms):** Provides the AP placement optimization algorithm (`ap_optimizer.py`) to replace the mock response in `POST /api/optimization/run`.
