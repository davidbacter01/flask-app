from configparser import ConfigParser
from os import path
from exceptions.exceptions import SectionNotFoundError


class Config:
    """used for managing database.ini file for configuring database"""

    def __init__(self, section: str):
        self.config = ConfigParser()
        self.file_name = 'config.ini'
        self.section = section
        self.is_configured = path.exists(f'setup/{self.file_name}')

    def save_configuration(self, config_dict: dict):
        """creates database.ini and saves configuration inside it"""

        if not self.is_configured:
            open(f'setup/{self.file_name}', 'w+').close()

        if not self.config.has_section(self.section):
            self.config.add_section(self.section)
        for key in config_dict:
            self.config[self.section][key] = config_dict[key]

        with open(f'setup/{self.file_name}', 'w') as configfile:
            self.config.write(configfile)

        self.is_configured = True

    def get_configuration(self):
        """returns a dict with configuration from .ini file"""
        filename = f'setup/{self.file_name}'
        self.config.read(filename)
        configuration = {}
        if self.config.has_section(self.section):
            params = self.config.items(self.section)
            for param in params:
                configuration[param[0]] = param[1]
        else:
            raise SectionNotFoundError(
                'Section {0} not found in the {1} file'.format(self.section, filename))

        return configuration
