import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from setup.config import Config

class Database():
    """creates a database instance"""
    def __init__(self):
        self.config = Config()
        self.credentials = self.config.get_configuration()

    def connect(self):
        #credentials = self.config.get_configuration()
        try:
            conn = psycopg2.connect(**self.credentials)
            return conn
        except psycopg2.DatabaseError:
            self.create_db()
            conn = psycopg2.connect(**self.credentials)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            curs=conn.cursor()
            curs.execute('''CREATE TABLE IF NOT EXISTS posts
                    (id SERIAL PRIMARY KEY UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    contents TEXT NOT NULL,
                    created_at TIMESTAMP,
                    modified_at TIMESTAMP)''')
            curs.close()
            return conn


    def create_db(self):
        conn = psycopg2.connect(user=self.credentials['user'], password=self.credentials['password'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        curs.execute('''CREATE DATABASE {}'''.format(self.credentials['dbname']))
        curs.close()
        conn.close()
