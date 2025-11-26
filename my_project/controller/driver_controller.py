from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session
from my_project.database import get_db

from my_project.service import driver_service
from my_project.service.driver_service import DriverNotFoundException, DriverExistsException

from my_project.domain.schemas import DriverCreate, DriverUpdate, DriverResponse
from my_project.domain.schemas import CarResponse

driver_bp = Blueprint("drivers", __name__, url_prefix="/drivers")


def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper


@driver_bp.route("/", methods=["POST"])
@with_db_session
def create_driver_endpoint(db: Session):
    try:
        schema = DriverCreate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        new_driver = driver_service.create_new_driver(db, schema)
        return jsonify(DriverResponse.model_validate(new_driver).model_dump()), 201
    except DriverExistsException as e:
        return jsonify({"error": str(e)}), 409


@driver_bp.route("/", methods=["GET"])
@with_db_session
def get_drivers_endpoint(db: Session):
    drivers = driver_service.get_all_drivers_service(db, 0, 100)
    return jsonify([DriverResponse.model_validate(d).model_dump() for d in drivers]), 200


@driver_bp.route("/<int:driver_id>", methods=["GET"])
@with_db_session
def get_driver_endpoint(db: Session, driver_id: int):
    try:
        driver = driver_service.get_driver_by_id(db, driver_id)
        return jsonify(DriverResponse.model_validate(driver).model_dump()), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@driver_bp.route("/<int:driver_id>", methods=["PUT"])
@with_db_session
def update_driver_endpoint(db: Session, driver_id: int):
    try:
        schema = DriverUpdate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        updated = driver_service.update_existing_driver(db, driver_id, schema)
        return jsonify(DriverResponse.model_validate(updated).model_dump()), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@driver_bp.route("/<int:driver_id>", methods=["DELETE"])
@with_db_session
def delete_driver_endpoint(db: Session, driver_id: int):
    try:
        driver_service.delete_existing_driver(db, driver_id)
        return jsonify({"message": "driver deleted"}), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404


# М:1 - Отримати всі авто конкретного водія
@driver_bp.route("/<int:driver_id>/cars", methods=["GET"])
@with_db_session
def get_driver_cars_endpoint(db: Session, driver_id: int):
    """Get all cars for a specific driver"""
    try:
        cars = driver_service.get_driver_cars(db, driver_id)
        result = [CarResponse.model_validate(car).model_dump() for car in cars]
        return jsonify(result), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# М:М - Отримати всі типи авто для водія
@driver_bp.route("/<int:driver_id>/car-types", methods=["GET"])
@with_db_session
def get_driver_car_types_endpoint(db: Session, driver_id: int):
    """Get all car types that a driver can work with (M:M relationship)"""
    try:
        from my_project.domain.schemas import CarTypeResponse
        car_types = driver_service.get_driver_car_types(db, driver_id)
        result = [CarTypeResponse.model_validate(ct).model_dump() for ct in car_types]
        return jsonify(result), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# М:М - Додати тип авто водієві
@driver_bp.route("/<int:driver_id>/car-types/<int:car_type_id>", methods=["POST"])
@with_db_session
def add_driver_car_type_endpoint(db: Session, driver_id: int, car_type_id: int):
    """Add a car type to a driver's allowed types (M:M relationship)"""
    try:
        driver_service.add_driver_car_type(db, driver_id, car_type_id)
        return jsonify({"message": "Car type added to driver"}), 201
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# М:М - Видалити тип авто у водія
@driver_bp.route("/<int:driver_id>/car-types/<int:car_type_id>", methods=["DELETE"])
@with_db_session
def remove_driver_car_type_endpoint(db: Session, driver_id: int, car_type_id: int):
    """Remove a car type from a driver's allowed types (M:M relationship)"""
    try:
        driver_service.remove_driver_car_type(db, driver_id, car_type_id)
        return jsonify({"message": "Car type removed from driver"}), 200
    except DriverNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
