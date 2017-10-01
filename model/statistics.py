__author__ = 'tsarev alexey'

import time
import numpy as np

from simulation import Simulation
from generated_values_storage import Generated_values_storage
from const import Const
#--------------------------------------------------------------------------------------------------------------------#
#													  Statistics 												  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Statistics:
	"""
		This class is designed to run Simulation with specified parameters
	"""
	def __init__(self, x_axis, x_range, input_map):
		const = Const()
		self.has_range = len(input_map[x_axis].split("-")) == 2
		self.x_axis = x_axis
		self.input_range = x_range
		self.step = input_map[const.STEP]
		self.lambd = input_map[const.LAMBDA] if x_axis != const.LAMBDA else -1
		self.mu = input_map[const.MU] if x_axis != const.MU else -1
		self.theta =  input_map[const.THETA] if x_axis != const.THETA else -1
		self.C = input_map[const.C]
		self.c0 = input_map[const.C0] if x_axis != const.C0 else -1
		self.L = input_map[const.L] if x_axis != const.L else -1
		self.H = input_map[const.H] if x_axis != const.L else -1
		self.Q = input_map[const.Q] if x_axis != const.Q else -1
		self.simulation_time = input_map[const.SIMULATION_TIME]
		self.is_debug = input_map[const.DEBUG]
		self.repeats = input_map[const.REPEATS]

	def generate(self):
		"""
			Run simulation and collect statistic depending with specified strategy
			strategy = {
					single - run with fixed params
					range - run for specified range
					}
			strategy depends on input_range, if there is no range then single simulation will be executed

		"""
		generated_values = []

		print("Input parameters has range =", self.has_range, "\n")
		if self.has_range:
			for var in np.arange(self.input_range[0], self.input_range[1]+1, self.step):
				start_time = time.time()
				generated_values_storage = Generated_values_storage()
				for i in range(0, int(self.repeats)):
					sim = Simulation("m/m/c/r", self.lambd if self.lambd != -1 else var,
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
				print("Generated values added to storage for ", self.x_axis, " = ", var, "/", self.input_range[1],
					  ", repeated ", len(range(0, int(self.repeats))), " times, ",
					  "execution time = %s sec" % (end_time - start_time))
				generated_values_storage.normalize(self.repeats)
				generated_values.append(generated_values_storage)
		else:
			for i in range(1, self.repeats):
				print("Repeat #", i)
				generated_values_storage = Generated_values_storage()
				sim = Simulation("m/m/c/r", self.lambd,
								 self.mu ,
								 self.theta,
								 int(self.C),
								 int(self.c0),
								 int(self.L),
								 int(self.H),
								 int(self.simulation_time),
								 int(self.Q),
								 self.is_debug)
				generated_values_storage.add(sim)
			generated_values_storage.normalize(self.repeats)
			generated_values.append(generated_values_storage)			
		return generated_values
