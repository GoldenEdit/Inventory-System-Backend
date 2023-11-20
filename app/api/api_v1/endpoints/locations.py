from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Location])
def read_locations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve locations.
    """
    locations = crud.location.get(
        db=db, skip=skip, limit=limit
    )
    return locations


@router.post("/", response_model=schemas.Location)
def create_location(
    *,
    db: Session = Depends(deps.get_db),
    location_in: schemas.LocationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new location.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    location = crud.location.create(db=db, obj_in=location_in)
    return location


@router.put("/{id}", response_model=schemas.Location)
def update_location(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    location_in: schemas.LocationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a location.
    """
    location = crud.location.get(db=db, id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    location = crud.location.update(db=db, db_obj=location, obj_in=location_in)
    return location


@router.get("/{id}", response_model=schemas.Location)
def read_location(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get location by ID.
    """
    location = crud.location.get(db=db, id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.delete("/{id}", response_model=schemas.Location)
def delete_location(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a location.
    """
    location = crud.location.get(db=db, id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    location = crud.location.remove(db=db, id=id)
    return location
