from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class FlashcardCollectionForm(FlaskForm):
    name = StringField('Collection name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add')


class FlashcardForm(FlaskForm):
    question = PageDownField('Question', validators=[DataRequired()])
    answer = PageDownField('Answer', validators=[DataRequired()])
    next = BooleanField('Next Flashcard?')
    submit = SubmitField('Add')

