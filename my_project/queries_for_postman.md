Users:
POST:
{
"name": "andriy",
"surname": "Porada",
"phone": "+380501234567",
"email": "[andriy@gmail.com](mailto:andriy@gmail.com)"
}

GET: [http://127.0.0.1:5000/users/](http://127.0.0.1:5000/users/)
[http://127.0.0.1:5000/users/1](http://127.0.0.1:5000/users/1)
[http://127.0.0.1:5000/users/1/cars](http://127.0.0.1:5000/users/1/cars)
[http://127.0.0.1:5000/users/1/drivers](http://127.0.0.1:5000/users/1/drivers)

PUT: [http://127.0.0.1:5000/users/1](http://127.0.0.1:5000/users/1)
{
"name": "andriy_updated",
"surname": "Porada",
"phone": "+380509876543",
"email": "[new@gmail.com](mailto:new@gmail.com)"
}

DELETE: [http://127.0.0.1:5000/users/1](http://127.0.0.1:5000/users/1)

Drivers:
POST:
{
"user_id": 1,
"license_number": "AB123456",
"experience_years": 5
}

GET: [http://127.0.0.1:5000/drivers/](http://127.0.0.1:5000/drivers/)
[http://127.0.0.1:5000/drivers/1](http://127.0.0.1:5000/drivers/1)
[http://127.0.0.1:5000/drivers/1/cars](http://127.0.0.1:5000/drivers/1/cars)

PUT: [http://127.0.0.1:5000/drivers/1](http://127.0.0.1:5000/drivers/1)
{
"license_number": "CD654321",
"experience_years": 6
}

DELETE: [http://127.0.0.1:5000/drivers/1](http://127.0.0.1:5000/drivers/1)

Car Types:
POST:
{
"name": "Sedan",
"seats": 5,
"description": "Comfortable family car"
}

GET: [http://127.0.0.1:5000/car-types/](http://127.0.0.1:5000/car-types/)
[http://127.0.0.1:5000/car-types/1](http://127.0.0.1:5000/car-types/1)
[http://127.0.0.1:5000/car-types/1/cars](http://127.0.0.1:5000/car-types/1/cars)

PUT: [http://127.0.0.1:5000/car-types/1](http://127.0.0.1:5000/car-types/1)
{
"name": "Sedan Updated",
"seats": 5,
"description": "Updated description"
}

DELETE: [http://127.0.0.1:5000/car-types/1](http://127.0.0.1:5000/car-types/1)

Cars:
POST:
{
"driver_id": 1,
"car_id": 1,
"car_type_id": 1,
"brand": "Toyota",
"model": "Camry",
"plate_number": "AA1234BB",
"year": 2022
}

GET: [http://127.0.0.1:5000/cars/](http://127.0.0.1:5000/cars/)
[http://127.0.0.1:5000/cars/1](http://127.0.0.1:5000/cars/1)

PUT: [http://127.0.0.1:5000/cars/1](http://127.0.0.1:5000/cars/1)
{
"brand": "Toyota",
"model": "Camry Updated",
"plate_number": "AA5678BB",
"year": 2023,
"car_type_id": 1
}

DELETE: [http://127.0.0.1:5000/cars/1](http://127.0.0.1:5000/cars/1)
