from sqlalchemy import select
from my_project.domain.models import Driver, Car, CarType, driver_car_type


def get_driver(db, user_id):
    query = select(Driver).where(Driver.user_id == user_id)
    return db.execute(query).scalars().first()


def get_all_drivers(db, skip=0, limit=100):
    query = select(Driver).offset(skip).limit(limit)
    return db.execute(query).scalars().all()


def create_driver(db, driver_schema):
    db_driver = Driver(**driver_schema.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def update_driver(db, db_driver, driver_update):
    update_data = driver_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_driver, key, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def delete_driver(db, db_driver):
    db.delete(db_driver)
    db.commit()


def get_driver_cars_dao(db, driver_id: int):
    """Get all cars for a specific driver"""
    query = select(Car).where(Car.driver_id == driver_id)
    return db.execute(query).scalars().all()


def get_driver_car_types_dao(db, driver_id: int):
    """Get all car types that a driver can work with (M:M)"""
    query = select(CarType).join(driver_car_type).where(driver_car_type.c.user_id == driver_id)
    return db.execute(query).scalars().all()


def add_driver_car_type_dao(db, driver_id: int, car_type_id: int):
    """Add a car type to a driver's allowed types (M:M)"""
    driver = db.execute(select(Driver).where(Driver.user_id == driver_id)).scalars().first()
    car_type = db.execute(select(CarType).where(CarType.car_type_id == car_type_id)).scalars().first()
    if not driver or not car_type:
        raise Exception("Driver or CarType not found")
    if car_type not in driver.car_types:
        driver.car_types.append(car_type)
        db.commit()


def remove_driver_car_type_dao(db, driver_id: int, car_type_id: int):
    """Remove a car type from a driver's allowed types (M:M)"""
    driver = db.execute(select(Driver).where(Driver.user_id == driver_id)).scalars().first()
    car_type = db.execute(select(CarType).where(CarType.car_type_id == car_type_id)).scalars().first()
    if not driver or not car_type:
        raise Exception("Driver or CarType not found")
    if car_type in driver.car_types:
        driver.car_types.remove(car_type)
        db.commit()