import sys

sys.path.append('../')
from stats.statisticsmanager import StatisticsManager
from utils.csvmanager import CSVManager
from utils.parametersparser import ParametersParser


def main():
    parser = ParametersParser()
    [parameters, config] = parser.parse_parameters()

    stat_manager = StatisticsManager(parameters)
    generated_stat = stat_manager.generate_statistics()

    csv_dto = stat_manager.transform_to_csv_dto(generated_stat, config)

    csv_manager = CSVManager()
    csv_manager.write_csv(csv_dto)

    print("Finish! Gathered ", len(generated_stat), " results to storage, all result saved in ", csv_dto.filename, " csv")

if __name__ == '__main__':
	main()
