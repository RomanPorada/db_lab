from sqlalchemy.orm import Session
from my_project.dao.driver_dao import (
    get_driver,
    get_all_drivers,
    create_driver,
    update_driver,
    delete_driver
)
from my_project.domain.schemas import DriverCreateSchema, DriverUpdateSchema

# Власні виключення
class DriverNotFoundException(Exception):
    pass

class DriverExistsException(Exception):
    pass

# Створення нового водія
def create_new_driver(db: Session, schema: DriverCreateSchema):
    # Перевірка чи водій вже існує (по user_id)
    existing_driver = get_driver(db, schema.user_id)
    if existing_driver:
        raise DriverExistsException("Driver already exists")
    return create_driver(db, schema)

# Отримати водія по user_id
def get_driver_by_id(db: Session, user_id: int):
    driver = get_driver(db, user_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return driver

# Отримати всіх водіїв
def get_all_drivers_service(db: Session, skip: int = 0, limit: int = 100):
    return get_all_drivers(db, skip=skip, limit=limit)

# Оновити водія
def update_existing_driver(db: Session, user_id: int, schema: DriverUpdateSchema):
    driver = get_driver(db, user_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return update_driver(db, driver, schema)

# Видалити водія
def delete_existing_driver(db: Session, user_id: int):
    driver = get_driver(db, user_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    delete_driver(db, driver)


# М:1 - Отримати всі авто конкретного водія
def get_driver_cars(db: Session, driver_id: int):
    """Get all cars for a specific driver"""
    from my_project.dao.driver_dao import get_driver_cars_dao
    driver = get_driver(db, driver_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return get_driver_cars_dao(db, driver_id)


# М:М - Отримати всі типи авто для водія
def get_driver_car_types(db: Session, driver_id: int):
    """Get all car types that a driver can work with"""
    from my_project.dao.driver_dao import get_driver_car_types_dao
    driver = get_driver(db, driver_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return get_driver_car_types_dao(db, driver_id)


# М:М - Додати тип авто водієві
def add_driver_car_type(db: Session, driver_id: int, car_type_id: int):
    """Add a car type to a driver's allowed types"""
    from my_project.dao.driver_dao import add_driver_car_type_dao
    driver = get_driver(db, driver_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return add_driver_car_type_dao(db, driver_id, car_type_id)


# М:М - Видалити тип авто у водія
def remove_driver_car_type(db: Session, driver_id: int, car_type_id: int):
    """Remove a car type from a driver's allowed types"""
    from my_project.dao.driver_dao import remove_driver_car_type_dao
    driver = get_driver(db, driver_id)
    if not driver:
        raise DriverNotFoundException("Driver not found")
    return remove_driver_car_type_dao(db, driver_id, car_type_id)
