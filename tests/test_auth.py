import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_page_loads(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Registration".encode("utf-8"), response.data)

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login".encode("utf-8"), response.data)

    def test_register_success(self):
        response = self.client.post("/users/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Account created for newuser!".encode("utf-8"), response.data)
        with self.app.app_context():
            user = db.session.query(User).filter_by(username="newuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "newuser@example.com")
            self.assertNotEqual(user.password, "password123")
            self.assertTrue(user.check_password("password123"))

    def test_register_duplicate_username(self):
        with self.app.app_context():
            user = User(username="existing", email="exist@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        response = self.client.post("/users/register", data={
            "username": "existing",
            "email": "another@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Username is already taken.".encode("utf-8"), response.data)

    def test_register_duplicate_email(self):
        with self.app.app_context():
            user = User(username="userone", email="duplicate@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        response = self.client.post("/users/register", data={
            "username": "usertwo",
            "email": "duplicate@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Email is already registered.".encode("utf-8"), response.data)

    def test_login_success(self):
        with self.app.app_context():
            user = User(username="loginuser", email="loginuser@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        response = self.client.post("/users/login", data={
            "username": "loginuser",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome, loginuser!".encode("utf-8"), response.data)
        self.assertIn("loginuser@example.com".encode("utf-8"), response.data)

    def test_login_invalid_password(self):
        with self.app.app_context():
            user = User(username="testuser", email="testuser@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        response = self.client.post("/users/login", data={
            "username": "testuser",
            "password": "wrongpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error: Invalid username or password.".encode("utf-8"), response.data)

    def test_logout(self):
        with self.app.app_context():
            user = User(username="logoutuser", email="logoutuser@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        self.client.post("/users/login", data={
            "username": "logoutuser",
            "password": "password123"
        }, follow_redirects=True)
        response = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have successfully logged out.".encode("utf-8"), response.data)
        self.assertIn("Login".encode("utf-8"), response.data)

    def test_account_requires_login(self):
        response = self.client.get("/users/account")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    def test_users_list_requires_login(self):
        response = self.client.get("/users/users_list")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    def test_users_list_authenticated(self):
        with self.app.app_context():
            user = User(username="member1", email="member1@example.com", password="password123")
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        self.client.post("/users/login", data={
            "username": "member1",
            "password": "password123"
        }, follow_redirects=True)
        response = self.client.get("/users/users_list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Users List (1)".encode("utf-8"), response.data)
        self.assertIn("member1".encode("utf-8"), response.data)
        self.assertIn("member1@example.com".encode("utf-8"), response.data)

if __name__ == "__main__":
    unittest.main()
