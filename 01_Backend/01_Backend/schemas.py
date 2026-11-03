"""
DeadZone Pydantic Request & Response Schemas
Matches exact JSON contract consumed by React Frontend.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class MeasurementBase(BaseModel):
    point: str
    zone: Optional[str] = "Unknown zone"
    rssi: float
    latency: Optional[float] = 0.0
    loss: Optional[float] = 0.0
    throughput: Optional[float] = 0.0
    channel: Optional[str] = "auto"

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementResponse(MeasurementBase):
    id: str
    status: str

    class Config:
        from_attributes = True

class MapPointResponse(BaseModel):
    id: str
    x: int
    y: int
    tone: str
    zone: str

    class Config:
        from_attributes = True

class ActiveSurveyResponse(BaseModel):
    surveyId: str
    building: str
    floor: str
    measurements: List[MeasurementResponse]
    heatCells: List[int]
    pointsTotal: int
    pointsSampled: int

class CoordinatePoint(BaseModel):
    id: str
    x: int
    y: int

class OptimizationRequest(BaseModel):
    coordinates: Optional[List[CoordinatePoint]] = []

class OptimizationCandidate(BaseModel):
    rank: str
    label: str
    zone: str
    score: int
    lift: str
    constraints: str
    tone: str
    graphPath: List[str]
    algorithm: str

class OptimizationResponse(BaseModel):
    status: str
    engine: str
    inputPoints: int
    candidates: List[OptimizationCandidate]
    meta: dict
