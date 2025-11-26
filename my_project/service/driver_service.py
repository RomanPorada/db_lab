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
