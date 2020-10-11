from exceptions import exceptions
from flask import Blueprint, redirect, render_template, request, session, abort
from services.services import Services
from models.user import User



user_views_blueprint = Blueprint('user_views', __name__)


@user_views_blueprint.route('/list_users')
def list_users():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return abort(403)
    users = Services.get_service(Services.users).get_all()
    return render_template('list_users.html', users=users)


@user_views_blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')

    users = Services.get_service(Services.users)
    user_data = request.form
    if user_data.get('password') != user_data.get('confirm_password'):
        message = 'Passwords do not match'
        return render_template('create_user.html', message=message)

    user = User(
        None,
        user_data.get('name'),
        user_data.get('email'),
        user_data.get('password')
        )
    try:
        users.add(user)
    except exceptions.UserExistsError:
        message = 'Duplicate user name!'
        return render_template('create_user.html', message=message)
    except exceptions.EmailExistsError:
        message = 'Duplicate email!'
        return render_template('create_user.html', message=message)

    return render_template('list_users.html', users=users.get_all())


@user_views_blueprint.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
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

    return redirect('/list_users')

@user_views_blueprint.route('/delete_user/<user_id>')
def delete_user(user_id):
    posts = Services.get_service(Services.users)
    posts.remove(user_id)
    return redirect('/list_users')
