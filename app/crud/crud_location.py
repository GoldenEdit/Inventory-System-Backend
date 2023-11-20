from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def create(
        self, db: Session, *, obj_in: LocationCreate
    ) -> Location:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Location]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )


location = CRUDLocation(Location)
