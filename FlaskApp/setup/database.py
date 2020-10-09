import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database():
    """creates a database instance"""
    def __init__(self, config):
        self.config = config
        self.credentials = None

    def connect(self):
        self.credentials = self.config.get_configuration()
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


    def setup(self):
        self.credentials = self.config.get_configuration()
        try:
            self.create_db()
        except psycopg2.DatabaseError as e:
            print(e)
            pass

        conn = psycopg2.connect(
            dbname=self.credentials.db_name,
            user=self.credentials.user,
            password=self.credentials.password
            )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS posts
                (id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                title TEXT NOT NULL,
                owner TEXT NOT NULL,
                contents TEXT NOT NULL,
                created_at TIMESTAMP,
                modified_at TIMESTAMP)''')
        curs.close()
        conn.close()
