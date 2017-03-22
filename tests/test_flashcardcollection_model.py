import unittest
from app import create_app, db
from app.models.flashcard_collections import FlashcardCollection
from app.models.flashcard import Flashcard
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

    def test_wrong_answered_flashcards(self):
        f = FlashcardCollection(name='Testcollection')
        for x in range(20):
            c = Flashcard(question="Question{0}".format(x), answer="Answer{0}".format(x))
            if x % 2 == 0:
                c.wrong_answered = True
                c.right_answered = False
            else:
                c.wrong_answered = False
                c.right_answered = True
            f.flashcards.append(c)
        db.session.add(f)
        db.session.commit()
        self.assertTrue(f.flashcards.filter_by(wrong_answered=False).count() == 10)
        self.assertTrue(f.flashcards.filter_by(right_answered=True).count() == 10)

    def test_from_json(self):
        json_dict = {
            'name': 'Testcollection',
            'categories': [
                {'name': 'Frist Cat'},
                {'name': 'Sec Cat'}
            ],
            'flashcards': [
                {'question': 'Is this Right?',
                 'answer': 'Yes'},
                {'question': 'Is this Wrong?',
                 'answer': 'No'}
            ]
        }

        coll = FlashcardCollection.from_json(json_collection=json_dict)
        self.assertTrue(coll is not None)
        self.assertTrue(coll.name == 'Testcollection')
