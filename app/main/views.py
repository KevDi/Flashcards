from flask import render_template, redirect, url_for, abort, flash, jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from ..models.users import User
from ..models.category import Category
from ..models.flashcard_collections import FlashcardCollection
from ..models.flashcard import Flashcard
from . import main
from .. import db
from .forms import FlashcardCollectionForm, FlashcardForm, EditFlashcardForm
from random import choice


@main.route('/')
def index():
    if current_user.is_authenticated:
        collections = current_user.collections.order_by(FlashcardCollection.timestamp.desc()).all()
    else:
        collections = []
    return render_template('index.html', collections=collections)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    collections = current_user.collections.order_by(FlashcardCollection.timestamp.desc()).all()
    return render_template('user.html', user=user, collections=collections)


@main.route('/add-collection', methods=['GET', 'POST'])
@login_required
def add_collection():
    form = FlashcardCollectionForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.category.data).first()
        if category is None:
            category = Category(name=form.category.data)
        collection = FlashcardCollection(name=form.name.data)
        collection.categories.append(category)
        collection.user = current_user
        db.session.add(collection)
        db.session.commit()
        flash('Flashcard Collection added.')
        return redirect(url_for('.index'))
    return render_template('add_collection.html', form=form)


@main.route('/get-category', methods=['GET', 'POST'])
@login_required
def get_category():
    return jsonify({
        'category': [category.name for category in Category.query.order_by(Category.name).all()]
    })


@main.route('/flashcardcollection/<int:id>')
@login_required
def flashcardcollection(id):
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    return render_template('flashcardcollection.html', flashcardcollection=flashcardcollection)


@main.route('/flashcardcollection/<int:id>/add-flashcard', methods=['GET', 'POST'])
@login_required
def add_flashcard(id):
    form = FlashcardForm()
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    if form.validate_on_submit():
        card = Flashcard(question=form.question.data, answer=form.answer.data)
        flashcardcollection.flashcards.append(card)
        db.session.add(flashcardcollection)
        db.session.commit()
        flash('Flashcard added to the Collection {0}'.format(flashcardcollection.name))
        if form.next.data:
            return redirect(url_for('.add_flashcard', id=flashcardcollection.id))
        else:
            return redirect(url_for('.flashcardcollection', id=flashcardcollection.id))
    return render_template('add_flashcard.html', form=form, name=flashcardcollection.name)


@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>')
@login_required
def flashcard(collId, cardId):
    flashcardcollection = FlashcardCollection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    return render_template('flashcard.html', flashcardcollection=flashcardcollection, flashcard=flashcard)


@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>/edit', methods=['GET', 'POST'])
@login_required
def edit_flashcard(collId, cardId):
    form = EditFlashcardForm()
    flashcardcollection = FlashcardCollection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    if form.validate_on_submit():
        flashcard.question = form.question.data
        flashcard.answer = form.answer.data
        db.session.add(flashcard)
        db.session.commit()
        flash('Flashcard was updated.')
        return redirect(url_for('.flashcard', collId=collId, cardId=cardId))
    form.question.data = flashcard.question
    form.answer.data = flashcard.answer
    return render_template('edit_flashcard.html', form=form, flashcard=flashcard)


@main.route('/flashcardcollection/<int:id>/learn')
@login_required
def learn(id):
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    flashcard = choice(flashcardcollection.flashcards.all())
    return render_template('learn.html', flashcard=flashcard, name=flashcardcollection.name)
