from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    surname: str
    phone: str
    email: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    user_id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class DriverBase(BaseModel):
    license_number: str
    experience_years: int


class DriverCreate(DriverBase):
    user_id: int


class DriverUpdate(BaseModel):
    license_number: Optional[str] = None
    experience_years: Optional[int] = None


class DriverResponse(DriverBase):
    user_id: int
    model_config = {"from_attributes": True}

class CarTypeBase(BaseModel):
    name: str
    seats: int
    description: Optional[str] = None


class CarTypeCreate(CarTypeBase):
    pass


class CarTypeUpdate(BaseModel):
    name: Optional[str] = None
    seats: Optional[int] = None
    description: Optional[str] = None


class CarTypeResponse(CarTypeBase):
    car_type_id: int
    model_config = {"from_attributes": True}

class CarBase(BaseModel):
    brand: str
    model: str
    plate_number: str
    year: Optional[int] = None
    car_type_id: int


class CarCreate(CarBase):
    driver_id: int
    car_id: int


class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    plate_number: Optional[str] = None
    year: Optional[int] = None
    car_type_id: Optional[int] = None


class CarResponse(CarBase):
    driver_id: int
    car_id: int
    model_config = {"from_attributes": True}

from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel
from typing import Optional

# ---------------- DRIVER SCHEMAS ----------------
class DriverCreateSchema(BaseModel):
    user_id: int
    license_number: str
    experience_years: Optional[int] = None

class DriverUpdateSchema(BaseModel):
    license_number: Optional[str] = None
    experience_years: Optional[int] = None

# ---------------- CAR SCHEMAS ----------------
class CarCreateSchema(BaseModel):
    driver_id: int
    car_id: int
    car_type_id: int
    brand: str
    model: str
    plate_number: str
    year: Optional[int] = None

class CarUpdateSchema(BaseModel):
    car_type_id: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    plate_number: Optional[str] = None
    year: Optional[int] = None
