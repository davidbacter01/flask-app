from flask import Blueprint, redirect, render_template, request, session
from services.services import Services



log_views_blueprint = Blueprint('log_views', __name__)

@log_views_blueprint.route('/login', methods=['GET', 'POST'])
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
            message = 'Wrong username!'
            user = usr
        else:
            message = 'Username and email do not exist!'

    if user is None:
        return render_template('login.html', mesaage=message)

    if user.password != request.form.get('password'):
        return render_template('login.html', message='Wrong password!')

    session['username'] = user.name
    return redirect('/')


@log_views_blueprint.route('/logout')
def log_out():
    session.pop('username', None)
    return redirect('/')
