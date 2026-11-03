"""
DeadZone SQLAlchemy Database Models
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class SurveyModel(Base):
    __tablename__ = "surveys"

    id = Column(String, primary_key=True, index=True)
    building = Column(String, default="North Block")
    floor = Column(String, default="2nd floor")
    points_total = Column(Integer, default=48)

    measurements = relationship("MeasurementModel", back_populates="survey")

class MeasurementModel(Base):
    __tablename__ = "measurements"

    id = Column(String, primary_key=True, index=True)
    survey_id = Column(String, ForeignKey("surveys.id"), default="DZ-2026-10-14")
    point = Column(String, nullable=False, index=True)
    zone = Column(String, default="Unknown zone")
    rssi = Column(Float, nullable=False)
    latency = Column(Float, default=0.0)
    loss = Column(Float, default=0.0)
    throughput = Column(Float, default=0.0)
    channel = Column(String, default="auto")
    status = Column(String, default="Good")

    survey = relationship("SurveyModel", back_populates="measurements")

class MapPointModel(Base):
    __tablename__ = "map_points"

    id = Column(String, primary_key=True, index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    tone = Column(String, default="good")
    zone = Column(String, default="Unknown")
