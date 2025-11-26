from my_project.dao import car_type_dao


class CarTypeNotFoundException(Exception):
    pass

class CarTypeExistsException(Exception):
    pass


def create_new_car_type(db, car_type_schema):
    return car_type_dao.create_car_type(db, car_type_schema)


def get_car_type_by_id(db, car_type_id: int):
    db_car_type = car_type_dao.get_car_type(db, car_type_id)
    if db_car_type is None:
        raise CarTypeNotFoundException("Car type not found")
    return db_car_type


def get_all_car_types_service(db, skip: int, limit: int):
    return car_type_dao.get_all_car_types(db, skip, limit)


def update_existing_car_type(db, car_type_id: int, car_type_update):
    db_car_type = get_car_type_by_id(db, car_type_id)
    return car_type_dao.update_car_type(db, db_car_type, car_type_update)


def delete_existing_car_type(db, car_type_id: int):
    db_car_type = get_car_type_by_id(db, car_type_id)
    car_type_dao.delete_car_type(db, db_car_type)
