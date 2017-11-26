from enum import Enum


class PARAM(Enum):
    LAMBDA = "lambda"
    MU = "mu"
    THETA = "theta"
    C = "c"
    c0 = "c0"
    L = "l"
    H = "h"
    Q = "q"
    TIME = "simulation_time"
    REPEATS = "repeats"
    DEBUG = "debug"

    def get_param(self, name):
       if name == "lambda": return self.LAMBDA
       if name == "mu": return self.MU
       if name == "theta": return self.THETA
       if name == "c": return self.C
       if name == "c0": return self.c0
       if name == "l": return self.L
       if name == "h": return self.H
       if name == "q": return self.Q
       if name == "simulation_time": return self.TIME
       if name == "repeats": return self.REPEATS
       if name == "debug": return self.DEBUG
       return None