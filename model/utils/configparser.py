import configparser
from enum import Enum

from utils.entities.dto import DTO
from utils.filemanager import FileManager, FileType, DirPath

class SectionName(Enum):
    COLUMN = "Columns"
    PARAMETERS = "Parameters"

class ConfigParser:

    '''
        Select and read config from ../config
    '''
    def parse_config(self):
        manager = FileManager()

        filename = manager.select_file(DirPath.CONFIGS, FileType.CONFIG)
        path_to_file = manager.get_path_to_file(DirPath.CONFIGS)

        config = configparser.ConfigParser()

        if filename is not None:
            with open(path_to_file + "\\" + filename) as cfg_file:
                config.readfp(cfg_file)  # read and parse entire file

            sections = {}
            for section in config.sections():
                options = {}
                for option, value in config.items(section):
                    options[option] = value
                sections[section] = options

            column_names = self.get_column_names(sections)
            return DTO(filename, path_to_file, column_names, sections)
        return None

    '''
        Get column names by sections from parsed .config file
    '''
    def get_column_names(self, sections):
        names = []
        for section, options in sections.items():
            if section == SectionName.COLUMN.value:
                for option, value in options.items():
                    names.append(value)
        return names

    '''
        Print config DTO entity
    '''
    def print_config(self, config):
        for section, options in config.data.items():
            print(section)
            for option, value in options.items():
                print("     ", option, ":", value)
