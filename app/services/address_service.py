import logging
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from geopy.distance import geodesic

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)


class AddressService:

    @staticmethod
    def create_address(db: Session, data: AddressCreate) -> Address:
        logger.info("Creating address: name=%s", data.name)

        address = Address(**data.model_dump())

        try:
            db.add(address)
            db.commit()
            db.refresh(address)
            logger.info("Address created successfully with id=%s", address.id)
            return address
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while creating address")
            raise

    @staticmethod
    def get_all_addresses(db: Session) -> List[Address]:
        logger.info("Fetching all addresses")
        return db.query(Address).all()

    @staticmethod
    def update_address(db: Session, address_id: int, data: AddressUpdate) -> Address | None:
        logger.info("Updating address id=%s", address_id)

        address = db.query(Address).filter(Address.id == address_id).first()

        if not address:
            logger.warning("Address id=%s not found for update", address_id)
            return None

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(address, key, value)

        try:
            db.commit()
            db.refresh(address)
            logger.info("Address id=%s updated successfully", address_id)
            return address
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while updating address id=%s", address_id)
            raise

    @staticmethod
    def delete_address(db: Session, address_id: int) -> bool:
        logger.info("Deleting address id=%s", address_id)

        address = db.query(Address).filter(Address.id == address_id).first()

        if not address:
            logger.warning("Address id=%s not found for deletion", address_id)
            return False

        try:
            db.delete(address)
            db.commit()
            logger.info("Address id=%s deleted successfully", address_id)
            return True
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while deleting address id=%s", address_id)
            raise

    @staticmethod
    def find_nearby_addresses(
        db: Session,
        latitude: float,
        longitude: float,
        distance_km: float,
    ) -> List[Address]:

        logger.info(
            "Searching nearby addresses within %s km from (%s, %s)",
            distance_km,
            latitude,
            longitude,
        )

        all_addresses = db.query(Address).all()

        origin = (latitude, longitude)
        nearby = []

        for address in all_addresses:
            target = (address.latitude, address.longitude)
            if geodesic(origin, target).km <= distance_km:
                nearby.append(address)

        logger.info("Found %s nearby addresses", len(nearby))
        return nearby