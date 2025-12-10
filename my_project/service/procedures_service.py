"""
Сервіс для SQL процедур та функцій
"""
from sqlalchemy.orm import Session
from my_project.dao.procedures_dao import (
    call_sp_add_user,
    call_sp_link_driver_route_by_names,
    call_sp_insert_noname_package,
    call_sp_show_trip_stats,
    call_sp_split_table_random,
    call_fn_trip_price_stat
)


class ProcedureException(Exception):
    pass


# ============= ПРОЦЕДУРИ =============

def add_user(db: Session, name: str, surname: str, phone: str, email: str):
    """Добавити користувача через процедуру"""
    try:
        return call_sp_add_user(db, name, surname, phone, email)
    except Exception as e:
        raise ProcedureException(f"Error adding user: {str(e)}")


def link_driver_route_by_names(db: Session, name: str, surname: str, start: str, end: str):
    """Зв'язати водія з маршрутом за іменами"""
    try:
        return call_sp_link_driver_route_by_names(db, name, surname, start, end)
    except Exception as e:
        raise ProcedureException(f"Error linking driver to route: {str(e)}")


def insert_noname_package(db: Session):
    """Вставити 10 анонімних користувачів"""
    try:
        return call_sp_insert_noname_package(db)
    except Exception as e:
        raise ProcedureException(f"Error inserting noname package: {str(e)}")


def get_trip_stats(db: Session):
    """Отримати статистику поїздок"""
    try:
        return call_sp_show_trip_stats(db)
    except Exception as e:
        raise ProcedureException(f"Error getting trip stats: {str(e)}")


def split_table_random(db: Session, parent_table: str):
    """Розділити таблицю випадково"""
    try:
        return call_sp_split_table_random(db, parent_table)
    except Exception as e:
        raise ProcedureException(f"Error splitting table: {str(e)}")


# ============= ФУНКЦІЇ =============

def get_trip_price_stat(db: Session, function_type: str):
    """Отримати статистику ціни поїздок (MAX, MIN, AVG, SUM)"""
    allowed_functions = ['MAX', 'MIN', 'AVG', 'SUM']
    if function_type.upper() not in allowed_functions:
        raise ProcedureException(f"Invalid function type. Allowed: {', '.join(allowed_functions)}")
    
    try:
        return call_fn_trip_price_stat(db, function_type.upper())
    except Exception as e:
        raise ProcedureException(f"Error getting trip price stat: {str(e)}")
