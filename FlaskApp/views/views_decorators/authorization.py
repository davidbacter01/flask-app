from functools import wraps
from flask import session, redirect, abort
from services.services import Services


def login_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        return function(**kwargs)

    return wrapped_function


def admin_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        if session['username'] != 'admin':
            return abort(403)
        return function(**kwargs)

    return wrapped_function


def admin_or_account_owner_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        if session["username"] != "admin" and int(kwargs['user_id']) != session["user_id"]:
            return abort(403)
        return function(**kwargs)

    return wrapped_function


def admin_or_post_owner_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        blog = Services.get_service(Services.posts).get_by_id(kwargs['post_id'])
        owner = blog.owner
        if session['username'] != 'admin' and session['username'] != owner:
            return abort(403)
        return function(**kwargs)

    return wrapped_function
