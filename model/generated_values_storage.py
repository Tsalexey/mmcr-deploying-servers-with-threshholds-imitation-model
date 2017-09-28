__author__ = 'tsarev alexey'

import random
import math
from request import Request
#--------------------------------------------------------------------------------------------------------------------#
#													   GENERATED_VALUES_STORAGE										 #
#--------------------------------------------------------------------------------------------------------------------#
class Generated_values_storage:
	'''
		This class is designed to store data generated by simulation
	'''
	def __init__(self):
		self.lambd = 0
		self.mu = 0
		self.theta = 0
		self.servers_count = 0
		self.core_servers_count = 0
		self.L = 0
		self.H = 0
		self.simulation_time = 0
		self.is_debug = False
		self.blocked = 0
		self.served = 0
		self.generated = 0
		self.B = 0
		self.N = 0

	def add(self, simulation):
		'''
			Add data from simulation
		'''
		self.lambd = simulation.lambd
		self.mu = simulation.mu
		self.theta = simulation.theta
		self.servers_count = simulation.servers_count
		self.core_servers_count = simulation.core_servers_count
		self.L = simulation.L
		self.H = simulation.H
		self.simulation_time = simulation.simulation_time
		self.is_debug = simulation.is_debug

		self.blocked += simulation.queue.blocked
		self.served += len(simulation.served_requests)
		self.generated += simulation.flow.generated_count	
		self.B += simulation.queue.blocked/len(simulation.served_requests)
		self.N += len(simulation.served_requests)/simulation.simulation_time

	def normalize(self, repeats):
		'''
			Normalize data if there was more then one repeats
		'''
		self.blocked /= repeats
		self.served /= repeats
		self.generated /= repeats	
		self.B /= repeats
		self.N /= repeats		
