from configparser import ConfigParser
from os import path


class Config:
    '''used for managing database.ini file for configuring database'''

    def __init__(self, file_name):
        self.config = ConfigParser()
        self.file_name = file_name
        self.is_configured = path.exists(f'setup/{self.file_name}')


    def save_configuration(self, section_name: str, config_dict: dict):
        '''creates database.ini and saves configuration inside it'''

        if not self.is_configured:
            open(f'setup/{self.file_name}', 'w+').close()

        self.config.add_section(section_name)
        for key in config_dict:
            self.config[section_name][key] = config_dict[key]

        with open(f'setup/{self.file_name}', 'w') as configfile:
            self.config.write(configfile)

        self.is_configured = True


    def get_configuration(self, filename, section):
        '''returns a dict with configuration from .ini file'''

        self.config.read(filename)
        configuration = {}
        if self.config.has_section(section):
            params = self.config.items(section)
            for param in params:
                configuration[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return configuration
