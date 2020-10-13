from exceptions import exceptions
from repository.user_repository_interface import UserRepositoryInterface
from models.user import User


class InMemoryUserRepository(UserRepositoryInterface):
    """class containing users and specific methods"""

    def __init__(self):
        self.users = [
            User(1, 'admin', 'admin@email.com', 'secret'),
            User(2, 'test_user_1', 'test_1@email.com', 'test1'),
            User(3, 'test_user_2', 'test_2@email.com', 'test2'),
            User(4, 'deleted', 'del@email.com', 'delete')
            ]


    def add(self, user: User):
        self.__ensure_unicity(user)
        self.users.insert(0, user)


    def edit(self, user: User):
        self.__ensure_unicity(user)
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

    def get_by_name(self, name):
        for usr in self.users:
            if usr.name == name:
                return usr
        return None

    def remove(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)


    def __ensure_unicity(self, user: User):
        for usr in self.users:
            if usr.name == user.name and usr.user_id != user.user_id:
                raise exceptions.UserExistsError
            if usr.email == user.email and usr.user_id != user.user_id:
                raise exceptions.EmailExistsError
