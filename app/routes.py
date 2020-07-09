from flask import render_template, flash, redirect

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


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data,
                form.remember_me.data
            )
        )
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
