import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.dbconfig import DbConfig
from setup.db_version_2 import updates


class Database():
    """creates a database instance"""
    def __init__(self, config: DbConfig):
        self.config = config
        self.credentials = None
        self.latest_version = '2'

    def connect(self):
        self.credentials = self.config.get_database_settings()
        conn = psycopg2.connect(
            host=self.credentials.host,
            dbname=self.credentials.db_name,
            user=self.credentials.user,
            password=self.credentials.password
            )
        return conn


    def create_db(self):
        conn = psycopg2.connect(
            user=self.credentials.user,
            password=self.credentials.password
            )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        curs.execute('''CREATE DATABASE {}'''.format(self.credentials.db_name))
        curs.close()
        conn.close()


    def update(self):
        current_version = 0
        try:
            current_version = self.config.get_version()
        except KeyError:
            self.config.update_current_version(dict(version='1'))
        if current_version != self.latest_version:
            conn = self.connect()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curs = conn.cursor()
            for query in updates:
                curs.execute(query)
            curs.close()
            conn.close()
            self.config.update_current_version(dict(version=self.latest_version))


    def setup(self):
        self.credentials = self.config.get_database_settings()
        try:
            self.create_db()
        except psycopg2.DatabaseError:
            pass
        self.update()


    def new_version_available(self):
        return self.latest_version != self.config.get_version()
