from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from repository.in_memory_users_repository import InMemoryUsersRepository
from repository.database_users_repository import DatabaseUsersRepository
from setup.database import Database
from setup.dbconfig import DbConfig
from services.authentification import Authentification


class Services:
    posts = 'posts'
    config = 'config'
    users = 'users'
    TESTING = False
    db = Database(DbConfig('postgres'))

    testing_services = {
        posts:InMemoryPostsRepository(),
        config:Mock(),
        users:InMemoryUsersRepository()
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:DbConfig('postgres'),
        users:DatabaseUsersRepository(db)
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]
        return Services.production_services[service_name]


    @staticmethod
    def get_auth_service():
        if Services.TESTING:
            return Authentification(Services.testing_services[Services.users])
        return Authentification(Services.production_services[Services.users])
