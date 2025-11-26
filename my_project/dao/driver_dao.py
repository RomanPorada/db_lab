from sqlalchemy import select
from my_project.domain.models import Driver


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