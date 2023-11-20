from typing import Optional

from pydantic import BaseModel


# Shared properties
class LocationBase(BaseModel):
    location_name: Optional[str] = None
    location_area: Optional[str] = None


# Properties to receive on Location creation
class LocationCreate(LocationBase):
    location_name: str
    location_area: str


# Properties to receive on Location update
class LocationUpdate(LocationBase):
    pass


# Properties shared by models stored in DB
class LocationInDBBase(LocationBase):
    id: int
    location_name: str
    location_area: str

    class Config:
        orm_mode = True


# Properties to return to client
class Location(LocationInDBBase):
    pass


# Properties properties stored in DB
class LocationInDB(LocationInDBBase):
    pass
