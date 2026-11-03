"""
DeadZone Backend — FastAPI Application
Preserves exact endpoints, request/response formats, and status codes.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import settings
from database import engine, Base, get_db
import models
import schemas
import services

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="DeadZone Wi-Fi Coverage Intelligence Backend API"
)

# CORS middleware to support Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    services.seed_initial_data(db)

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "server": "deadzone-backend", "version": settings.VERSION}

@app.get("/api/surveys/active", response_model=schemas.ActiveSurveyResponse)
def get_active_survey(db: Session = Depends(get_db)):
    """Return the current survey state — measurements + heat cells."""
    survey = db.query(models.SurveyModel).filter(models.SurveyModel.id == "DZ-2026-10-14").first()
    if not survey:
        raise HTTPException(status_code=404, detail="Active survey not found")

    measurements = db.query(models.MeasurementModel).filter(
        models.MeasurementModel.survey_id == "DZ-2026-10-14"
    ).all()

    return schemas.ActiveSurveyResponse(
        surveyId=survey.id,
        building=survey.building,
        floor=survey.floor,
        measurements=measurements,
        heatCells=services.DEFAULT_HEAT_CELLS,
        pointsTotal=survey.points_total,
        pointsSampled=len(measurements)
    )

@app.post("/api/surveys/measurements", status_code=status.HTTP_201_CREATED)
def add_survey_measurement(
    measurement: schemas.MeasurementCreate,
    db: Session = Depends(get_db)
):
    """Append a new measurement reading to the database."""
    if not measurement.point or measurement.rssi is None:
        raise HTTPException(status_code=400, detail="point and rssi are required fields.")

    new_measurement = services.add_measurement(db, measurement)
    return {
        "status": "success",
        "measurement": schemas.MeasurementResponse.from_orm(new_measurement)
    }

@app.get("/api/surveys/map-points")
def get_map_points(db: Session = Depends(get_db)):
    """Return core coordinate map points (P-037 to P-041)."""
    points = db.query(models.MapPointModel).all()
    return {"points": [schemas.MapPointResponse.from_orm(p) for p in points]}

@app.post("/api/optimization/run", response_model=schemas.OptimizationResponse)
def run_ap_optimization(payload: schemas.OptimizationRequest):
    """
    Accept floor plan coordinates and run AP candidate ranking.
    Simulates graph traversal and weighted scoring.
    """
    coords = payload.coordinates or []
    candidates = services.run_optimization(coords)
    return schemas.OptimizationResponse(
        status="completed",
        engine="dsa-graph-traversal",
        inputPoints=len(coords),
        candidates=candidates,
        meta={
            "note": "Integration seam with Module 04 (Algorithms)",
            "weights": {
                "coverageGap": 0.4,
                "measuredRSSI": 0.3,
                "channelOverlap": 0.2,
                "installConstraints": 0.1
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
