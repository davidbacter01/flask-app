from datetime import datetime
from exceptions import exceptions
from repository.users_repository_interface import UsersRepositoryInterface
from setup.database import Database
from database.user import User
from models import user


class DatabaseUsersRepository(UsersRepositoryInterface):
    """class that can access the users table in db"""

    def __init__(self, database: Database, session, pw_manager):
        self.database = database
        self.session = session
        self.pw_manager = pw_manager

    def add(self, user: User):
        """adds user to database, raises error if email or name is duplicate"""
        self.__ensure_uniqueness(user)
        session = self.session()
        new_entry = User(
            id=user.user_id,
            name=user.name,
            email=user.email,
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
            entry.password = self.pw_manager.hash(user.password)
        entry.email = user.email
        entry.modified_at = datetime.now()
        session.commit()
        session.close()

    def get_all(self):
        """returns a list of User objects from db"""
        session = self.session()
        result = session.query(User).all()
        session.commit()
        res = []
        for usr in result:
            entry = user.User(usr.id,
                              usr.name,
                              usr.email,
                              usr.password)
            entry.created_at = usr.created_at
            entry.modified_at = usr.modified_at
            res.append(entry)
        session.close()
        return res

    def get_by_id(self, user_id):
        """returns a User object from db that has the specified id"""
        session = self.session()
        result = session.query(User).filter_by(id=user_id).first()
        session.commit()
        entry = user.User(result.id,
                          result.name,
                          result.email,
                          result.password)
        entry.created_at = result.created_at
        entry.modified_at = result.modified_at
        session.close()
        return entry

    def get_by_name(self, name):
        session = self.session()
        result = session.query(User).filter_by(name=name).first()
        session.commit()
        entry = user.User(result.id,
                          result.name,
                          result.email,
                          result.password)
        entry.created_at = result.created_at
        entry.modified_at = result.modified_at
        session.close()
        return entry

    def get_by_email(self, email):
        session = self.session()
        result = session.query(User).filter_by(email=email).first()
        session.commit()
        entry = user.User(result.id,
                          result.name,
                          result.email,
                          result.password)
        entry.created_at = result.created_at
        entry.modified_at = result.modified_at
        session.close()
        return entry

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
