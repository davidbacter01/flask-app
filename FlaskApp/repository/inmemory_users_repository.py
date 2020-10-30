from passlib.hash import sha256_crypt

from exceptions import exceptions
from models.user import User
from repository.users_repository_interface import UsersRepositoryInterface


class InMemoryUsersRepository(UsersRepositoryInterface):
    """class containing users and specific methods"""

    def __init__(self, posts_repository):
        self.users = [
            User(1, 'admin', 'admin@email.com', sha256_crypt.hash('secret')),
            User(2, 'test_user_1', 'test_1@email.com', sha256_crypt.hash('test1')),
            User(3, 'test_user_2', 'test_2@email.com', sha256_crypt.hash('test2')),
            User(4, 'deleted', 'del@email.com', 'delete'),
            User(5, 'user', '1', '1'),
            User(6, 'edit', 'edit@email.com', sha256_crypt.hash('edit')),
            User(7, 'delete', 'delete', sha256_crypt.hash('delete')),
            User(8, 'testdelete', '1', '1'),
            User(9, 'User1', 'user1', sha256_crypt.hash('secret')),
            User(10, 'User2', 'ads', sha256_crypt.hash('secret')),
            User(11, 'User3', 'asd', sha256_crypt.hash('secret')),
            User(12, 'test_user_2', 'asf', sha256_crypt.hash('secret')),
            User(13, 'are', 'qwe', sha256_crypt.hash('secret'))
        ]
        self.posts = posts_repository

    def add(self, user: User):
        self.__ensure_uniqueness(user)
        self.users.insert(0, user)

    def update(self, user: User):
        self.__ensure_uniqueness(user)
        for usr in self.users:
            if usr.user_id == user.user_id:
                self.users.remove(usr)
                self.users.append(user)

    def get_all(self):
        return self.users

    def get_by_id(self, user_id):
        for usr in self.users:
            if usr.user_id == user_id:
                return usr
        return None

    def get_by_name(self, name):
        for usr in self.users:
            if usr.name == name:
                return usr
        return None

    def get_by_email(self, email):
        for usr in self.users:
            if usr.email == email:
                return usr
        return None

    def remove(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
        for post in self.posts.posts:
            if post.owner == user_id:
                self.posts.remove(post.blog_id)

    def __ensure_uniqueness(self, user: User):
        for usr in self.users:
            if usr.name == user.name and usr.user_id != user.user_id:
                raise exceptions.UserExistsError
            if usr.email == user.email and usr.user_id != user.user_id:
                raise exceptions.EmailExistsError
