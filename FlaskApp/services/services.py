from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from repository.in_memory_user_repository import InMemoryUserRepository
from repository.database_user_repository import DatabaseUserRepository
from setup.database import Database
from setup.dbconfig import DbConfig


class Services:
    posts = 'posts'
    config = 'config'
    users = 'users'
    TESTING = False
    db = Database(DbConfig('postgres'))

    testing_services = {
        posts:InMemoryPostsRepository(),
        config:Mock(),
        users:InMemoryUserRepository()
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:DbConfig('postgres'),
        users:DatabaseUserRepository(db)
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]

        return Services.production_services[service_name]
