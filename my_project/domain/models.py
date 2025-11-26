from sqlalchemy import (
    Column, Integer, BigInteger, String, ForeignKey, TIMESTAMP, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from my_project.database import Base

# М:М junction table: Driver <-> CarType
driver_car_type = Table(
    'driver_car_type',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('drivers.user_id', ondelete='CASCADE'), primary_key=True),
    Column('car_type_id', BigInteger, ForeignKey('car_types.car_type_id', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    driver = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    cars = relationship("Car", secondary="drivers", back_populates="user", viewonly=True)


class Driver(Base):
    __tablename__ = 'drivers'

    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    license_number = Column(String(20), nullable=False, unique=True)
    experience_years = Column(Integer)

    user = relationship("User", back_populates="driver")
    cars = relationship("Car", back_populates="driver", cascade="all, delete-orphan")
    car_types = relationship("CarType", secondary=driver_car_type, back_populates="drivers")


class CarType(Base):
    __tablename__ = 'car_types'

    car_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    seats = Column(Integer, nullable=False)
    description = Column(String(100))

    cars = relationship("Car", back_populates="car_type", cascade="all, delete-orphan")
    drivers = relationship("Driver", secondary=driver_car_type, back_populates="car_types")


class Car(Base):
    __tablename__ = 'cars'

    car_id = Column(BigInteger, primary_key=True, autoincrement=True)
    driver_id = Column(BigInteger, ForeignKey('drivers.user_id', ondelete='CASCADE'), nullable=False)
    car_type_id = Column(BigInteger, ForeignKey('car_types.car_type_id', ondelete='CASCADE'), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    plate_number = Column(String(15), unique=True, nullable=False)
    year = Column(Integer)

    driver = relationship("Driver", back_populates="cars")
    car_type = relationship("CarType", back_populates="cars")
    user = relationship("User", secondary="drivers", back_populates="cars", viewonly=True)
