from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    location_area = Column(String, index=True)
    
