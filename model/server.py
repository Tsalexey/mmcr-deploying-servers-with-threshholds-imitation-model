__author__ = 'tsarev alexey'

import random
#--------------------------------------------------------------------------------------------------------------------#
#													  SERVER														 #
#--------------------------------------------------------------------------------------------------------------------#
class Server:
	'''
		This class represents server
	'''
	def __init__(self, ID, is_deployed, is_debug):
		'''
			arrival_time = request arrival time to server
			departure_time = request departure time form server
		'''
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
		if self.is_debug: 
			print("created Server: id = ", self.ID, 
				  ", busy = ", self.is_busy, 
				  ", deployed = ", self.is_deployed,
				  ", to be turned on = ", self.to_be_turned_on,
				  ", to be turned off = ", self.to_be_turned_off)

	def load(self, request):
		'''
			Start request serving
		'''
		if self.is_debug: print("		load server #", self.ID)
		self.served_request = request
		self.arrival_time = request.server_arrival_time
		self.departure_time = self.arrival_time + request.beta;
		self.is_busy = True;
		self.is_deployed = True
		self.to_be_turned_on = False
		self.to_be_turned_off = False

	def unload(self):
		'''
			Finishe request serving
		'''
		if self.is_debug: print("		unload server #", self.ID)
		self.is_busy = False
		self.is_deployed = True
		if self.to_be_turned_off:
			self.is_deployed = False
		self.to_be_turned_on = False
		self.to_be_turned_off = False
		return self.served_request

	def turn_on(self, actual_time, theta):
		'''
			Start server turning
		'''
		if not self.is_deployed and not self.to_be_turned_on:
			if self.is_debug: print("		start deploying server #", self.ID)
			self.turn_on_time = actual_time + random.expovariate(theta)
			self.to_be_turned_off = False
			self.to_be_turned_on = True
			self.is_busy = False;
			self.is_deployed = False

	def turn_off(self):
		'''
			Change server state
		'''
		self.to_be_turned_on = False
		self.to_be_turned_off = True
		if self.is_debug: print("		turn off server #", self.ID)

	def deploy(self):
		'''
			Turn on server
		'''
		if not self.is_deployed and self.to_be_turned_on:
			self.is_deployed = True
			self.to_be_turned_on = False
			self.to_be_turned_off = False
			self.is_busy = False
			if self.is_debug: print("		deployed server #", self.ID)

	def unload_and_undeploy(self):
		'''
			Turn off server (turn off runs immideatly)
		'''
		if self.is_busy and self.is_deployed and self.to_be_turned_off:
			if self.is_debug: print("		unload & undeploy server #", self.ID)
			self.is_busy = False
			self.is_deployed = False
			self.to_be_turned_on = False
			self.to_be_turned_off = False
			return self.served_request			

	def get_info(self):
		'''
			Print debug information
		'''
		if self.is_debug:
			print("		-srv info:id=",  self.ID, ",busy=", self.is_busy, ",deployed=", self.is_deployed, 
				  ",turn on=", self.to_be_turned_on, ",turn off=", self.to_be_turned_off,
				  ",departure=%.3f"%self.departure_time)
