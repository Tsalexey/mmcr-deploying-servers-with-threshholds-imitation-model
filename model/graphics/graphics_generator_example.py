import sys
import os

sys.path.append('../')
from utils.csvmanager import CSVManager
from graphics.graphics_generator import Graphics_generator

def main():

    csv_manager = CSVManager()
    csv_dto = csv_manager.parse_csv()

    path_with_name = os.path.join(csv_dto.path, csv_dto.filename + ".pdf")

    x = csv_dto.data["lambda"]
    y = csv_dto.data

    Graphics_generator.plot(x, r'$\lambda, мс^-1$', y, path_with_name)

if __name__ == '__main__':
	main()