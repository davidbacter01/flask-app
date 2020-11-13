from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_users_repository import InMemoryUsersRepository
from repository.database_users_repository import DatabaseUsersRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from repository.disk_image_repository import DiskImageRepository
from repository.inmemory_image_repository import InMemoryImageRepository
from setup.database import Database
from setup.dbconfig import DbConfig
from services.authentification import Authentification
from services.file_validator import FileValidator
from services.password_manager import PasswordManager
from services.statistics import Statistics
from database.post import Base


def return_false():
    return False


class Services:
    posts = 'posts'
    config = 'config'
    users = 'users'
    authentification = 'authentification'
    database = 'database'
    file_validator = 'validator'
    pw_manager = 'pw_manager'
    image_repo = 'image_repo'
    statistics = 'statistics'
    TESTING = True
    db = Database(DbConfig('postgres'))
    test_db = Mock()
    test_db.new_version_available = return_false
    engine = create_engine(db.config.get_uri())
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    pass_manager = PasswordManager(sha256_crypt)
    production_users = DatabaseUsersRepository(db, Session, pass_manager)
    production_image_repo = DiskImageRepository('./static/img')
    prod_posts = DatabasePostsRepository(db, Session, production_image_repo)
    production_statistics = Statistics(production_users, prod_posts)
    testing_image_repo = InMemoryImageRepository()
    test_posts = InMemoryPostsRepository(users_repository=None, img_repo=testing_image_repo)
    test_users = InMemoryUsersRepository(test_posts, pass_manager)
    test_auth = Authentification(test_users, pass_manager)
    prod_auth = Authentification(production_users, pass_manager)
    test_posts.users = test_users
    test_statistics = Statistics(test_users, test_posts)

    testing_services = {
        posts: test_posts,
        config: Mock(),
        users: test_users,
        authentification: test_auth,
        database: test_db,
        file_validator: Mock(),
        pw_manager: pass_manager,
        image_repo: testing_image_repo,
        statistics: test_statistics
    }

    production_services = {
        posts: prod_posts,
        config: DbConfig('postgres'),
        users: production_users,
        authentification: prod_auth,
        database: db,
        file_validator: FileValidator(["JPEG", "JPG", "PNG"]),
        pw_manager: pass_manager,
        image_repo: production_image_repo,
        statistics: production_statistics
    }

    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]
        return Services.production_services[service_name]
