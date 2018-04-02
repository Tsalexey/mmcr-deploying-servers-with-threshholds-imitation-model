from utils.configparser import ConfigParser, SectionName
from utils.const.param import PARAM
from utils.entities.parameter import Parameter
from utils.parametersvalidator import ParametersValidator


class ParametersParser:

    '''
        Parse Parameters section from .config file
    '''
    def parse_parameters(self):
        parser = ConfigParser()
        validator = ParametersValidator()

        config_dto = parser.parse_config()
        params_dict = self.get_parameters(config_dto.data)

        if validator.validate(params_dict):
            return [self.parse(params_dict), config_dto]

    def parse_parameters(self, name):
        parser = ConfigParser()
        validator = ParametersValidator()

        config_dto = parser.parse_config(name)
        params_dict = self.get_parameters(config_dto.data)

        if validator.validate(params_dict):
            return [self.parse(params_dict), config_dto]

    def parse(self, dict):
        params = {}
        for param, value in dict.items():
            p = PARAM.get_param(PARAM, param)
            v = None
            step = None
            has_range = False
            if len(value.split('-')) == 2:
                has_range = True
                values = value.split('|')
                step = values[1]
                values = values[0].split('-')
                start_value = values[0]
                end_value = values[1]
                v = [start_value, end_value]
            elif param != "debug":
                v = [float(value), float(value)]
                step = 1
            params[p] = Parameter(p, has_range, v, step)
        return params

    '''
        Get parameters from section
    '''
    def get_parameters(self, sections):
        param_dict = {}
        for section, options in sections.items():
            if section == SectionName.PARAMETERS.value:
                for option, value in options.items():
                    param_dict[option] = value
        return param_dict

