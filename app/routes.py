from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user

from app import webapp
from app.forms import LoginForm
from app.models import User


@webapp.route('/')
@webapp.route('/index')
def index():
    user = {'username': 'Josh'}
    posts = [
        {
            'author': {'username': 'Olly'},
            'body': 'Beautiful day in Littleborough!'
        },
        {
            'author': {'username': 'Jorja'},
            'body': 'Josh is the coolest!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
