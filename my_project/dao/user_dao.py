from sqlalchemy import select
from my_project.domain.models import User

def get_user(db, user_id: int):
    query = select(User).where(User.user_id == user_id)
    return db.scalars(query).first()

def get_user_by_phone(db, phone: str):
    query = select(User).where(User.phone == phone)
    return db.scalars(query).first()

def get_all_users(db, skip: int = 0, limit: int = 100):
    query = select(User).offset(skip).limit(limit)
    return db.scalars(query).all()

def create_user(db, user_schema):
    user_data = user_schema.model_dump()
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db, db_user, user_update):
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db, db_user):
    db.delete(db_user)
    db.commit()