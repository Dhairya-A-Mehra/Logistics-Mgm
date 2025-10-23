from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from ..database import Base


class Warehouse(Base):
    """Warehouse model for storing warehouse locations"""
    __tablename__ = "warehouses"
    __table_args__ = {"schema": "public"}
    
    warehouse_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    region = Column(String)
    
    def __repr__(self):
        return f"<Warehouse(name={self.name}, region={self.region})>"
