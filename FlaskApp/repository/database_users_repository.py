from datetime import datetime
from exceptions import exceptions
from repository.users_repository_interface import UsersRepositoryInterface
from models.user import User
from setup.database import Database
from services.password_manager import PasswordManager


class DatabaseUsersRepository(UsersRepositoryInterface):
    """class that can access the users table in db"""

    def __init__(self, database: Database):
        self.database = database

    def add(self, user: User):
        '''adds user to database, raises error if email or name is duplicate'''
        self.__ensure_unicity(user)
        conn = self.database.connect()
        curs = conn.cursor()
        query = '''INSERT INTO users (name,
                email, password, created_at, modified_at)
                VALUES (%s, %s, %s, %s, %s)'''
        values = (user.name, user.email, user.password,
                  datetime.now(), user.modified_at)
        curs.execute(query, values)
        conn.commit()
        curs.close()
        conn.close()

    def update(self, user: User):
        '''updates the user in db that has same id as the arg User'''
        conn = self.database.connect()
        curs = conn.cursor()
        query = 'UPDATE users SET '
        values = ()
        invalid_passwords = ('', ' ', None)
        if user.name is not None and user.name != 'admin':
            query += f'name={user.name} '
        if user.password in invalid_passwords:
            query += ' email=%s, modified_at=%s WHERE id=%s '
            values = (user.email, datetime.now(), user.user_id)
        else:
            query += 'password=%s, email=%s, modified_at=%s WHERE id=%s '
            values = (PasswordManager.hash(user.password), user.email, datetime.now(), user.user_id)
        curs.execute(query, values)
        conn.commit()
        curs.close()
        conn.close()

    def get_all(self):
        '''returns a list of User objects from db'''
        conn = self.database.connect()
        conn.autocommit = True
        curs = conn.cursor()
        users = []
        curs.execute('''SELECT * FROM users''')
        db_entries = curs.fetchall()
        for entry in db_entries:
            user = User(entry[0], entry[1], entry[2], entry[3])
            user.created_at = entry[4]
            user.modified_at = entry[5]
            users.append(user)

        curs.close()
        conn.close()
        return users

    def get_by_id(self, user_id):
        '''returns a User object from db that has the specified id'''
        conn = self.database.connect()
        conn.autocommit = True
        curs = conn.cursor()
        query = '''SELECT * FROM users WHERE id = %s'''
        values = (user_id,)
        curs.execute(query, values)
        db_entry = curs.fetchone()
        user = User(db_entry[0], db_entry[1], db_entry[2], db_entry[3])
        user.created_at = db_entry[4]
        user.modified_at = db_entry[5]
        curs.close()
        conn.close()
        return user

    def get_by_name(self, name):
        conn = self.database.connect()
        conn.autocommit = True
        curs = conn.cursor()
        query = '''SELECT * FROM users WHERE name = %s'''
        values = (name,)
        curs.execute(query, values)
        db_entry = curs.fetchone()
        if db_entry is None:
            curs.close()
            conn.close()
            return None
        user = User(db_entry[0], db_entry[1], db_entry[2], db_entry[3])
        user.created_at = db_entry[4]
        user.modified_at = db_entry[5]
        curs.close()
        conn.close()
        return user

    def get_by_email(self, email):
        conn = self.database.connect()
        conn.autocommit = True
        curs = conn.cursor()
        query = '''SELECT * FROM users WHERE email = %s'''
        values = (email,)
        curs.execute(query, values)
        db_entry = curs.fetchone()
        if db_entry is None:
            curs.close()
            conn.close()
            return None
        user = User(db_entry[0], db_entry[1], db_entry[2], db_entry[3])
        user.created_at = db_entry[4]
        user.modified_at = db_entry[5]
        curs.close()
        conn.close()
        return user

    def remove(self, user_id):
        '''removes from db the user that has the specified id'''
        conn = self.database.connect()
        curs = conn.cursor()
        query = '''DELETE FROM users WHERE id = %s'''
        curs.execute(query, (user_id,))
        conn.commit()
        curs.close()
        conn.close()

    def __ensure_unicity(self, user: User):
        users = self.get_all()
        for usr in users:
            if usr.name == user.name and usr.user_id != user.user_id:
                raise exceptions.UserExistsError('duplicate username')

            if usr.email == user.email and usr.user_id != user.user_id:
                raise exceptions.EmailExistsError('duplicate email')

        return True
