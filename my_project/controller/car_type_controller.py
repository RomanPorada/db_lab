from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session
from my_project.database import get_db

from my_project.service import car_type_service
from my_project.service.car_type_service import (
    CarTypeNotFoundException,
    CarTypeExistsException
)

from my_project.domain.schemas import (
    CarTypeCreate,
    CarTypeUpdate,
    CarTypeResponse
)
from my_project.domain.schemas import CarResponse

car_type_bp = Blueprint("car_types", __name__, url_prefix="/car-types")

def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper


@car_type_bp.route("/", methods=["POST"])
@with_db_session
def create_car_type_endpoint(db: Session):
    try:
        schema = CarTypeCreate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        new_car_type = car_type_service.create_new_car_type(db, schema)
        return jsonify(CarTypeResponse.model_validate(new_car_type).model_dump()), 201
    except CarTypeExistsException as e:
        return jsonify({"error": str(e)}), 409


@car_type_bp.route("/", methods=["GET"])
@with_db_session
def get_car_types_endpoint(db: Session):
    car_types = car_type_service.get_all_car_types_service(db, 0, 100)
    return jsonify([CarTypeResponse.model_validate(ct).model_dump() for ct in car_types]), 200


@car_type_bp.route("/<int:type_id>", methods=["GET"])
@with_db_session
def get_car_type_endpoint(db: Session, type_id: int):
    try:
        car_type = car_type_service.get_car_type_by_id(db, type_id)
        return jsonify(CarTypeResponse.model_validate(car_type).model_dump()), 200
    except CarTypeNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@car_type_bp.route("/<int:type_id>", methods=["PUT"])
@with_db_session
def update_car_type_endpoint(db: Session, type_id: int):
    try:
        schema = CarTypeUpdate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        updated = car_type_service.update_existing_car_type(db, type_id, schema)
        return jsonify(CarTypeResponse.model_validate(updated).model_dump()), 200
    except CarTypeNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@car_type_bp.route("/<int:type_id>", methods=["DELETE"])
@with_db_session
def delete_car_type_endpoint(db: Session, type_id: int):
    try:
        car_type_service.delete_existing_car_type(db, type_id)
        return jsonify({"message": "car type deleted"}), 200
    except CarTypeNotFoundException as e:
        return jsonify({"error": str(e)}), 404


# М:1 - Отримати всі авто конкретного типу
@car_type_bp.route("/<int:car_type_id>/cars", methods=["GET"])
@with_db_session
def get_car_type_cars_endpoint(db: Session, car_type_id: int):
    """Get all cars of a specific type"""
    try:
        cars = car_type_service.get_car_type_cars(db, car_type_id)
        result = [CarResponse.model_validate(car).model_dump() for car in cars]
        return jsonify(result), 200
    except CarTypeNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

