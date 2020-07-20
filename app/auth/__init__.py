from flask import Blueprint

bp = Blueprint(
    name='auth',
    import_name=__name__,
    template_folder='templates'
)

from app.auth import routes