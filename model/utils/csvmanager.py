import csv

from utils.configparser import ConfigParser
from utils.entities.dto import DTO
from utils.filemanager import FileManager, DirPath, FileType


class CSVManager:


    '''
        Read .csv file from ../stats/generated and into DTO entity
    '''
    def parse_csv(self):
        manager = FileManager()
        filename = manager.select_file(DirPath.STATISTICS, FileType.CSV)
        return self.parse_csv_with_name(filename)

    def parse_csv_with_name(self, filename):
        manager = FileManager()
        parser = ConfigParser()

        config_dto = parser.parse_config()
        path_to_file = manager.get_path_to_file(DirPath.STATISTICS)

        csv_dict = {}

        column_names = config_dto.column_names
        for name in column_names:
            csv_dict[name] = []

        csv_file = open(path_to_file + "\\" + filename, 'rt')

        csv_reader = csv.DictReader(csv_file, fieldnames=column_names, delimiter=';', quotechar='"')

        header = next(csv_reader)
        for row in csv_reader:
            for key in row:
                csv_dict[key].append(row[key])
        return DTO(filename, path_to_file, column_names, csv_dict)

    '''
        Write DTO entity with .csv to file
    '''
    def write_csv(self, csv_dto):
        with open(csv_dto.path + "\\" + csv_dto.filename, 'w') as fp:
            writer = csv.DictWriter(fp, csv_dto.column_names, delimiter=';')
            writer.writeheader()

            for i in range(0, len(csv_dto.data[csv_dto.column_names[0]])):
                row = {}
                for column in csv_dto.column_names:
                    values = csv_dto.data[column]
                    temp = values[i]
                    row[column] = temp
                writer.writerow(row)
