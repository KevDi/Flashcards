from .. import db
from markdown import markdown
from flask import url_for
import bleach


class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    question_html = db.Column(db.Text)
    answer = db.Column(db.Text)
    answer_html = db.Column(db.Text)
    right_answered = db.Column(db.Boolean, default=False)
    wrong_answered = db.Column(db.Boolean, default=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('flashcardcollection.id'))

    @staticmethod
    def on_changed_question(target, value, oldvalue, initiator):
        allowed_tags = ['abbr', 'acronym', 'b', 'blockquote', 'code', 'i',
                        'li', 'ol', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.question_html = bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True)

    @staticmethod
    def on_changed_answer(target, value, oldvalue, initiator):
        allowed_tags = ['abbr', 'acronym', 'b', 'blockquote', 'code', 'i',
                        'li', 'ol', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.answer_html = bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True)

    def to_json(self):
        json_flashcard = {
            'url': url_for('api.get_flashcard', id=self.id, _external=True),
            'question': self.question,
            'question_html': self.question_html,
            'answer': self.answer,
            'answer_html': self.answer_html,
            'right_answered': self.right_answered,
            'wrong_answered': self.wrong_answered,
            'collection': url_for('api.get_collection', id=self.collection_id, _external=True),
        }
        return json_flashcard

    def __repr__(self):
        return '<Flashcard: %r>' % self.id


db.event.listen(Flashcard.answer, 'set', Flashcard.on_changed_answer)
db.event.listen(Flashcard.question, 'set', Flashcard.on_changed_question)
