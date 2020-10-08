from setup.config import Config
from models.database_settings import DatabaseSettings


class DbConfig(Config):
    def __init__(self):
        self.file_name = 'config.ini'
        super().__init__(self.file_name)


    def save_from_dbsetup(self, dbsettings: DatabaseSettings):
        settings = {
            'dbname':dbsettings.db_name,
            'host':dbsettings.host,
            'user':dbsettings.user,
            'password':dbsettings.password
            }

        return super().save_configuration(dbsettings.section, settings)


    def get_configuration(self, filename='setup/config.ini', section='postgres'):
        credentials_dict = super().get_configuration(filename, section)
        return DatabaseSettings(
            credentials_dict['dbname'],
            credentials_dict['user'],
            credentials_dict['password'])
