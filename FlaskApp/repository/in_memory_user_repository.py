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


    def add(self, user):
        if user not in self.users:
            self.users.insert(0, user)


    def edit(self, user: User):
        for us in self.users:
            if us.user_id == user.user_id:
                us = user


    def get_all(self):
        return self.users


    def get_by_id(self, user_id):
        for us in self.users:
            if us.user_id == user_id:
                return us

        return None

    def remove(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)

