from datetime import datetime
from .. import db


class FlashcardCollection(db.Model):
    __tablename__ = 'flashcardcollection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Flashcard Collection: %r>' % self.name
