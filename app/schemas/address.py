from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    street: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name must not be empty or whitespace")
        return value


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    street: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("name")
    @classmethod
    def name_not_blank_if_provided(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Name must not be empty or whitespace")
        return value



class AddressResponse(AddressBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)