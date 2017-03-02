from .. import db

has_category = db.Table('has_category',
                        db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                        db.Column('flashcardcollection_id', db.Integer, db.ForeignKey('flashcardcollection.id')))
