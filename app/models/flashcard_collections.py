from datetime import datetime
from .. import db
from .hascategory import has_category


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

    def __repr__(self):
        return '<Flashcard Collection: %r>' % self.name
