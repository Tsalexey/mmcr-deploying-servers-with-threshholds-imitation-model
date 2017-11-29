import sys

sys.path.append('../')
from utils.const.column import COLUMN
from optimization.ValuesFilter import ValuesFilter, CONDITION, OPERATION
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

    print("Finish! Gathered ", len(generated_stat), " results to storage, all result saved in ", csv_dto.filename, ".csv")

    W_max = 2000
    B_max = 0.05

    filter = ValuesFilter(csv_dto.data)

    filter.simple_filter(COLUMN.W_SYSTEM, CONDITION.LESS_OR_EQUAL, W_max)
    filter.simple_filter(COLUMN.B, CONDITION.LESS_OR_EQUAL, B_max)
    # filter.clever_filter({OPERATION.MINUS: [COLUMN.C, COLUMN.c0]}, CONDITION.MIN, None)
    filter.simple_filter(COLUMN.UP_DOWN_TIME, CONDITION.MAX, None)
    filter.simple_filter(COLUMN.UP_DOWN_COUNT, CONDITION.MIN, None)

    csv_dto.data = filter.filtered_csv
    csv_dto.filename = "[FILTERED]" + csv_dto.filename
    csv_manager.write_csv(csv_dto)


if __name__ == '__main__':
	main()
