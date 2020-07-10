from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import webapp, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@webapp.route('/')
@webapp.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)


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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@webapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
