"""
Контролер для SQL процедур та функцій
Всі процедури в одному файлі, як просили
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import BaseModel, ValidationError

from my_project.database import get_db
from my_project.service import procedures_service
from my_project.service.procedures_service import ProcedureException


procedures_bp = Blueprint("procedures", __name__, url_prefix="/procedures")


# ============= REQUEST SCHEMAS =============

class AddUserRequest(BaseModel):
    name: str
    surname: str
    phone: str
    email: str = None


class LinkDriverRouteRequest(BaseModel):
    name: str
    surname: str
    start: str  # start_location
    end: str    # end_location


class SplitTableRequest(BaseModel):
    table_name: str


# ============= DECORATOR =============

def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(db, *args, **kwargs)
        finally:
            try:
                db.close()
            except Exception:
                # Ігноруємо помилки при закритті після raw cursor операцій
                pass
    wrapper.__name__ = f.__name__
    return wrapper


# ============= PROCEDURES ENDPOINTS =============

@procedures_bp.route("/sp_add_user", methods=["POST"])
@with_db_session
def add_user_endpoint(db: Session):
    """
    Викликає процедуру sp_add_user
    Додає нового користувача в БД
    """
    try:
        schema = AddUserRequest.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        result = procedures_service.add_user(db, schema.name, schema.surname, schema.phone, schema.email)
        return jsonify(result), 201
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400


@procedures_bp.route("/sp_link_driver_route_by_names", methods=["POST"])
@with_db_session
def link_driver_route_endpoint(db: Session):
    """
    Викликає процедуру sp_link_driver_route_by_names
    Зв'язує водія з маршрутом за іменами
    """
    try:
        schema = LinkDriverRouteRequest.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        result = procedures_service.link_driver_route_by_names(
            db, schema.name, schema.surname, schema.start, schema.end
        )
        return jsonify(result), 201
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400


@procedures_bp.route("/sp_insert_noname_package", methods=["POST"])
@with_db_session
def insert_noname_package_endpoint(db: Session):
    """
    Викликає процедуру sp_insert_noname_package
    Додає 10 анонімних користувачів в БД
    """
    try:
        result = procedures_service.insert_noname_package(db)
        return jsonify(result), 201
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400


@procedures_bp.route("/sp_show_trip_stats", methods=["GET"])
@with_db_session
def show_trip_stats_endpoint(db: Session):
    """
    Викликає процедуру sp_show_trip_stats
    Повертає статистику поїздок (кількість, max, min, avg, sum ціни)
    """
    try:
        result = procedures_service.get_trip_stats(db)
        return jsonify(result), 200
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400


@procedures_bp.route("/sp_split_table_random", methods=["POST"])
@with_db_session
def split_table_random_endpoint(db: Session):
    """
    Викликає процедуру sp_split_table_random
    Розділяє таблицю на дві нові таблиці випадково
    """
    try:
        schema = SplitTableRequest.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        result = procedures_service.split_table_random(db, schema.table_name)
        return jsonify(result), 201
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400


# ============= FUNCTIONS ENDPOINTS =============

@procedures_bp.route("/fn_trip_price_stat/<function_type>", methods=["GET"])
@with_db_session
def trip_price_stat_endpoint(db: Session, function_type: str):
    """
    Викликає функцію fn_trip_price_stat
    Параметр function_type: MAX, MIN, AVG, SUM
    """
    try:
        result = procedures_service.get_trip_price_stat(db, function_type)
        return jsonify(result), 200
    except ProcedureException as e:
        return jsonify({"error": str(e)}), 400
