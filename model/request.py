__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													  Request														 #
#--------------------------------------------------------------------------------------------------------------------#
class Request:
	'''
		This class represents Request entity
	'''
	def __init__(self, ID, arrival_time, alpha, beta):
		'''
			ID = request ID
			arrival_time = time of request generation
			server_arrival_time = starting time of request serving
			alpha = request generating time
			beta = request serving time
		'''
		self.ID = ID
		self.arrival_time = arrival_time
		self.queue_arrival_time = arrival_time
		self.server_arrival_time = arrival_time
		self.alpha = alpha
		self.beta = beta
		self.queue_size_at_serving = 0