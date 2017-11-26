import argparse

from utils.const.param import PARAM


class ParametersValidator:

    def validate(self, params_dict):
        for key, value in params_dict.items():
            self.check_value(key, value)
        return True

    def check_value(self, key, value):
        if key == "debug":
            self.check_bool(key, value)
        else:
            if len(value.split('-')) == 2:
                self.check_range(key, value)
            else:
                self.check_float(key, value)

    def check_range(self, key, value):
        if len(value.split('|')) != 2: argparse.ArgumentTypeError("Wrong value for parameter ", key, "=", value,
                                                                  ". Step not specified")
        values = value.split('|')
        if key == PARAM.C.value or key == PARAM.c0.value or key == PARAM.L.value or key == PARAM.H.value or key == PARAM.Q.value:
            self.check_int(key, value[1])
            for v in values[0].split('-'):
                self.check_int(key, v)
        else:
            self.check_float(key, value[1])
            self.check_float(key, values[1])

    def check_int(self, key, value):
        if not value.isdigit():
            argparse.ArgumentTypeError("Wrong value for parameter ", key, "=", value)

    def check_float(self, key, value):
        try:
            float(value)
        except ValueError:
            argparse.ArgumentTypeError("Wrong value for parameter ", key, "=", value)

    def check_bool(self, key, value):
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif value.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError("Wrong value for parameter ", key, "=", value)