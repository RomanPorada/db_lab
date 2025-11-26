from sqlalchemy import select
from my_project.domain.models import Car
from sqlalchemy.orm import Session

# Отримати конкретний автомобіль за driver_id і car_id
def get_car(db: Session, driver_id: int, car_id: int):
    query = select(Car).where(Car.driver_id == driver_id, Car.car_id == car_id)
    return db.execute(query).scalars().first()

# Отримати всі автомобілі
def get_all_cars(db: Session, skip: int = 0, limit: int = 100):
    query = select(Car).offset(skip).limit(limit)
    return db.execute(query).scalars().all()

# Створити новий автомобіль
def create_car(db: Session, car_schema):
    db_car = Car(**car_schema.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

# Оновити існуючий автомобіль
def update_car(db: Session, db_car, car_update):
    update_data = car_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car

# Видалити автомобіль
def delete_car(db: Session, db_car):
    db.delete(db_car)
    db.commit()


# М:1 - Отримати всі авто водія за його ID
def get_cars_by_driver_dao(db: Session, driver_id: int):
    query = select(Car).where(Car.driver_id == driver_id)
    return db.execute(query).scalars().all()


# М:1 - Отримати всі авто типу за ID типу
def get_cars_by_type_dao(db: Session, car_type_id: int):
    query = select(Car).where(Car.car_type_id == car_type_id)
    return db.execute(query).scalars().all()
