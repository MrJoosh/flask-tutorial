from flask import render_template
from app import webapp


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
