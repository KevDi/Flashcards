from datetime import datetime
from flask import url_for
from .. import db
from .category import Category
from .flashcard import Flashcard
from .hascategory import has_category
from app.exceptions import ValidationError


class FlashcardCollection(db.Model):
    __tablename__ = 'flashcardcollection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')
    categories = db.relationship('Category',
                                 secondary=has_category,
                                 backref=db.backref('collections', lazy='dynamic'),
                                 lazy='dynamic')

    def to_json(self):
        json_collection = {
            'url': url_for('api.get_collection', id=self.id, _external=True),
            'name': self.name,
            'timestamp': self.timestamp,
            'user': url_for('api.get_user', id=self.user_id, _external=True),
            'flashcards': url_for('api.get_collection_flashcards', id=self.id, _external=True),
            'flashcard_count': self.flashcards.count(),
            'categories': url_for('api.get_collection_categories', id=self.id, _external=True),
            'categories_count': self.categories.count()
        }
        return json_collection

    @staticmethod
    def from_json(json_collection):
        name = json_collection.get('name')
        if name is None or name == '':
            raise ValidationError('FlashcardCollection must have a name!')
        collection = FlashcardCollection(name=name)
        categories = json_collection.get('categories', [])
        for category in categories:
            if category.get('name') is not None:
                cat = Category(name=category.get('name'))
                collection.categories.append(cat)
        flashcards = json_collection.get('flashcards', [])
        for flashcard in flashcards:
            if flashcard.get('answer') is not None and flashcard.get('question') is not None:
                card = Flashcard(question=flashcard.get('question'), answer=flashcard.get('answer'))
                collection.flashcards.append(card)
        return collection

    def __repr__(self):
        return '<Flashcard Collection: %r>' % self.name
