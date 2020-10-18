import abc
from models.user import User


class UsersRepositoryInterface(abc.ABC):

    """interface for user repository"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_by_id') and
                callable(subclass.get_by_id) and
                hasattr(subclass, 'get_all') and
                callable(subclass.get_all) and
                hasattr(subclass, 'add_user') and
                callable(subclass.add_user) and
                hasattr(subclass, 'remove_user') and
                callable(subclass.remove_user) and
                hasattr(subclass, 'get_by_name') and
                callable(subclass.get_by_name)and
                hasattr(subclass, 'edit_user') and
                callable(subclass.edit_user) or
                NotImplemented)


    @abc.abstractmethod
    def get_by_id(self, user_id: int):
        pass


    @abc.abstractmethod
    def get_by_name(self, name: str):
        pass


    @abc.abstractmethod
    def get_all(self):
        pass


    @abc.abstractmethod
    def add(self, user: User):
        pass


    @abc.abstractmethod
    def remove(self, user_id):
        pass


    @abc.abstractmethod
    def update(self, user: User):
        pass
