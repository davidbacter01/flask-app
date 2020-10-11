from exceptions import exceptions
from repository.user_repository_interface import UserRepositoryInterface
from models.user import User


class InMemoryUserRepository(UserRepositoryInterface):
    """class containing users and specific methods"""

    def __init__(self):
        self.users = [
            User(1, 'admin', 'admin@email.com', 'secret'),
            User(2, 'test_user_1', 'test_1@email.com', 'test1'),
            User(3, 'test_user_2', 'test_2@email.com', 'test2')
            ]


    def add(self, user: User):
        for usr in self.users:
            if usr.name == user.name:
                raise exceptions.UserExistsError
            if usr.email == user.email:
                raise exceptions.EmailExistsError

        self.users.insert(0, user)


    def edit(self, user: User):
        for usr in self.users:
            if usr.user_id == user.user_id:
                usr = user


    def get_all(self):
        return self.users


    def get_by_id(self, user_id):
        for usr in self.users:
            if usr.user_id == user_id:
                return usr

        return None

    def remove(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
