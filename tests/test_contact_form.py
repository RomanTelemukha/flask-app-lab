import os
import unittest
from app import app


class ContactFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        self.log_path = os.path.join(os.path.dirname(app.root_path), "feedback.log")

    def test_contact_page_loads(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"name", response.data)
        self.assertIn(b"email", response.data)
        self.assertIn(b"phone", response.data)
        self.assertIn(b"subject", response.data)
        self.assertIn(b"message", response.data)

    def test_contact_form_valid_submission(self):
        valid_data = {
            "name": "Ivan",
            "email": "ivan@example.com",
            "phone": "+380991234567",
            "subject": "feedback",
            "message": "Тестове повідомлення"
        }
        response = self.client.post("/contact", data=valid_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Повідомлення успішно надіслано та збережено!".encode("utf-8"), response.data)
        self.assertTrue(os.path.exists(self.log_path))
        with open(self.log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("Ivan", log_content)
            self.assertIn("ivan@example.com", log_content)

    def test_contact_form_invalid_name_short(self):
        invalid_data = {
            "name": "Tom",
            "email": "tom@example.com",
            "phone": "+380991234567",
            "subject": "general",
            "message": "Тестове повідомлення"
        }
        response = self.client.post("/contact", data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Довжина імені повинна бути від 4 до 10 символів".encode("utf-8"), response.data)

    def test_contact_form_invalid_phone(self):
        invalid_data = {
            "name": "Andriy",
            "email": "andriy@example.com",
            "phone": "0991234567",
            "subject": "support",
            "message": "Тестове повідомлення"
        }
        response = self.client.post("/contact", data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Формат телефону повинен бути +380XXXXXXXXX".encode("utf-8"), response.data)

    def test_contact_form_invalid_email(self):
        invalid_data = {
            "name": "Andriy",
            "email": "bad-email",
            "phone": "+380991234567",
            "subject": "support",
            "message": "Тестове повідомлення"
        }
        response = self.client.post("/contact", data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Некоректний формат email".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
