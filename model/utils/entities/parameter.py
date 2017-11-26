
class Parameter:

    def __init__(self, param, has_range, values, step):
        self.param = param
        self.has_range = has_range
        self.start_value = float(values[0])
        self.end_value = float(values[1])
        self.values = values
        self.step = float(step)
