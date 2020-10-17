from functools import wraps
from flask import session, redirect, abort


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
        if  session['username'] != 'admin':
            return abort(403)
        return function(**kwargs)

    return wrapped_function


def admin_or_owner_required(function):
    @wraps(function)
    def wrapped_function(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        if session["username"] != "admin" and int(kwargs['user_id']) != session["id"]:
            return abort(403)
        return function(**kwargs)

    return wrapped_function
