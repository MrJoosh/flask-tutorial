from flask import render_template

from app import webapp, db


@webapp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@webapp.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # pylint: disable=no-member
    return render_template('500.html'), 500
