from exceptions import exceptions
from flask import Blueprint, redirect, render_template, request, url_for
from services.password_manager import PasswordManager
from services.services import Services
from models.user import User
from views.views_decorators import authorization


users_views_blueprint = Blueprint('users_views', __name__, url_prefix='/users')

@users_views_blueprint.route('/view/<int:user_id>')
@authorization.setup_required
@authorization.admin_or_owner_required
def view_user(user_id):
    user = Services.get_service(Services.users).get_by_id(user_id)
    return render_template('view_user.html', user=user)


@users_views_blueprint.route('/list')
@authorization.setup_required
@authorization.admin_required
def list_users():
    users = Services.get_service(Services.users).get_all()
    return render_template('list_users.html', users=users)


@users_views_blueprint.route('/new', methods=['GET', 'POST'])
@authorization.setup_required
@authorization.admin_required
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')

    users = Services.get_service(Services.users)
    user_data = request.form
    if user_data.get('password') != user_data.get('confirm_password'):
        message = 'Passwords do not match'
        return render_template('create_user.html', message=message)

    password = PasswordManager.hash(user_data.get('password'))
    user = User(
        None,
        user_data.get('name'),
        user_data.get('email'),
        password)
    try:
        users.add(user)
    except exceptions.UserExistsError:
        message = 'Duplicate user name!'
        return render_template('create_user.html', message=message)
    except exceptions.EmailExistsError:
        message = 'Duplicate email!'
        return render_template('create_user.html', message=message)

    return render_template('list_users.html', users=users.get_all())


@users_views_blueprint.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@authorization.setup_required
@authorization.admin_or_owner_required
def edit_user(user_id):
    users = Services.get_service(Services.users)
    user = users.get_by_id(user_id)
    if request.method == 'GET':
        return render_template('edit_user.html', user=user)

    user_data = request.form
    user = User(
        user_data.get('user_id'),
        user_data.get('name'),
        user_data.get('email'),
        user_data.get('password')
        )

    try:
        users.edit(user)
    except exceptions.UserExistsError:
        message = 'Duplicate user!'
        return render_template('edit_user.html', user=user, message=message)
    except exceptions.EmailExistsError:
        message = 'Duplicate email!'
        return render_template('edit_user.html', user=user, message=message)

    return redirect(url_for('users_views.list_users'))

@users_views_blueprint.route('/delete/<int:user_id>')
@authorization.setup_required
@authorization.admin_required
def delete_user(user_id):
    posts = Services.get_service(Services.users)
    posts.remove(user_id)
    return redirect(url_for('users_views.list_users'))
