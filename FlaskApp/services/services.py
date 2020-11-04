from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_users_repository import InMemoryUsersRepository
from repository.database_users_repository import DatabaseUsersRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from setup.database import Database
from setup.dbconfig import DbConfig
from services.authentification import Authentification
from database.post import Base


def return_false():
    return False


class Services:
    posts = 'posts'
    config = 'config'
    users = 'users'
    authentification = 'authentification'
    database = 'database'
    TESTING = False
    db = Database(DbConfig('postgres'))
    test_db = Mock()
    test_db.new_version_available = return_false
    engine = create_engine(db.config.get_uri())
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    production_users = DatabaseUsersRepository(db, Session)
    test_posts = InMemoryPostsRepository()
    test_users = InMemoryUsersRepository(test_posts)
    test_posts.users = test_users

    testing_services = {
        posts: test_posts,
        config: Mock(),
        users: test_users,
        authentification: Authentification(test_users),
        database: test_db
    }

    production_services = {
        posts: DatabasePostsRepository(db, Session),
        config: DbConfig('postgres'),
        users: production_users,
        authentification: Authentification(production_users),
        database: db
    }

    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]
        return Services.production_services[service_name]
