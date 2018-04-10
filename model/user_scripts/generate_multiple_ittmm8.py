import sys

sys.path.append('../')

from stats.statisticsmanager import StatisticsManager
from utils.csvmanager import CSVManager
from utils.parametersparser import ParametersParser

def main():
    names2 = [
        "ittmm1_4",
        "ittmm2_4",
        "ittmm3_4"
    ];
    generate(names2, "m/m/c[c0]/r", "requests");

def generate(names, mode, strategy):
    parser = ParametersParser()

    for name in names:
        [parameters, config] = parser.parse_parameters(name + ".config")

        stat_manager = StatisticsManager(parameters, mode, strategy)
        generated_stat = stat_manager.generate_statistics()

        csv_dto = stat_manager.transform_to_csv_dto(generated_stat, config)

        csv_manager = CSVManager()
        csv_manager.write_csv(csv_dto)

        print("Finish! Gathered ", len(generated_stat), " results to storage, all result saved in ", csv_dto.filename,
              ".csv")

        csv_dto.filename = csv_dto.filename
        csv_manager.write_csv(csv_dto)


if __name__ == '__main__':
	main()

