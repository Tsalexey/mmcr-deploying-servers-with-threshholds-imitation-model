import sys

sys.path.append('../')

from stats.statisticsmanager import StatisticsManager
from utils.csvmanager import CSVManager
from utils.parametersparser import ParametersParser

def main():
    names = [
        "#1_1",
        "#1_2",
        "#1_3",
        "#2_1",
        "#2_2",
        "#2_3",
        "#3_1",
        "#3_2",
        "#3_3",
        "#4_1",
        "#4_2",
        "#4_3",
        "#5_1",
        "#5_2",
        "#5_3"
    ];

    names2 = [
        "#1_(4)",
        "#2_(4)",
        "#3_(4)",
        "#3_(5)",
        "#3_(6)",
        "#4_(4)",
        "#4_(5)",
        "#4_(6)",
        "#5_(4)",
        "#5_(5)",
        "#5_(6)"
    ];

    generate(names, "m/m/c[c0]/r[l,h]", "requests");
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

