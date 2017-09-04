import random
#--------------------------------------------------------------------------------------------------------------------#
#													  SERVER														 #
#--------------------------------------------------------------------------------------------------------------------#
class Server:
	def __init__(self, ID, is_deployed, is_debug):
		self.ID = ID
		self.arrival_time = 0
		self.departure_time = 0
		self.is_deployed = is_deployed
		self.is_debug = is_debug
		self.is_busy = False
		self.to_be_turned_off =False
		self.to_be_turned_on = False
		self.turn_on_time = 0
		self.served_request = 0

	def load(self, request):
		if self.is_debug: print("		load server #", self.ID)
		self.served_request = request
		self.arrival_time = request.server_arrival_time
		self.departure_time = self.arrival_time + request.beta;
		self.is_busy = True;

	def unload(self):
		if self.is_debug: print("		unload server #", self.ID)
		self.is_busy = False
		return self.served_request

	def turn_on(self, actual_time, theta):
		if self.is_debug: print("		start deploying server #", self.ID)
		self.turn_on_time = actual_time + random.expovariate(theta)
		self.to_be_turned_off = False
		self.to_be_turned_on = True

	def turn_off(self):
		if self.is_debug: print("		turn off server #", self.ID)
		self.is_deployed = False
		self.to_be_turned_off = True
		self.to_be_turned_on = False