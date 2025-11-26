from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from my_project.database import get_db
from my_project.service import car_service
from my_project.service.car_service import CarNotFoundException, CarExistsException
from my_project.domain.schemas import CarCreateSchema, CarUpdateSchema, CarResponse

car_bp = Blueprint("cars", __name__, url_prefix="/cars")

# Декоратор для роботи з сесією бази
def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper


# Створити нове авто
@car_bp.route("/", methods=["POST"])
@with_db_session
def create_car_endpoint(db: Session):
    try:
        schema = CarCreateSchema.model_validate(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        new_car = car_service.create_new_car(db, schema)
        dto = CarResponse.model_validate(new_car).model_dump()
        return jsonify(dto), 201
    except CarExistsException as e:
        return jsonify({"error": str(e)}), 409


# Отримати всі авто
@car_bp.route("/", methods=["GET"])
@with_db_session
def get_cars_endpoint(db: Session):
    cars = car_service.get_all_cars(db)
    result = [CarResponse.model_validate(car).model_dump() for car in cars]
    return jsonify(result), 200


# Отримати одне авто по car_id і driver_id (query-параметр)
@car_bp.route("/<int:car_id>", methods=["GET"])
@with_db_session
def get_car_endpoint(db: Session, car_id: int):
    driver_id = request.args.get("driver_id", type=int)
    if driver_id is None:
        return jsonify({"error": "driver_id query parameter is required"}), 400

    try:
        car = car_service.get_car_by_id(db, car_id, driver_id)
        return jsonify(CarResponse.model_validate(car).model_dump()), 200
    except CarNotFoundException:
        return jsonify({"error": "Car not found"}), 404


# Оновити авто
@car_bp.route("/<int:car_id>", methods=["PUT"])
@with_db_session
def update_car_endpoint(db: Session, car_id: int):
    driver_id = request.args.get("driver_id", type=int)
    if driver_id is None:
        return jsonify({"error": "driver_id query parameter is required"}), 400

    try:
        schema = CarUpdateSchema.model_validate(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        updated_car = car_service.update_car(db, car_id, driver_id, schema)
        return jsonify(CarResponse.model_validate(updated_car).model_dump()), 200
    except CarNotFoundException:
        return jsonify({"error": "Car not found"}), 404


# Видалити авто
@car_bp.route("/<int:car_id>", methods=["DELETE"])
@with_db_session
def delete_car_endpoint(db: Session, car_id: int):
    driver_id = request.args.get("driver_id", type=int)
    if driver_id is None:
        return jsonify({"error": "driver_id query parameter is required"}), 400

    try:
        car_service.delete_car(db, car_id, driver_id)
        return jsonify({"message": "Car deleted"}), 200
    except CarNotFoundException:
        return jsonify({"error": "Car not found"}), 404


# М:1 - Отримати всі авто конкретного водія (driver_id)
@car_bp.route("/by-driver/<int:driver_id>", methods=["GET"])
@with_db_session
def get_cars_by_driver_endpoint(db: Session, driver_id: int):
    """Get all cars for a specific driver (M:1 relationship)"""
    try:
        cars = car_service.get_cars_by_driver(db, driver_id)
        result = [CarResponse.model_validate(car).model_dump() for car in cars]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# М:1 - Отримати всі авто конкретного типу (car_type_id)
@car_bp.route("/by-type/<int:car_type_id>", methods=["GET"])
@with_db_session
def get_cars_by_type_endpoint(db: Session, car_type_id: int):
    """Get all cars of a specific type (M:1 relationship)"""
    try:
        cars = car_service.get_cars_by_type(db, car_type_id)
        result = [CarResponse.model_validate(car).model_dump() for car in cars]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
