from flask import session
from exceptions import exceptions
from repository.users_repository_interface import UsersRepositoryInterface


class Authentification:
    """manages login operations"""

    def __init__(self, user_repo: UsersRepositoryInterface, pw_manager):
        self.users = user_repo
        self.password_manager = pw_manager
        self.logged_in = None

    def login(self, name, password):
        user = self.users.get_by_name(name)
        message = 'Invalid username, email or password!'
        if user is None:
            user = self.users.get_by_email(name)
        if user is None:
            raise exceptions.InvalidLoginError(message)
        if not self.password_manager.verify(password, user.password):
            raise exceptions.InvalidLoginError(message)
        session['username'] = user.name
        session['user_id'] = user.user_id
        self.logged_in = user

    def logout(self):
        if self.logged_in or ('username' in session):
            session.pop('username', None)
            session.pop('user_id', None)
