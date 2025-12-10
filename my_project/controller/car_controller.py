from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from my_project.database import get_db
from my_project.service import car_service
from my_project.service.car_service import CarNotFoundException, CarExistsException
from my_project.domain.schemas import CarCreateSchema, CarUpdateSchema

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
        return jsonify(new_car.to_dict()), 201
    except CarExistsException as e:
        return jsonify({"error": str(e)}), 409


# Отримати всі авто
@car_bp.route("/", methods=["GET"])
@with_db_session
def get_cars_endpoint(db: Session):
    cars = car_service.get_all_cars(db)
    return jsonify([car.to_dict() for car in cars]), 200


# Отримати одне авто по car_id і driver_id (query-параметр)
@car_bp.route("/<int:car_id>", methods=["GET"])
@with_db_session
def get_car_endpoint(db: Session, car_id: int):
    driver_id = request.args.get("driver_id", type=int)
    if driver_id is None:
        return jsonify({"error": "driver_id query parameter is required"}), 400

    try:
        car = car_service.get_car_by_id(db, car_id, driver_id)
        return jsonify(car.to_dict()), 200
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
        return jsonify(updated_car.to_dict()), 200
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
