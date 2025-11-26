from sqlalchemy import select
from my_project.domain.models import CarType


def get_car_type(db, car_type_id):
    query = select(CarType).where(CarType.car_type_id == car_type_id)
    return db.execute(query).scalars().first()


def get_all_car_types(db, skip=0, limit=100):
    query = select(CarType).offset(skip).limit(limit)
    return db.execute(query).scalars().all()


def create_car_type(db, car_type_schema):
    db_car_type = CarType(**car_type_schema.model_dump())
    db.add(db_car_type)
    db.commit()
    db.refresh(db_car_type)
    return db_car_type


def update_car_type(db, db_car_type, car_type_update):
    update_data = car_type_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_car_type, key, value)
    db.commit()
    db.refresh(db_car_type)
    return db_car_type


def delete_car_type(db, db_car_type):
    db.delete(db_car_type)
    db.commit()