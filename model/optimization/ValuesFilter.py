from enum import Enum


class CONDITION(Enum):
    NOT_EQUAL = -1
    EQUAL = 0
    LESS = 1
    GREATER = 2
    LESS_OR_EQUAL = 3
    GREATER_OR_EQUAL = 4
    MIN = 5
    MAX = 6

class OPERATION(Enum):
    MINUS = "-"
    PLUS = "+"
    MUL = "*"
    SUB = "/"

class ValuesFilter:

    def __init__(self, csv):
        self.csv = csv
        self.filtered_csv = {}

    '''
        Filter like: "B <= 0.05"
        NOTE: 'SUB' operation is not tested
    '''
    def simple_filter(self, column, condition, limit):
        self.copy_keys()

        if condition == CONDITION.MAX or condition == CONDITION.MIN:
            indexes = self.find_row(self.csv[column.value], condition)
            for i in indexes:
                self.copy_row(i)
        else:
            index = 0
            for value in self.csv[column.value]:
                if self.compare(value, limit, condition):
                    self.copy_row(index)
                index += 1
        self.csv = self.filtered_csv

    '''
        Filter like: C-c0 <= 5
        cond_dict = {OPERATION : [COLUMN, ..., COLUMN]}
        NOTE: only 1 operation supported in cond_dict
        NOTE: 'SUB' operation is not tested
    '''
    def clever_filter(self, cond_dict, condition, limit):
        self.copy_keys()

        if condition == CONDITION.MAX or condition == CONDITION.MIN:
            indexes = self.find_row(self.get_values(cond_dict), condition)
            for i in indexes:
                self.copy_row(i)
        else:
            index = 0
            for value in self.get_values(cond_dict):
                if self.compare(value, limit, condition):
                    self.copy_row(index)
                index += 1
        self.csv = self.filtered_csv

    '''
        For condition MIN/MAX find appropriate rows
    '''
    def find_row(self, values, condition):
        rows = []
        i = 0
        j = 0
        temp_value = values[j]
        for value in values:
            if temp_value == value:
                rows.append(i)
            if condition == CONDITION.MIN:
                if value < temp_value:
                    rows = []
                    rows.append(i)
                    temp_value = value
            elif condition == CONDITION.MAX:
                if value > temp_value:
                    rows = []
                    rows.append(i)
                    temp_value = value
            else:
                return None
            i += 1
        return rows

    '''
        Calculate values for COLUMNS on the base of operation for clever_filter
    '''
    def get_values(self, cond_dict):
        temp_list = []

        operation = None
        cols = []

        for key, values in cond_dict.items():
            operation = key
            cols = values
            break

        first_col = cols.pop(0)

        for value in self.csv[first_col.value]:
            temp_list.append(value)

        for col in cols:
            i = 0
            for value in self.csv[col.value]:
                temp_list[i] = self.handle_operation(temp_list[i], value, operation)
                i += 1

        return temp_list

    '''
        Do OPERATION for values
    '''
    def handle_operation(self, left_value, right_value, operation):
        if operation == OPERATION.MINUS:
            return float(left_value) - float(right_value)
        if operation == OPERATION.PLUS:
            return float(left_value) + float(right_value)
        if operation == OPERATION.MUL:
            return float(left_value) * float(right_value)
        if operation == OPERATION.SUB:
            return float(left_value) / float(right_value)
        return None

    '''
        Compare values with limit
    '''
    def compare(self, value, limit, condition):
        if condition == CONDITION.NOT_EQUAL:
            return float(value) != limit
        if condition == CONDITION.EQUAL:
            return float(value) == limit
        if condition == CONDITION.LESS:
            return float(value) < limit
        if condition == CONDITION.GREATER:
            return float(value) > limit
        if condition == CONDITION.LESS_OR_EQUAL:
            return float(value) <= limit
        if condition == CONDITION.GREATER_OR_EQUAL:
            return float(value) >= limit
        return None

    '''
        Copy row from csv to filtered csv
    '''
    def copy_row(self, index):
        for key, values in self.csv.items():
            temp_value = self.filtered_csv[key]
            if len(values) < index or len(values) == 0:
                temp_value.append(0)
            else:
                temp_value.append(values[index])
            self.filtered_csv[key] = temp_value

    '''
        Generate empty filtered csv with right names
    '''
    def copy_keys(self):
        self.filtered_csv = {}

        for key, values in self.csv.items():
            self.filtered_csv[key] = []
        return self.filtered_csv
