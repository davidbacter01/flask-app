from functools import wraps
from flask import render_template
from services.services import Services


def setup_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if not Services.get_service(Services.config).is_configured:
            return render_template('db_setup.html')
        return function(**kwargs)
    return wrapped_function
