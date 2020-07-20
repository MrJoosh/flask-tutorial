from flask import Blueprint

bp = Blueprint(
    name='errors',
    import_name=__name__,
    template_folder='templates'
    )

from app.errors import handlers
