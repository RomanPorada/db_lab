from sqlalchemy.orm import Session
from my_project.dao.car_dao import (
    get_car,
    get_all_cars,
    create_car,
    update_car,
    delete_car
)
from my_project.domain.schemas import CarCreateSchema, CarUpdateSchema

# Власні виключення
class CarNotFoundException(Exception):
    pass

class CarExistsException(Exception):
    pass

# Створення нового автомобіля
def create_new_car(db: Session, schema: CarCreateSchema):
    existing_car = get_car(db, schema.driver_id, schema.car_id)
    if existing_car:
        raise CarExistsException("Car already exists")
    return create_car(db, schema)

# Отримати автомобіль по driver_id і car_id
def get_car_by_id(db: Session, driver_id: int, car_id: int):
    car = get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    return car

# Отримати всі автомобілі
def get_all_cars_service(db: Session, skip: int = 0, limit: int = 100):
    return get_all_cars(db, skip=skip, limit=limit)

# Оновити автомобіль
def update_existing_car(db: Session, driver_id: int, car_id: int, schema: CarUpdateSchema):
    car = get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    return update_car(db, car, schema)

# Видалити автомобіль
def delete_existing_car(db: Session, driver_id: int, car_id: int):
    car = get_car(db, driver_id, car_id)
    if not car:
        raise CarNotFoundException("Car not found")
    delete_car(db, car)
