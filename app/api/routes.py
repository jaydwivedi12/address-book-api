from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import get_db
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.services.address_service import AddressService

router = APIRouter(prefix="/api/v1/addresses", tags=["Addresses"])


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    try:
        return AddressService.create_address(db, address)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address",
        )


@router.get(
    "",
    response_model=List[AddressResponse],
)
def get_addresses(
    db: Session = Depends(get_db),
) -> List[AddressResponse]:
    return AddressService.get_all_addresses(db)


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    try:
        updated = AddressService.update_address(db, address_id, address)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        return updated
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address",
        )


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
) -> None:
    try:
        deleted = AddressService.delete_address(db, address_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address",
        )


@router.get(
    "/nearby",
    response_model=List[AddressResponse],
)
def find_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db),
) -> List[AddressResponse]:
    return AddressService.find_nearby_addresses(
        db=db,
        latitude=latitude,
        longitude=longitude,
        distance_km=distance_km,
    )