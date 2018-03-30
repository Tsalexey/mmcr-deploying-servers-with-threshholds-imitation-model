import sys
import time
import numpy as np

from core.simulation import Simulation
from core.states import States
from utils.const.param import PARAM
from utils.entities.dto import DTO
from utils.filemanager import FileManager, DirPath

sys.path.append('../')
from stats.generated_values_storage import Generated_values_storage


class StatisticsManager:

    def __init__(self, parameters):
        self.parameters = parameters
        self.simulation_time = self.parameters[PARAM.TIME].start_value
        self.range_dict = self.create_range_dict()
        self.is_debug = False
        self.mode = "m/m/c[c0]/r[l,h]" #"m/m/c[c0]/r" #"m/m/c[c0]/r[l,h]"
        self.strategy = "request"

    def generate_statistics(self):
        generated_values = []

        t1 = time.time()
        for lambd in self.range_dict[PARAM.LAMBDA]:
            for mu in self.range_dict[PARAM.MU]:
                for theta in self.range_dict[PARAM.THETA]:
                    for C in self.range_dict[PARAM.C]:
                        for c0 in self.range_dict[PARAM.c0]:
                            for L in self.range_dict[PARAM.L]:
                                for H in self.range_dict[PARAM.H]:
                                    for Q in self.range_dict[PARAM.Q]:
                                        if lambd <= 0: continue
                                        if mu <= 0: continue
                                        if theta <= 0: continue
                                        if C <= 0: continue
                                        if c0 <= 0: continue
                                        if L <= 0: continue
                                        if H <= 0: continue
                                        if Q <= 0: continue
                                        if c0 > C or c0 < 0: continue
                                        if H - L < 2: continue
                                        if Q - H <= 2: continue
                                        if H < L or H > Q: continue
                                        if L > Q: continue

                                        start_time = time.time()
                                        generated_values_storage = Generated_values_storage()
                                        for repeats in self.range_dict[PARAM.REPEATS]:
                                            sim = Simulation(self.mode, lambd, mu, theta, C, c0, L, H, self.simulation_time, Q, self.is_debug)
                                            if (self.strategy == "time"):
                                                sim.start()
                                            else:
                                                sim.start_requests(self.simulation_time)
                                            generated_values_storage.add(sim)
                                        end_time = time.time()
                                        generated_values_storage.normalize(self.parameters[PARAM.REPEATS].end_value)
                                        generated_values.append(generated_values_storage)
                                        self.log(lambd, mu, theta, C, c0, L, H, Q, start_time, end_time)
        t2 = time.time()
        print("Total simulation time = %.5f"%(t2-t1))
        return generated_values

    def create_range_dict(self):
        range_dict = {PARAM.LAMBDA: self.get_nprange(PARAM.LAMBDA),
                      PARAM.MU: self.get_nprange(PARAM.MU),
                      PARAM.THETA: self.get_nprange(PARAM.THETA),
                      PARAM.C: self.get_nprange(PARAM.C),
                      PARAM.c0: self.get_nprange(PARAM.c0),
                      PARAM.L: self.get_nprange(PARAM.L),
                      PARAM.H: self.get_nprange(PARAM.H),
                      PARAM.Q: self.get_nprange(PARAM.Q),
                      PARAM.REPEATS: self.get_nprange(PARAM.REPEATS)}
        return range_dict

    def get_nprange(self, param):
        if param == PARAM.REPEATS:
            return np.arange(1, self.parameters[PARAM.REPEATS].end_value + self.parameters[PARAM.REPEATS].step,
                                self.parameters[PARAM.REPEATS].step)
        else:
            return np.arange(self.parameters[param].start_value,
                             self.parameters[param].end_value + self.parameters[param].step,
                             self.parameters[param].step)

    def log(self, lambd, mu, theta, C, c0, L, H, Q, start_time, end_time):
        print("Generated: \n",
              self.get_string(lambd, PARAM.LAMBDA),
              self.get_string(mu, PARAM.MU),
              self.get_string(theta, PARAM.THETA),
              self.get_string(C, PARAM.C),
              self.get_string(c0, PARAM.c0),
              self.get_string(L, PARAM.L),
              self.get_string(H, PARAM.H),
              self.get_string(Q, PARAM.Q),
              "rep ", len(self.range_dict[PARAM.REPEATS]), " times, time = %s sec" % (end_time - start_time))

    def get_string(self, value, param):
        if self.parameters[param].start_value == self.parameters[param].end_value:
            return "%.2s=%.2f," % (param.value, value)
        else:
            return "%.2s=%.2f/%.2f," % (param.value, value, self.parameters[param].end_value)

    def transform_to_csv_dto(self, generated_stat, config):
        manager = FileManager()

        path_to_file = manager.get_path_to_file(DirPath.STATISTICS)

        filename = "Statistics for " + config.filename + " #"
        i = 1
        while manager.is_file_exists(path_to_file, filename + str(i)):
            i += 1

        filename += str(i)

        data = self.transform_generated_values(config.column_names, generated_stat)

        return DTO(filename, path_to_file, config.column_names, data)

    def transform_generated_values(self, column_names, generated_stat):
        data = {}

        sim = []
        lambd = []
        mu = []
        theta = []
        C = []
        c0 = []
        L = []
        H = []
        blocked = []
        served = []
        generated = []
        B = []
        N = []
        W_system = []
        Q = []
        W_queue = []
        idle_time = []
        off_time = []
        up_time = []
        full_time = []
        idle_count = []
        off_count = []
        up_count = []
        full_count = []
        up_down_mean = []
        up_down_count = []

        i=0
        for stat in generated_stat:
            i = i + 1
            sim.append(i)
            lambd.append("{:.5}".format(stat.lambd))
            mu.append("{:.5}".format(stat.mu))
            theta.append("{:.5}".format(stat.theta))
            C.append(stat.servers_count)
            c0.append(stat.core_servers_count)
            L.append(stat.L)
            H.append(stat.H)
            blocked.append("{:.5}".format(stat.blocked))
            served.append("{:.5}".format(stat.served))
            generated.append("{:.5}".format(stat.generated))
            B.append("{:.5}".format(stat.B))
            N.append("{:.5}".format(stat.N))
            W_system.append("{:.5}".format(stat.W_system))
            Q.append("{:.5}".format(stat.Q))
            W_queue.append("{:.5}".format(stat.W_queue))
            idle_time.append("{:.5}".format(stat.state_time[States.IDLE]))
            off_time.append("{:.5}".format(stat.state_time[States.TURN_OFF]))
            up_time.append("{:.5}".format(stat.state_time[States.TURN_UP]))
            full_time.append("{:.5}".format(stat.state_time[States.FULL]))
            idle_count.append("{:.5}".format(stat.state_count[States.IDLE]))
            off_count.append("{:.5}".format(stat.state_count[States.TURN_OFF]))
            up_count.append("{:.5}".format(stat.state_count[States.TURN_UP]))
            full_count.append("{:.5}".format(stat.state_count[States.FULL]))
            up_down_mean.append("{:.5}".format(stat.up_down_mean))
            up_down_count.append("{:.5}".format(stat.up_down_count))

        data[column_names[0]] = sim
        data[column_names[1]] = lambd
        data[column_names[2]] = mu
        data[column_names[3]] = theta
        data[column_names[4]] = C
        data[column_names[5]] = c0
        data[column_names[6]] = L
        data[column_names[7]] = H
        data[column_names[8]] = blocked
        data[column_names[9]] = served
        data[column_names[10]] = generated
        data[column_names[11]] = B
        data[column_names[12]] = N
        data[column_names[13]] = W_system
        data[column_names[14]] = Q
        data[column_names[15]] = W_queue
        data[column_names[16]] = idle_time
        data[column_names[17]] = off_time
        data[column_names[18]] = up_time
        data[column_names[19]] = full_time
        data[column_names[20]] = idle_count
        data[column_names[21]] = off_count
        data[column_names[22]] = up_count
        data[column_names[23]] = full_count
        data[column_names[24]] = up_down_mean
        data[column_names[25]] = up_down_count

        return data
