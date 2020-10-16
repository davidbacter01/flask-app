from exceptions import exceptions
from flask import Blueprint, redirect, render_template, request, session
from services.services import Services
from views.views_decorators.authorization import login_required, setup_required



login_views_blueprint = Blueprint('login_views', __name__)


@login_views_blueprint.before_request
@setup_required
def check_setup():
    config = Services.get_service(Services.config)
    if not config.is_configured:
        return redirect('/setup')
    return None



@login_views_blueprint.route('/login', methods=['GET', 'POST'])
@setup_required
def log_in():
    if request.method == 'GET':
        return render_template('login.html')

    authentificator = Services.get_service(Services.authentification)
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        authentificator.login(name, email, password)
    except exceptions.InvalidLoginError as error:
        return render_template('login.html', message=error.args)
    return redirect('/index')


@login_views_blueprint.route('/logout')
@setup_required
@login_required
def log_out():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/index')
