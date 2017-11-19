import sys

sys.path.append('../')
from core.states import States

__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													   GENERATED_VALUES_STORAGE										 #
#--------------------------------------------------------------------------------------------------------------------#
class Generated_values_storage:
	"""
		This class is designed to store data generated by simulation
	"""
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
		self.W_system = 0
		self.N = 0
		self.W_queue = 0
		self.Q = 0
		self.state_time = dict.fromkeys(States.get_States_list(States), 0)
		self.state_count = dict.fromkeys(States.get_States_list(States), 0)
		self.up_down_mean = 0;
		self.up_down_count = 0


	def add(self, simulation):
		"""
			Add data from simulation
		"""
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
		self.B += simulation.queue.blocked / (simulation.queue.blocked + len(simulation.served_requests))

		w = 0
		for request in simulation.served_requests:
			w += request.w
		for request in simulation.queue.blocked_requests:
			w += request.w
		self.W_system += w / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))
		self.N += (w / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))) * self.lambd

		wq = 0
		for request in simulation.served_requests:
			wq += request.wq
		for request in simulation.queue.blocked_requests:
			wq += request.wq
		self.W_queue += wq / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))
		self.Q += (wq / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))) * self.lambd

		for state in States.get_States_list(States):
			self.state_time[state] += simulation.state_time[state]
			self.state_count[state] += simulation.state_count[state]

		self.up_down_mean += simulation.up_down_mean
		self.up_down_count += simulation.up_down_count

	def normalize(self, repeats):
		"""
			Normalize data if there was more then one repeats
		"""
		self.blocked /= repeats
		self.served /= repeats
		self.generated /= repeats
		self.B /= repeats
		self.N /= repeats
		self.W_system /= repeats
		self.W_queue /= repeats
		self.Q /= repeats
		for state in States.get_States_list(States):
			self.state_time[state] /= repeats
			self.state_count[state] /= repeats
		self.up_down_mean /= repeats
		self.up_down_count /= repeats
