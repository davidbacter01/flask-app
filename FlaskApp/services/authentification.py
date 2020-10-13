from exceptions import exceptions
from flask import session
from passlib.hash import sha256_crypt
from repository.user_repository_interface import UserRepositoryInterface


class Authentification:
    """manages login operations"""

    def __init__(self, user_repo: UserRepositoryInterface):
        self.users = user_repo
        self.crypt = sha256_crypt


    def login(self, name, email, password):
        hashed = self.hash(password)
        user = self.users.get_by_name(name)
        if user is None:
            raise exceptions.InvalidLoginError
        if user.email == email and user.password == hashed:
            session['username'] = name
            session['user_id'] = user.user_id
        else:
            raise exceptions.InvalidLoginError


    def hash(self, password):
        password = self.crypt.encrypt("password")
        return password


    def check_password_equality(self, password, hashed_password):
        return self.crypt.verify(password, hashed_password)
