from setup.config import Config
from models.database_settings import DatabaseSettings


class DbConfig(Config):

    def save_dbsettings(self, dbsettings: DatabaseSettings):
        settings = {
            'dbname':dbsettings.db_name,
            'host':dbsettings.host,
            'user':dbsettings.user,
            'password':dbsettings.password
            }

        return super().save_configuration(settings)


    def get_configuration(self):
        credentials_dict = super().get_configuration()
        return DatabaseSettings(
            credentials_dict['dbname'],
            credentials_dict['user'],
            credentials_dict['password'])


    def get_version(self):
        self.config.read(f'setup/{self.file_name}')
        if 'version' not in self.config.options('postgres'):
            self.config['postgres']['version'] = '1'
            with open('setup/config.ini', 'w') as configfile:
                self.config.write(configfile)
        return self.config['postgres']['version']
