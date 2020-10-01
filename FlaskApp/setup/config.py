from configparser import ConfigParser
from os import path


class Config:
    '''used for managing database.ini file for configuring database'''

    def __init__(self):
        self.config = ConfigParser()
        self.is_configured = path.exists('setup/database.ini')


    def save_configuration(self, config_dict: dict):
        '''creates database.ini and saves configuration inside it'''

        if not self.is_configured:
            open('setup/database.ini', 'w+').close()

        self.config.add_section('postgres')

        self.config['postgres']['host'] = config_dict.get('host')
        self.config['postgres']['dbname'] = config_dict.get('dbname')
        self.config['postgres']['user'] = config_dict.get('user')
        self.config['postgres']['password'] = config_dict.get('password')
        with open('setup/database.ini', 'w') as configfile:
            self.config.write(configfile)

        self.is_configured = True


    def get_configuration(self, filename='setup/database.ini', section='postgres'):
        '''returns a dict with db configuration from .ini file'''

        self.config.read(filename)
        configuration = {}
        if self.config.has_section(section):
            params = self.config.items(section)
            for param in params:
                configuration[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return configuration
