from app import webapp

@webapp.route('/')
@webapp.route('/index')
def index():
    return "Hello, world!"

