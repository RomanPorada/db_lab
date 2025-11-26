from sqlalchemy.orm import Session
from my_project.dao.car_dao import (
    get_car as dao_get_car,
    get_all_cars as dao_get_all_cars,
    create_car as dao_create_car,
    update_car as dao_update_car,
    delete_car as dao_delete_car,
)
from my_project.domain.schemas import CarCreateSchema, CarUpdateSchema

# Власні виключення
class CarNotFoundException(Exception):
    pass

class CarExistsException(Exception):
    pass

# Створення нового автомобіля
def create_new_car(db: Session, schema: CarCreateSchema):
    existing_car = dao_get_car(db, schema.driver_id, schema.car_id)
    if existing_car:
        raise CarExistsException("Car already exists")
    return dao_create_car(db, schema)

# Отримати автомобіль по car_id і driver_id (controller passes car_id then driver_id)
def get_car_by_id(db: Session, car_id: int, driver_id: int):
    car = dao_get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    return car

# Отримати всі автомобілі
def get_all_cars(db: Session, skip: int = 0, limit: int = 100):
    return dao_get_all_cars(db, skip=skip, limit=limit)

# Оновити автомобіль
def update_car(db: Session, car_id: int, driver_id: int, schema: CarUpdateSchema):
    car = dao_get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    return dao_update_car(db, car, schema)

# Видалити автомобіль
def delete_car(db: Session, car_id: int, driver_id: int):
    car = dao_get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    dao_delete_car(db, car)


# М:1 - Отримати всі авто водія
def get_cars_by_driver(db: Session, driver_id: int):
    """Get all cars for a specific driver"""
    from my_project.dao.car_dao import get_cars_by_driver_dao
    return get_cars_by_driver_dao(db, driver_id)


# М:1 - Отримати всі авто типу
def get_cars_by_type(db: Session, car_type_id: int):
    """Get all cars of a specific type"""
    from my_project.dao.car_dao import get_cars_by_type_dao
    return get_cars_by_type_dao(db, car_type_id)
