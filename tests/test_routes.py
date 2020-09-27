import unittest

from app import app, db
from app.models import User, Device
from config import TestConfig

class TestHome(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if hasattr(self, 'client'):
            del self.client

    def test_home_with_no_active_users(self):
        with app.test_client() as client:
            result = client.get('home')
            self.assertTrue(b"No-one" in result.data)