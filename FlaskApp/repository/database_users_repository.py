from datetime import datetime
from exceptions import exceptions
from repository.users_repository_interface import UsersRepositoryInterface
from setup.database import Database
from services.password_manager import PasswordManager
from database.crud import Session
from database.models import User


class DatabaseUsersRepository(UsersRepositoryInterface):
    """class that can access the users table in db"""

    def __init__(self, database: Database):
        self.database = database
        self.session = Session

    def add(self, user: User):
        """adds user to database, raises error if email or name is duplicate"""
        self.__ensure_uniqueness(user)
        session = self.session()
        new_entry = User(
            id=user.user_id,
            name=user.name,
            email=user.emal,
            password=user.password,
            created_at=user.created_at,
            modified_at=user.modified_at
            )
        session.add(new_entry)
        session.commit()
        session.close()

    def update(self, user: User):
        """updates the user in db that has same id as the arg User"""
        session = self.session()
        entry = session.query(User).filter_by(id=user.user_id).first()
        invalid_passwords = ('', ' ', None)
        if user.name is not None and user.name != 'admin':
            entry.name = user.name
        if user.password not in invalid_passwords:
            entry.password = PasswordManager.hash(user.password)
        entry.email = user.email
        entry.modified_at = datetime.now()
        session.commit()
        session.close()

    def get_all(self):
        """returns a list of User objects from db"""
        session = self.session()
        result = session.query(User).all()
        session.commit()
        session.close()
        return result

    def get_by_id(self, user_id):
        """returns a User object from db that has the specified id"""
        session = self.session()
        user = session.query(User).filter_by(id=user_id).first()
        session.commit()
        session.close()
        return user

    def get_by_name(self, name):
        session = self.session()
        user = session.query(User).filter_by(name=name).first()
        session.commit()
        session.close()
        return user

    def get_by_email(self, email):
        session = self.session()
        user = session.query(User).filter_by(email=email).first()
        session.commit()
        session.close()
        return user

    def remove(self, user_id):
        """removes from db the user that has the specified id"""
        session = self.session()
        session.query(User).filter_by(id=user_id).first().delete()
        session.commit()
        session.close()

    def __ensure_uniqueness(self, user: User):
        users = self.get_all()
        for usr in users:
            if usr.name == user.name and usr.user_id != user.user_id:
                raise exceptions.UserExistsError('duplicate username')
            if usr.email == user.email and usr.user_id != user.user_id:
                raise exceptions.EmailExistsError('duplicate email')
        return True
