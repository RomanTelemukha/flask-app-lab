import unittest
from app import app


class Lab4TestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post("/users/login", data={"username": "wrong", "password": "wrong"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong data! Try again!", response.data)

    def test_login_valid_credentials(self):
        response = self.client.post("/users/login", data={"username": "user1", "password": "password"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1", response.data)

    def test_profile_unauthorized(self):
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_profile_authorized(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1", response.data)

    def test_logout(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        response = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)
        with self.client.session_transaction() as sess:
            self.assertNotIn("username", sess)

    def test_add_cookie(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        response = self.client.post("/users/cookie/add", data={"cookie_key": "test_key", "cookie_value": "test_val", "cookie_expire": "3600"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("test_key=test_val", response.headers.get("Set-Cookie", ""))

    def test_delete_cookie(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        self.client.set_cookie("test_key", "test_val")
        response = self.client.post("/users/cookie/delete", data={"delete_key": "test_key"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("test_key=;", response.headers.get("Set-Cookie", ""))

    def test_change_theme(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        response = self.client.get("/users/theme/dark")
        self.assertEqual(response.status_code, 302)
        self.assertIn("theme=dark", response.headers.get("Set-Cookie", ""))


if __name__ == "__main__":
    unittest.main()
