import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["username"] = "tester"

            response = self.client.post("/post/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "text": "This is TDD!",
                "category": "news",
                "is_active": True
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)

            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
            self.assertEqual(post.author, "tester")

    def test_list_posts(self):
        with self.app.app_context():
            p1 = Post(title="Visible Post", content="Content 1", is_active=True, category="news")
            p2 = Post(title="Hidden Post", content="Content 2", is_active=False, category="news")
            db.session.add_all([p1, p2])
            db.session.commit()

            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Visible Post", response.data)
            self.assertNotIn(b"Hidden Post", response.data)

    def test_view_post_detail(self):
        with self.app.app_context():
            p = Post(title="Detail Post", content="Full article content", is_active=True, author="author1", category="tech")
            db.session.add(p)
            db.session.commit()

            response = self.client.get(f"/post/{p.id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Post", response.data)
            self.assertIn(b"Full article content", response.data)
            self.assertIn(b"author1", response.data)

    def test_update_post(self):
        with self.app.app_context():
            p = Post(title="Old Title", content="Old Content", is_active=True, category="news")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(f"/post/{post_id}/update", data={
                "title": "New Title",
                "content": "Updated Content",
                "category": "tech",
                "is_active": True
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.title, "New Title")
            self.assertEqual(updated.content, "Updated Content")
            self.assertEqual(updated.category, "tech")

    def test_delete_post(self):
        with self.app.app_context():
            p = Post(title="To Delete", content="Will be deleted", is_active=True, category="other")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            deleted = db.session.get(Post, post_id)
            self.assertIsNone(deleted)

    def test_404_not_found(self):
        response = self.client.get("/post/99999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)


if __name__ == "__main__":
    unittest.main()

