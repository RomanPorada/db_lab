from my_project.dao import user_dao


class UserNotFoundException(Exception):
    pass


class UserExistsException(Exception):
    pass


def create_new_user(db, user_schema):
    existing_user = user_dao.get_user_by_phone(db, user_schema.phone)
    if existing_user:
        raise UserExistsException("User with this phone already exists")

    return user_dao.create_user(db, user_schema)


def get_user_by_id(db, user_id: int):
    db_user = user_dao.get_user(db, user_id)
    if db_user is None:
        raise UserNotFoundException("User not found")
    return db_user


def get_all_users_service(db, skip: int, limit: int):
    return user_dao.get_all_users(db, skip, limit)


def update_existing_user(db, user_id: int, user_update):
    db_user = get_user_by_id(db, user_id)
    return user_dao.update_user(db, db_user, user_update)


def delete_existing_user(db, user_id: int):
    db_user = get_user_by_id(db, user_id)
    user_dao.delete_user(db, db_user)
