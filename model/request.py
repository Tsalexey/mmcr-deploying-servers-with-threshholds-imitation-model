#--------------------------------------------------------------------------------------------------------------------#
#													  Request														 #
#--------------------------------------------------------------------------------------------------------------------#
class Request:
	def __init__(self, ID, arrival_time, alpha, beta):
		self.ID = ID
		self.arrival_time = arrival_time
		self.queue_arrival_time = arrival_time
		self.server_arrival_time = arrival_time
		self.alpha = alpha
		self.beta = beta
		self.queue_size_at_serving = 0