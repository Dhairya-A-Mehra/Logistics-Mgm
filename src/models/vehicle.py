from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from ..database import Base


class Vehicle(Base):
    """Vehicle model for fleet management"""
    __tablename__ = "vehicles"
    __table_args__ = {"schema": "public"}
    
    vehicle_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    vehicle_type = Column(String)
    capacity_kg = Column(Numeric)
    capacity_volume_cm3 = Column(Numeric)
    fuel_type = Column(String)
    status = Column(String)
    
    def __repr__(self):
        return f"<Vehicle(type={self.vehicle_type}, status={self.status})>"
