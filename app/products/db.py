import os
from datetime import datetime
from tinydb import TinyDB, Query

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "products.json")

DEFAULT_PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200.0,
        "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам’яті та SSD на 512 ГБ.",
        "category": "Ноутбуки",
        "quantity": 10,
        "image": "",
        "created_at": "2026-11-12 10:00:00"
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800.0,
        "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год.",
        "category": "Смартфони",
        "quantity": 25,
        "image": "",
        "created_at": "2026-11-12 10:00:00"
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800.0,
        "content": "Настільний комп’ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
        "category": "Комп'ютери",
        "quantity": 5,
        "image": "",
        "created_at": "2026-11-12 10:00:00"
    }
]


def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    return TinyDB(DB_PATH)


def init_db():
    with get_db() as db:
        table = db.table("products")
        if len(table) == 0:
            for item in DEFAULT_PRODUCTS:
                table.insert(item)


def get_all_products():
    init_db()
    with get_db() as db:
        table = db.table("products")
        return sorted(table.all(), key=lambda p: p["id"])


def get_product_by_id(product_id):
    init_db()
    with get_db() as db:
        table = db.table("products")
        product_query = Query()
        result = table.get(product_query.id == product_id)
        return result


def insert_product(data):
    init_db()
    with get_db() as db:
        table = db.table("products")
        all_products = table.all()
        new_id = max([p["id"] for p in all_products], default=0) + 1
        data["id"] = new_id
        data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table.insert(data)
        return data


def update_product(product_id, data):
    init_db()
    with get_db() as db:
        table = db.table("products")
        product_query = Query()
        existing = table.get(product_query.id == product_id)
        if not existing:
            return None
        data["id"] = existing["id"]
        data["created_at"] = existing["created_at"]
        table.update(data, product_query.id == product_id)
        return data


def delete_product(product_id):
    init_db()
    with get_db() as db:
        table = db.table("products")
        product_query = Query()
        removed = table.remove(product_query.id == product_id)
        return len(removed) > 0
