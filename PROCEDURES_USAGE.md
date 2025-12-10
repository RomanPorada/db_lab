# Приклади використання SQL Процедур та Функцій

## Передумови

1. Сервер запущений: `http://localhost:5000`
2. Процедури та функції створені в MySQL базі даних `lab_4`
3. Таблиці та зв'язки існують (routes, trips, тощо)

## SQL Процедури

### 1. sp_add_user — Додати користувача

**Endpoint:** `POST /procedures/sp_add_user`

**Request Body (JSON):**
```json
{
  "name": "Ivan",
  "surname": "Petrov",
  "phone": "+380991234567",
  "email": "ivan@example.com"
}
```

**Response (201):**
```json
{
  "message": "User added successfully"
}
```

**PowerShell приклад:**
```powershell
$body = @{
    name = "Ivan"
    surname = "Petrov"
    phone = "+380991234567"
    email = "ivan@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:5000/procedures/sp_add_user" `
  -ContentType "application/json" `
  -Body $body
```

**curl приклад:**
```bash
curl -X POST http://localhost:5000/procedures/sp_add_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Ivan","surname":"Petrov","phone":"+380991234567","email":"ivan@example.com"}'
```

---

### 2. sp_link_driver_route_by_names — Зв'язати водія з маршрутом

**Endpoint:** `POST /procedures/sp_link_driver_route_by_names`

Спеціальна процедура, яка за іменем/прізвищем водія та стартовою/кінцевою локацією знайде водія та маршрут, а потім створить зв'язок.

**Request Body (JSON):**
```json
{
  "name": "John",
  "surname": "Doe",
  "start": "Kyiv",
  "end": "Kharkiv"
}
```

**Response (201):**
```json
{
  "message": "Driver linked to route successfully"
}
```

**Помилки:**
- `"User with given name/surname not found"` — користувач не знайдений
- `"This user is not a driver"` — користувач існує, але не є водієм
- `"Route not found"` — маршрут не знайдений

**curl приклад:**
```bash
curl -X POST http://localhost:5000/procedures/sp_link_driver_route_by_names \
  -H "Content-Type: application/json" \
  -d '{"name":"John","surname":"Doe","start":"Kyiv","end":"Kharkiv"}'
```

---

### 3. sp_insert_noname_package — Додати 10 анонімних користувачів

**Endpoint:** `POST /procedures/sp_insert_noname_package`

Процедура додає 10 користувачів з іменами Noname1-Noname10 та однаковим номером телефону.

**Request Body (JSON):**
```json
{}
```

**Response (201):**
```json
{
  "message": "Noname package inserted (10 users added)"
}
```

**curl приклад:**
```bash
curl -X POST http://localhost:5000/procedures/sp_insert_noname_package \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 4. sp_show_trip_stats — Статистика поїздок

**Endpoint:** `GET /procedures/sp_show_trip_stats`

Показує загальну статистику по всіх поїздках.

**Response (200):**
```json
{
  "total_trips": 42,
  "max_price": 1250.50,
  "min_price": 50.00,
  "avg_price": 487.25,
  "sum_price": 20484.50
}
```

**PowerShell приклад:**
```powershell
Invoke-RestMethod -Method Get `
  -Uri "http://localhost:5000/procedures/sp_show_trip_stats"
```

**curl приклад:**
```bash
curl -X GET http://localhost:5000/procedures/sp_show_trip_stats
```

---

### 5. sp_split_table_random — Розділити таблицю випадково

**Endpoint:** `POST /procedures/sp_split_table_random`

Розділяє таблицю на дві нові таблиці, випадково розподіляючи рядки.

**Request Body (JSON):**
```json
{
  "table_name": "trips"
}
```

**Response (201):**
```json
{
  "message": "Table 'trips' split successfully"
}
```

**Результат:** 
- Таблиця `trips` залишається незміненою
- Створюються дві нові таблиці:
  - `trips_partA_20251210_143022`
  - `trips_partB_20251210_143022`

**curl приклад:**
```bash
curl -X POST http://localhost:5000/procedures/sp_split_table_random \
  -H "Content-Type: application/json" \
  -d '{"table_name":"trips"}'
```

---

## SQL Функції

### fn_trip_price_stat — Статистика цін на поїздки

**Endpoint:** `GET /procedures/fn_trip_price_stat/{function_type}`

Розраховує статистику цін за типом функції.

#### Параметр function_type:
- `MAX` — максимальна ціна
- `MIN` — мінімальна ціна
- `AVG` — середня ціна
- `SUM` — сума всіх цін

#### Приклади:

**1. Максимальна ціна**
```
GET /procedures/fn_trip_price_stat/MAX
```
```json
{
  "function": "MAX",
  "result": 1250.50
}
```

**2. Мінімальна ціна**
```
GET /procedures/fn_trip_price_stat/MIN
```
```json
{
  "function": "MIN",
  "result": 50.00
}
```

**3. Середня ціна**
```
GET /procedures/fn_trip_price_stat/AVG
```
```json
{
  "function": "AVG",
  "result": 487.25
}
```

**4. Сума всіх цін**
```
GET /procedures/fn_trip_price_stat/SUM
```
```json
{
  "function": "SUM",
  "result": 20484.50
}
```

**PowerShell приклади:**
```powershell
# MAX
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/procedures/fn_trip_price_stat/MAX"

# MIN
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/procedures/fn_trip_price_stat/MIN"

# AVG
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/procedures/fn_trip_price_stat/AVG"

# SUM
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/procedures/fn_trip_price_stat/SUM"
```

**curl приклади:**
```bash
curl -X GET http://localhost:5000/procedures/fn_trip_price_stat/MAX
curl -X GET http://localhost:5000/procedures/fn_trip_price_stat/MIN
curl -X GET http://localhost:5000/procedures/fn_trip_price_stat/AVG
curl -X GET http://localhost:5000/procedures/fn_trip_price_stat/SUM
```

---

## Обробка помилок

### Неправильний параметр function_type
```
GET /procedures/fn_trip_price_stat/INVALID
```

**Response (400):**
```json
{
  "error": "Invalid function type. Allowed: MAX, MIN, AVG, SUM"
}
```

### Помилка при виконанні процедури
```json
{
  "error": "Error linking driver to route: User with given name/surname not found"
}
```

---

## Запуск в Postman

1. Імпортуйте `Postman_Collection.json`
2. Перейдіть на папку "SQL Procedures"
3. Запустіть потрібну процедуру
4. Для функцій перейдіть на "SQL Functions" і виберіть потрібний тип

---

## Замітки

- Всі процедури та функції працюють тільки, якщо вони існують в MySQL базі даних
- Перевірте, що таблиці `users`, `drivers`, `routes`, `trips` існують
- Для `sp_split_table_random` переконайтеся, що таблиця має поле `id`
- Номер телефону повинен бути унікальним при додаванні користувача через `sp_add_user`
