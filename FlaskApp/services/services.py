from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from repository.inmemory_users_repository import InMemoryUsersRepository
from repository.database_users_repository import DatabaseUsersRepository
from setup.database import Database
from setup.dbconfig import DbConfig
from services.authentification import Authentification


class Services:
    posts = 'posts'
    config = 'config'
    users = 'users'
    authentification = 'authentification'
    TESTING = False
    db = Database(DbConfig('postgres'))
    production_users = DatabaseUsersRepository(db)
    test_users = InMemoryUsersRepository()

    testing_services = {
        posts:InMemoryPostsRepository(),
        config:Mock(),
        users:test_users,
        authentification:Authentification(test_users)
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:DbConfig('postgres'),
        users:production_users,
        authentification:Authentification(production_users)
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]
        return Services.production_services[service_name]
