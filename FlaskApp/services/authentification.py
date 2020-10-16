from exceptions import exceptions
from flask import session
from services.password_manager import PasswordManager
from repository.users_repository_interface import UsersRepositoryInterface


class Authentification:
    """manages login operations"""

    def __init__(self, user_repo: UsersRepositoryInterface):
        self.users = user_repo
        self.logged_in = None
        self.crypter = PasswordManager


    def login(self, name, email, password):
        user = self.users.get_by_name(name)
        message = 'Invalid username, email or password!'
        if user is None:
            raise exceptions.InvalidLoginError(message)
        if not self.verify(password, user.password):
            raise exceptions.InvalidLoginError(message)
        if user.email == email:
            session['username'] = name
            session['user_id'] = user.user_id
            self.logged_in = user
        else:
            raise exceptions.InvalidLoginError(message)


    def logout(self):
        if self.logged_in:
            session.pop('username', None)
            session.pop('user_id', None)

    def verify(self, password, hashed_password):
        return self.crypter.verify(password, hashed_password)
