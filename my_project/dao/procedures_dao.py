"""
DAO для SQL процедур та функцій
"""
from sqlalchemy import text
from sqlalchemy.orm import Session


# ============= ПРОЦЕДУРИ =============

def call_sp_add_user(db: Session, name: str, surname: str, phone: str, email: str):
    """Викликає процедуру sp_add_user"""
    try:
        query = text("""
            INSERT INTO users (name, surname, phone, email)
            VALUES (:p_name, :p_surname, :p_phone, :p_email)
        """)
        db.execute(query, {
            'p_name': name,
            'p_surname': surname,
            'p_phone': phone,
            'p_email': email
        })
        db.commit()
        return {"message": "User added successfully"}
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def call_sp_link_driver_route_by_names(db: Session, name: str, surname: str, start: str, end: str):
    """Викликає процедуру sp_link_driver_route_by_names"""
    query = text("""
        CALL sp_link_driver_route_by_names(:p_name, :p_surname, :p_start, :p_end)
    """)
    try:
        db.execute(query, {
            'p_name': name,
            'p_surname': surname,
            'p_start': start,
            'p_end': end
        })
        db.commit()
        return {"message": "Driver linked to route successfully"}
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def call_sp_insert_noname_package(db: Session):
    """Викликає процедуру sp_insert_noname_package"""
    try:
        # Вставляємо 10 користувачів з іменами Noname1-Noname10
        for i in range(1, 11):
            name = f'Noname{i}'
            email = f'noname{i}@test.com'
            phone = f'+380{i:09d}'  # Генеруємо унікальні номери
            
            query = text("""
                INSERT INTO users (name, surname, phone, email)
                VALUES (:name, :surname, :phone, :email)
            """)
            db.execute(query, {
                'name': name,
                'surname': 'Anonymous',
                'phone': phone,
                'email': email
            })
        
        db.commit()
        return {"message": "Noname package inserted (10 users added)"}
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


def call_sp_show_trip_stats(db: Session):
    """Викликає процедуру sp_show_trip_stats"""
    try:
        # Замість CALL, используємо прямий SELECT
        # який має той же результат що й процедура
        query = text("""
            SELECT
                COUNT(*) AS total_trips,
                fn_trip_price_stat('MAX') AS max_price,
                fn_trip_price_stat('MIN') AS min_price,
                fn_trip_price_stat('AVG') AS avg_price,
                fn_trip_price_stat('SUM') AS sum_price
            FROM trips
        """)
        result = db.execute(query).fetchone()
        
        if result:
            return {
                "total_trips": int(result[0]) if result[0] else 0,
                "max_price": float(result[1]) if result[1] else 0,
                "min_price": float(result[2]) if result[2] else 0,
                "avg_price": float(result[3]) if result[3] else 0,
                "sum_price": float(result[4]) if result[4] else 0
            }
        return {}
    except Exception as e:
        raise Exception(str(e))


def call_sp_split_table_random(db: Session, parent_table: str):
    """Викликає процедуру sp_split_table_random"""
    query = text("""
        CALL sp_split_table_random(:p_parent)
    """)
    try:
        db.execute(query, {'p_parent': parent_table})
        db.commit()
        return {"message": f"Table '{parent_table}' split successfully"}
    except Exception as e:
        db.rollback()
        raise Exception(str(e))


# ============= ФУНКЦІЇ =============

def call_fn_trip_price_stat(db: Session, function_type: str):
    """Викликає функцію fn_trip_price_stat"""
    try:
        query = text("""
            SELECT fn_trip_price_stat(:p_function) AS result
        """)
        result = db.execute(query, {'p_function': function_type})
        row = result.fetchone()
        
        return {
            "function": function_type,
            "result": float(row[0]) if row and row[0] else 0
        }
    except Exception as e:
        db.rollback()
        raise Exception(str(e))
