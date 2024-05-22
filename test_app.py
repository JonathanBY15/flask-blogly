import unittest
from app import app, db, User
from bs4 import BeautifulSoup

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and initialize database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:walmart48@localhost/blogly_test'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()  # Close the session after each test
            db.drop_all()

    def test_users_list(self):
        """Test user list page. Assert that the page loads and contains an h1:'Users'."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find the h1 tag
        h1_tag = soup.find('h1')
        
        # Check if the h1 tag has the value 'Users'
        self.assertIsNotNone(h1_tag)
        self.assertEqual(h1_tag.text, 'Users')

    def test_add_user(self):
        """Test adding a new user. Assert that the user is added and displayed on the page."""
        response = self.client.post('/users/new', data={
            'first_name': 'Test',
            'last_name': 'User',
            'image_url': ''
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_show_user(self):
        """Test showing a user. Assert that the user is displayed on the page along with the edit button."""
        with app.app_context():
            user = User(first_name='Test', last_name='User', image_url='https://cdn-icons-png.flaticon.com/128/1077/1077063.png')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            response = self.client.get(f'/users/{user_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)
            self.assertIn(b'Edit', response.data)

    def test_edit_user(self):
        """Test editing a user. Assert that the user is updated and displayed on the page."""
        with app.app_context():
            user = User(first_name='Test', last_name='User', image_url='https://cdn-icons-png.flaticon.com/128/1077/1077063.png')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            response = self.client.post(f'/users/{user_id}/edit', data={
                'first_name': 'Updated',
                'last_name': 'User',
                'image_url': 'https://cdn-icons-png.flaticon.com/128/1077/1077063.png'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Updated User', response.data)

    def test_delete_user(self):
        """Test deleting a user. Assert that the user is deleted and not displayed on the page."""
        with app.app_context():
            user = User(first_name='Test', last_name='User', image_url='https://cdn-icons-png.flaticon.com/128/1077/1077063.png')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            response = self.client.post(f'/users/{user_id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test User', response.data)

if __name__ == '__main__':
    unittest.main()
