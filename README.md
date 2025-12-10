# Lab 4 - Flask REST API with MySQL

Реалізація Back-end проекту на Flask + Python з підключенням до MySQL.

## Структура проекту

```
app.py                          # Flask app entry point
config/
  app.yml                       # Database configuration
my_project/
  database.py                   # SQLAlchemy engine & session
  domain/
    models.py                   # SQLAlchemy ORM models
    schemas.py                  # Pydantic DTO schemas
  controller/
    user_controller.py          # User endpoints
    driver_controller.py        # Driver endpoints
    car_type_controller.py      # CarType endpoints
    car_controller.py           # Car endpoints
  service/
    user_service.py             # User business logic
    driver_service.py           # Driver business logic
    car_type_service.py         # CarType business logic
    car_service.py              # Car business logic
  dao/
    user_dao.py                 # User data access
    driver_dao.py               # Driver data access
    car_type_dao.py             # CarType data access
    car_dao.py                  # Car data access
```

## Запуск приложения

1. **Переконайтеся, що MySQL запущен і БД налаштована** (див. `config/app.yml`)

2. **Установіть залежності:**
   ```powershell
   pip install flask sqlalchemy mysql-connector-python pydantic pyyaml
   ```

3. **Запустіть додаток:**
   ```powershell
   python app.py
   ```
   або
   ```powershell
   flask run
   ```

4. **API буде доступний за адресою:** `http://localhost:5000`

## Функціональність

### CRUD операції
- ✅ **Вивід даних з таблиць** — GET endpoints для всіх сутностей
- ✅ **Вставка даних у таблиці** — POST endpoints для створення записів
- ✅ **Оновлення даних** — PUT endpoints для редагування записів
- ✅ **Видалення даних** — DELETE endpoints для видалення записів

### М:1 (Many-to-One) запити
- `GET /cars/by-driver/{driver_id}` — отримати всі машини водія
- `GET /cars/by-type/{car_type_id}` — отримати всі машини типу
- `GET /drivers/{driver_id}/cars` — альтернативний endpoint для машин водія
- `GET /car-types/{car_type_id}/cars` — отримати машини конкретного типу

### М:М (Many-to-Many) запити
Зв'язок: **Driver ↔ CarType** (водій може працювати з декількома типами машин)

- `GET /drivers/{driver_id}/car-types` — отримати всі типи машин для водія
- `POST /drivers/{driver_id}/car-types/{car_type_id}` — додати тип машини водієві
- `DELETE /drivers/{driver_id}/car-types/{car_type_id}` — видалити тип машини від водія

## Архітектура

### Контролери
- Обробляють HTTP запити
- Валідують вхідні дані за допомогою Pydantic
- Повертають DTO-об'єкти у форматі JSON
- Обробляють помилки з відповідними HTTP кодами

### Сервіси
- Містять бізнес-логіку
- Перевіряють, що сутності існують
- Вальідують бізнес-правила (наприклад, унікальність)
- Викликають DAO методи для роботи з БД

### DAO (Data Access Objects)
- Містять усі SQL-запити через SQLAlchemy
- М:1 запити: `get_cars_by_driver()`, `get_cars_by_type()`
- М:М запити: `get_driver_car_types()`, `add_driver_car_type()`, `remove_driver_car_type()`

### Schemas (DTO)
Pydantic моделі для валідації і серіалізації:
- `UserResponse`, `DriverResponse`, `CarTypeResponse`, `CarResponse`
- `UserCreate`, `DriverCreate`, `CarTypeCreate`, `CarCreate`
- `UserUpdate`, `DriverUpdate`, `CarTypeUpdate`, `CarUpdate`

## Тестування через Postman

1. **Імпортуйте колекцію** — відкрийте `Postman_Collection.json` у Postman
2. **Запустіть запити** — всі examples готові до використання

### SQL Процедури та Функції (Endpoints)

#### Процедури (POST)
- **`POST /procedures/sp_add_user`** — додати користувача
  ```json
  {"name": "Alice", "surname": "Smith", "phone": "+380991111111", "email": "alice@test.com"}
  ```

- **`POST /procedures/sp_link_driver_route_by_names`** — зв'язати водія з маршрутом
  ```json
  {"name": "John", "surname": "Doe", "start": "Kyiv", "end": "Kharkiv"}
  ```

- **`POST /procedures/sp_insert_noname_package`** — додати 10 анонімних користувачів
  ```json
  {}
  ```

- **`POST /procedures/sp_split_table_random`** — розділити таблицю випадково
  ```json
  {"table_name": "trips"}
  ```

#### Процедури (GET)
- **`GET /procedures/sp_show_trip_stats`** — статистика поїздок
  - Повертає: `total_trips`, `max_price`, `min_price`, `avg_price`, `sum_price`

#### Функції (GET)
- **`GET /procedures/fn_trip_price_stat/{function_type}`** — статистика ціни поїздок
  - `function_type`: `MAX`, `MIN`, `AVG`, `SUM`
  - Приклади:
    - `/procedures/fn_trip_price_stat/MAX` — максимальна ціна
    - `/procedures/fn_trip_price_stat/MIN` — мінімальна ціна
    - `/procedures/fn_trip_price_stat/AVG` — середня ціна
    - `/procedures/fn_trip_price_stat/SUM` — сума всіх цін

#### Створення користувача
```bash
POST http://localhost:5000/users/
Content-Type: application/json

{
  "name": "John",
  "surname": "Doe",
  "phone": "+380991234567",
  "email": "john@example.com"
}
```

#### Створення водія
```bash
POST http://localhost:5000/drivers/
Content-Type: application/json

{
  "user_id": 1,
  "license_number": "DL123456",
  "experience_years": 5
}
```

#### Отримання всіх машин водія (М:1)
```bash
GET http://localhost:5000/drivers/1/cars
```

#### Додання типу машини водієві (М:М)
```bash
POST http://localhost:5000/drivers/1/car-types/1
```

#### Отримання типів машин, з якими працює водій (М:М)
```bash
GET http://localhost:5000/drivers/1/car-types
```

## Статус

- ✅ Всі 4 сутності мають CRUD операції
- ✅ М:1 запити реалізовані (Driver → Cars, CarType → Cars)
- ✅ М:М запити реалізовані (Driver ↔ CarType через junction table)
- ✅ Всі контролери повертають DTO-об'єкти
- ✅ Сервіси містять бізнес-логіку
- ✅ DAO містить усі SQL-методи
- ✅ Постман-колекція готова до тестування
- ✅ SQL процедури та функції підтримані через endpoints

## Готові endpoint'и (35 всього)

```
Users (5):
  POST   /users/
  GET    /users/
  GET    /users/<id>
  PUT    /users/<id>
  DELETE /users/<id>

Drivers (9):
  POST   /drivers/
  GET    /drivers/
  GET    /drivers/<id>
  PUT    /drivers/<id>
  DELETE /drivers/<id>
  GET    /drivers/<id>/cars           [M:1]
  GET    /drivers/<id>/car-types      [M:M]
  POST   /drivers/<id>/car-types/<car_type_id> [M:M]
  DELETE /drivers/<id>/car-types/<car_type_id> [M:M]

CarTypes (6):
  POST   /car-types/
  GET    /car-types/
  GET    /car-types/<id>
  PUT    /car-types/<id>
  DELETE /car-types/<id>
  GET    /car-types/<id>/cars        [M:1]

Cars (5):
  POST   /cars/
  GET    /cars/
  GET    /cars/<id>?driver_id=<id>
  PUT    /cars/<id>?driver_id=<id>
  DELETE /cars/<id>?driver_id=<id>

SQL Procedures & Functions (6):
  POST   /procedures/sp_add_user
  POST   /procedures/sp_link_driver_route_by_names
  POST   /procedures/sp_insert_noname_package
  GET    /procedures/sp_show_trip_stats
  POST   /procedures/sp_split_table_random
  GET    /procedures/fn_trip_price_stat/{MAX|MIN|AVG|SUM}
```

Всього: **35 endpoint'ів**

### Документація по процедурам

Детальне описання з прикладами для всіх процедур та функцій — див. **[PROCEDURES_USAGE.md](PROCEDURES_USAGE.md)**
