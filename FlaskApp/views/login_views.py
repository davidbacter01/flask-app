from exceptions import exceptions
from flask import Blueprint, redirect, render_template, request
from services.services import Services
from views.views_decorators.authorization import login_required
from views.views_decorators.setup_required import setup_required


login_views_blueprint = Blueprint('login_views', __name__)


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
    except ValueError:
        message = 'You must complete user info before first login!'
        user = Services.get_service(Services.users).get_by_name(name)
        return render_template('legacy_user_setup.html', message=message, user=user)
    except exceptions.InvalidLoginError as error:
        return render_template('login.html', message=error.args)
    return redirect('/index')


@login_views_blueprint.route('/logout')
@setup_required
@login_required
def log_out():
    authentificator = Services.get_service(Services.authentification)
    authentificator.logout()
    return redirect('/index')
