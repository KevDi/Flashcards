from flask import render_template, redirect, url_for, abort
from flask_login import login_required
from ..models.users import  User
from . import main
from .. import db


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)