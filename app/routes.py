from flask import render_template

from app import webapp
from app.forms import LoginForm


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


@webapp.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
