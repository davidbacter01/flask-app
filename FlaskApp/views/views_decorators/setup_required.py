from functools import wraps
from flask import redirect
from services.services import Services


def setup_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if not Services.get_service(Services.config).is_configured:
            return redirect('/setup')
        return function(**kwargs)
    return wrapped_function
