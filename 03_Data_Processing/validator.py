"""
DeadZone Data Validation Module
Validates incoming Wi-Fi measurement fields and types.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator

class WiFIReadingSchema(BaseModel):
    id: Optional[str] = None
    point: str = Field(..., min_length=1, description="Identifier for survey pin, e.g. P-041")
    zone: str = Field(default="Unknown zone", description="Indoor zone or room label")
    rssi: float = Field(..., ge=-105.0, le=-15.0, description="Received Signal Strength Indicator in dBm")
    latency: float = Field(default=0.0, ge=0.0, le=2000.0, description="Round trip time latency in ms")
    loss: float = Field(default=0.0, ge=0.0, le=100.0, description="Packet loss percentage")
    throughput: float = Field(default=0.0, ge=0.0, le=1000.0, description="Download throughput in Mbps")
    channel: str = Field(default="auto", description="Wi-Fi channel and frequency band")
    status: Optional[str] = None

    @validator("point")
    def validate_point_format(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Measurement point cannot be empty.")
        return v

def validate_record(record: Dict[str, Any]) -> WiFIReadingSchema:
    """Validate a single dictionary record against schema."""
    return WiFIReadingSchema(**record)

def validate_dataset(records: List[Dict[str, Any]]) -> List[WiFIReadingSchema]:
    """Validate a list of records, returning validated objects or raising ValidationError."""
    return [validate_record(r) for r in records]
