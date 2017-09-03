import random
#--------------------------------------------------------------------------------------------------------------------#
#													  SERVER														 #
#--------------------------------------------------------------------------------------------------------------------#
class Server:
	def __init__(self, ID, is_deployed):
		self.ID = ID
		self.arrival_time = 0
		self.departure_time = 0
		self.is_deployed = is_deployed
		self.is_busy = False
		self.turn_on_time = 0
		self.served_request = 0

	def load(self, request):
		self.served_request = request
		self.arrival_time = request.server_arrival_time
		self.departure_time = self.arrival_time + request.beta;
		self.is_busy = True;

	def unload(self):
		self.is_busy = False
		return self.served_request

	def turn_on(self, actual_time, theta):
		self.turn_on_time = actual_time + random.expovariate(theta)

	def turn_off(self):
		self.is_deployed = False