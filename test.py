from unittest import TestCase

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(last_name="Zaytseva", first_name="Irina")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Blogly Recent Posts</h1>', html)

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Zaytseva', html)

    def test_show_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Maksym", "last_name": "Zaytsev", "image_url": "https://www.clipartkey.com/mpngs/m/22-221407_super-mario-svg-free.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Irina Zaytseva", html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit a user</h1>", html)

    def test_update_user(self):
        with app.test_client() as client:
            d = {"first_name": "Maksym", "last_name": "Illiashenko", "image_url": "https://www.clipartkey.com/mpngs/m/22-221407_super-mario-svg-free.png"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)


    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)



class PostTestCase(TestCase):
    """Tests for views for Posts."""
   
    def setUp(self):
        """Add sample post."""
     
        Post.query.delete()

        post = Post(title="Titanic", content="This is my favorite movie")
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Titanic", html)


    # def test_show_post_form(self):
    #     with app.test_client() as client:
    #         resp = client.get("/users/user.id/posts/new")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Add Post for", html)

    # def test_update_user(self):
    #     with app.test_client() as client:
    #         d = {"title": "Titanic", "content": "The best movie ever!"}
    #         resp = client.post("/users/user.id/posts/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h2>Posts</h2>", html)     
              
    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Post", html)

    # def test_update_post(self):
    #     with app.test_client() as client:
    #         d = {"title": "Titanic", "content": "The best movie ever! Must watch!"}
    #         resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Posts", html) 


    # def test_delete_post(self):
    #     with app.test_client() as client:
    #         resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h2>Posts</h2>", html)
    
class TagTestCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add sample tag."""

        Tag.query.delete()

        tag = Tag(name="fun")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_tags(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('fun', html)

    def test_show_tag_form(self):
        with app.test_client() as client:
            resp = client.get("/tags/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a tag</h1>', html)

    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("fun", html)        
    
    def test_edit_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit a tag</h1>", html) 


    def test_update_tag(self):
        with app.test_client() as client:
            d = {"name": "daram"}
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Tags</h1>", html)

    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f"/tags/{self.tag_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Tags</h1>", html)