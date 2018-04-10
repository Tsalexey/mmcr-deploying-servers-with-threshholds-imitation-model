import sys

sys.path.append('../')

from stats.statisticsmanager import StatisticsManager
from utils.csvmanager import CSVManager
from utils.parametersparser import ParametersParser

def main():
    names = [
        "ittmm1_1",
        "ittmm1_2",
        "ittmm1_3",
        "ittmm1_1",
        "ittmm2_2",
        "ittmm2_3",
        "ittmm3_1",
        "ittmm3_2",
        "ittmm3_3",
        "ittmm4_1",
        "ittmm4_2",
        "ittmm4_3",
        "ittmm5_1",
        "ittmm5_2",
        "ittmm5_3"
    ];

    names2 = [
        "ittmm1_4",
        "ittmm2_4",
        "ittmm3_4",
        "ittmm3_5",
        "ittmm3_6",
        "ittmm4_4",
        "ittmm4_5",
        "ittmm4_6",
        "ittmm5_4",
        "ittmm5_5",
        "ittmm5_6"
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

