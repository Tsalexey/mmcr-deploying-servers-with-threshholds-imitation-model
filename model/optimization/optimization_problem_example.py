import sys
from enum import Enum

from utils.const.column import COLUMN

sys.path.append('../')
from utils.csvmanager import CSVManager
from optimization.ValuesFilter import ValuesFilter, CONDITION, OPERATION


def main():
    W_max = 2000
    B_max = 0.05
    t_max = 2
    threshhold_diff = 2

    csv_manager = CSVManager()
    csv_dto = csv_manager.parse_csv()

    filter = ValuesFilter(csv_dto.data)

    filter.simple_filter(COLUMN.W_SYSTEM, CONDITION.LESS_OR_EQUAL, W_max)
    filter.simple_filter(COLUMN.B, CONDITION.LESS_OR_EQUAL, B_max)
    filter.simple_filter(COLUMN.UP_DOWN_TIME, CONDITION.GREATER_OR_EQUAL, t_max)

    filter.clever_filter({OPERATION.MINUS: [COLUMN.H, COLUMN.L]}, CONDITION.GREATER_OR_EQUAL, threshhold_diff)
    filter.clever_filter({OPERATION.MINUS: [COLUMN.C, COLUMN.c0]}, CONDITION.MIN, None)

    csv_dto.data = filter.filtered_csv
    csv_dto.filename = "[FILTERED]" + csv_dto.filename
    csv_manager.write_csv(csv_dto)

if __name__ == '__main__':
	main()

