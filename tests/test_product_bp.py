import io
import unittest
from app import app
from app.products.db import reset_db


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        reset_db()

    def tearDown(self):
        reset_db()

    def test_products_list(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

        alt_response = self.client.get("/product")
        self.assertEqual(alt_response.status_code, 200)
        self.assertIn(b"Laptop", alt_response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

        alt_response = self.client.get("/product/1")
        self.assertEqual(alt_response.status_code, 200)
        self.assertIn(b"Laptop", alt_response.data)

    def test_product_detail_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_product_add_get(self):
        response = self.client.get("/products/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"name", response.data)
        self.assertIn(b"price", response.data)

    def test_product_add_post_valid(self):
        data = {
            "name": "Tablet",
            "content": "Сучасний планшет для навчання та роботи.",
            "price": "650.00",
            "category": "Смартфони",
            "quantity": "15"
        }
        response = self.client.post("/products/add", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tablet".encode("utf-8"), response.data)

    def test_product_add_post_with_image(self):
        data = {
            "name": "Mouse",
            "content": "Бездротова ергономічна мишка.",
            "price": "45.00",
            "category": "Аксесуари",
            "quantity": "50",
            "image": (io.BytesIO(b"fake image data"), "mouse.png")
        }
        response = self.client.post("/products/add", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mouse".encode("utf-8"), response.data)

    def test_product_add_post_invalid(self):
        data = {
            "name": "X",
            "content": "Опис",
            "price": "-10",
            "category": "Ноутбуки",
            "quantity": "-5"
        }
        response = self.client.post("/products/add", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Назва повинна містити щонайменше 3 символи".encode("utf-8"), response.data)

    def test_product_edit_get(self):
        response = self.client.get("/products/1/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

    def test_product_edit_post(self):
        data = {
            "name": "Laptop Gaming",
            "content": "Оновлений потужний ноутбук.",
            "price": "1400.00",
            "category": "Ноутбуки",
            "quantity": "8"
        }
        response = self.client.post("/products/1/edit", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Laptop Gaming".encode("utf-8"), response.data)
        self.assertIn(b"1400", response.data)

    def test_product_delete(self):
        add_data = {
            "name": "Keyboard",
            "content": "Механічна клавіатура з підсвіткою.",
            "price": "120.00",
            "category": "Аксесуари",
            "quantity": "20"
        }
        self.client.post("/products/add", data=add_data)
        from app.products.db import get_all_products
        products = get_all_products()
        created = next(p for p in products if p["name"] == "Keyboard")
        delete_url = f"/products/{created['id']}/delete"
        response = self.client.post(delete_url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        check_response = self.client.get(f"/products/{created['id']}")
        self.assertEqual(check_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
