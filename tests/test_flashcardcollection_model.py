import unittest
from app import create_app, db
from app.models.users import User
from app.models.flashcard_collections import FlashcardCollection
from app.models.category import Category


class FlashcardCollectionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_category(self):
        f = FlashcardCollection(name='Testcollection')
        c = Category(name='Test')
        f.categories.append(c)
        self.assertTrue(f.categories.count() == 1)
        c2 = Category(name='New')
        f.categories.append(c2)
        self.assertTrue(f.categories.count() == 2)
