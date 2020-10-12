from flask import Blueprint, redirect, render_template, request, session
from services.services import Services



login_views_blueprint = Blueprint('login_views', __name__)

@login_views_blueprint.before_request
def check_setup():
    config = Services.get_service(Services.config)
    if not config.is_configured:
        return redirect('/setup')
    return None


@login_views_blueprint.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'GET':
        return render_template('login.html')

    users = Services.get_service(Services.users).get_all()
    user = None
    message = ''
    for usr in users:
        if usr.name == request.form.get('name'):
            user = usr
        elif usr.email == request.form.get('email'):
            user = usr

    if user is None:
        message = 'Invalid credentials!'
        return render_template('login.html', message=message)

    if user.password != request.form.get('password'):
        return render_template('login.html', message=message)

    session['username'] = user.name
    session['user_id'] = user.user_id
    return redirect('/')


@login_views_blueprint.route('/logout')
def log_out():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')
