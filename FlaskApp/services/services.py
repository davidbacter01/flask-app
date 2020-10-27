from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_users_repository import InMemoryUsersRepository
from repository.database_users_repository import DatabaseUsersRepository
from setup.database import Database
from setup.dbconfig import DbConfig
from services.authentification import Authentification


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
    production_users = DatabaseUsersRepository(db)
    test_users = InMemoryUsersRepository()
    test_posts = test_users.posts


    testing_services = {
        posts:test_posts,
        config:Mock(),
        users:test_users,
        authentification:Authentification(test_users),
        database:test_db
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:DbConfig('postgres'),
        users:production_users,
        authentification:Authentification(production_users),
        database:db
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]
        return Services.production_services[service_name]
