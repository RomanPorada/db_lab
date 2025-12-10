from flask import Flask
from my_project.controller.user_controller import user_bp
from my_project.controller.driver_controller import driver_bp
from my_project.controller.car_type_controller import car_type_bp
from my_project.controller.car_controller import car_bp
from my_project.controller.procedures_controller import procedures_bp

from my_project.database import engine, Base

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

app.register_blueprint(user_bp)
app.register_blueprint(driver_bp)
app.register_blueprint(car_type_bp)
app.register_blueprint(car_bp)
app.register_blueprint(procedures_bp)

@app.route('/')
def start():
    return "API Started"

if __name__ == '__main__':
    app.run(debug=True)