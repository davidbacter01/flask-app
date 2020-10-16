from exceptions import exceptions
from flask import session
from passlib.hash import sha256_crypt
from repository.users_repository_interface import UsersRepositoryInterface


class Authentification:
    """manages login operations"""

    def __init__(self, user_repo: UsersRepositoryInterface):
        self.users = user_repo
        self.crypter = sha256_crypt


    def login(self, name, email, password):
        user = self.users.get_by_name(name)
        message = 'Invalid username, email or password!'
        if user is None:
            raise exceptions.InvalidLoginError(message)
        if not self.password_equality(password, user.password):
            raise exceptions.InvalidLoginError(message)
        if user.email == email:
            session['username'] = name
            session['user_id'] = user.user_id
        else:
            raise exceptions.InvalidLoginError(message)


    def hash(self, password):
        password = self.crypter.encrypt("password")
        return password


    def password_equality(self, password, hashed_password):
        return self.crypter.verify(password, hashed_password)
