from setup.config import Config
from models.database_settings import DatabaseSettings


class DbConfig(Config):

    def save_dbsettings(self, dbsettings: DatabaseSettings):
        settings = {
            'dbname': dbsettings.db_name,
            'host': dbsettings.host,
            'user': dbsettings.user,
            'password': dbsettings.password
        }

        return super().save_configuration(settings)

    def get_database_settings(self):
        credentials_dict = super().get_configuration()
        return DatabaseSettings(
            credentials_dict['dbname'],
            credentials_dict['user'],
            credentials_dict['password'])

    def get_uri(self):
        creds = super().get_configuration()
        return f"postgres+psycopg2://{creds['user']}:" +\
            f"{creds['password']}@localhost:5432/{creds['dbname']}"

    def get_version(self):
        try:
            return super().get_configuration()['version']
        except KeyError:
            return '1'

    def update_current_version(self, new_version):
        super().save_configuration(new_version)
