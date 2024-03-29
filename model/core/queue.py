__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													  QUEUE														  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Queue:
	"""
		This class represents Queue
	"""
	def __init__(self, max_size, is_debug):
		self.max_size = max_size
		self.blocked = 0
		self.requests = []
		self.blocked_requests_sum_w = 0;
		self.blocked_requests_sum_wq = 0;
		self.is_debug = is_debug

	def push(self, request):
		"""
			Push request into queue
		"""
		if len(self.requests) == self.max_size:
			if self.is_debug: print("		push: request blocked")
			self.blocked += 1
			request.w = 0; #request.queue_arrival_time - request.arrival_time
			request.wq = 0; #request.server_arrival_time - request.queue_arrival_time
			self.blocked_requests_sum_w += request.w;
			self.blocked_requests_sum_wq += request.wq;
		else:
			if self.is_debug: print("		push: request entered to queue")
			self.requests.append(request)

	def pop(self, request, time):
		"""
			Pop request form queue
		"""
		if self.is_debug: print("		push: request leaved queue")
		queued_request_id = 0;
		for req in self.requests:
			if req.ID == request.ID:
				break;
			queued_request_id += 1

		queued_request = self.requests.pop(queued_request_id)
		queued_request.server_arrival_time = time
		return queued_request