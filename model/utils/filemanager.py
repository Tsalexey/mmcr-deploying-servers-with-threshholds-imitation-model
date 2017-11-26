import os
from enum import Enum
import sys
from pathlib import Path

sys.path.append('../')

class FileType(Enum):
    CSV = "csv"
    CONFIG = "config"

class DirPath(Enum):
    STATISTICS = "..\\model\\stats\\generated"
    CONFIGS = "..\\model\\config"

class FileManager:

    def select_file(self, rel_path, file_type):
        [file_count, file_dict] = self.get_file_names(rel_path, file_type)

        if file_count == 0:
            print("No found *.%s files in %s" % (file_type.value, os.path.relpath(rel_path.value, os.path.abspath(__file__))))
        else:
            if file_count == 1:
                return file_dict[1]
            else :
                print("Founded %s files" % (file_count))
                print("Select a file:")
                for key, value in file_dict.items():
                    print("#[", key, "] ", value)
                nb = input('Input file number to continue: ')

                try:
                    number = int(nb)
                except ValueError:
                    print("Invalid number")
                return file_dict[number]
            return None
        return None

    def get_path_to_file(self, rel_path):
        abs_path = os.path.abspath(__file__)
        path = os.path.relpath(rel_path.value, abs_path)
        return os.path.abspath(path)

    def get_file_names(self, rel_path, file_type):
        path_to_file = self.get_path_to_file(rel_path)
        file_dict = {}
        file_count = 0
        for root, dirs, files in os.walk(path_to_file):
            for file in files:
                if file.endswith(file_type.value):
                    file_count += 1
                    file_dict[file_count] = file
        return [file_count, file_dict]

    def is_file_exists(self, path, filename):
        my_file = Path(path + "\\" + filename)
        return my_file.is_file()

    def generate_filename(self, path, filename):
        p = path + "\\" + filename

        i = 1
        while self.is_file_exists(Path(path + "\\" + filename + i)):
            i += 1
        return p + i