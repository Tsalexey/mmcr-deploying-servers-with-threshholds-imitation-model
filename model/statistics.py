__author__ = 'tsarev alexey'

import time
import numpy as np

from enum import Enum
from simulation import Simulation
from server import Server
from queue import Queue
from request import Request
from flow import Flow
from generated_values_storage import Generated_values_storage

#--------------------------------------------------------------------------------------------------------------------#
#													  Statistics 												  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Statistics:
	'''
		This class is designed to run Simulation with specified parameters
	'''
	def __init__(self, x_axis, x_range, input_map):
		self.has_range = len(input_map[x_axis].split("-")) == 2
		self.x_axis = x_axis
		self.input_range = x_range
		# TODO replace strings by const
		self.step = input_map["step"]
		self.lambd = input_map["lambda"] if x_axis != "lambda" else -1
		self.mu = input_map["mu"] if x_axis != "mu" else -1
		self.theta =  input_map["theta"] if x_axis != "theta" else -1
		self.C = input_map["C"]
		self.c0 = input_map["c0"] if x_axis != "c0" else -1
		self.L = input_map["L"] if x_axis != "L" else -1
		self.H = input_map["H"] if x_axis != "H" else -1
		self.Q = input_map["Q"] if x_axis != "Q" else -1
		self.simulation_time = input_map["simulation_time"]
		self.is_debug = input_map["is_debug"]
		self.repeats = input_map["repeats"]

	def generate(self):
		'''
			Run simulation and collect statistic depending on specified mode
			mode = {
					single - run with fixed params 
					range - run for specified range
					}
			mode depends on input_range, if there is no range then single simulation will be executed

		'''
		generated_values = []

		print("Input parameters has range =", self.has_range, "\n")
		if self.has_range:
			for var in np.arange(self.input_range[0], self.input_range[1]+1, self.step):
				start_time = time.time()
				for i in range(1, int(self.repeats)):
					generated_values_storage = Generated_values_storage()
					sim = Simulation(self.lambd if self.lambd != -1 else var, 
									 self.mu if self.mu != -1 else var, 
									 self.theta if self.theta != -1 else var, 
									 int(self.C) if self.C != -1 else var, 
									 int(self.c0) if self.c0 != -1 else var, 		 
									 int(self.L) if self.L != -1 else var, 
									 int(self.H) if self.H != -1 else var, 
									 int(self.simulation_time), 
									 int(self.Q) if self.Q != -1 else var, 
									 self.is_debug)
					sim.start()
					generated_values_storage.add(sim)
				end_time = time.time()
				print("Generated values added to storage for ", self.x_axis, " = ", var, "/", self.input_range[1], ", execution time = %s sec" % (end_time - start_time))
				generated_values_storage.normalize(self.repeats)
				generated_values.append(generated_values_storage)
		else:
			for i in range(1, self.repeats):
				print("Repeat #", i)
				generated_values_storage = Generated_values_storage()
				sim = Simulation(lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
				generated_values_storage.add(sim)
				generated_values_storage.normalize(self.repeats)
				generated_values.append(generated_values_storage)			
		return generated_values