from .. import db
from flask import url_for


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def to_json(self):
        json_category = {
            'url': url_for('api.get_category', id=self.id, _external=True),
            'name': self.name
        }
        return json_category

    def __repr__(self):
        return '<Category: %r>' % self.name
