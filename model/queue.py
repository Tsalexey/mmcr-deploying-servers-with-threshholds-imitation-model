#--------------------------------------------------------------------------------------------------------------------#
#													  QUEUE														  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Queue:
	def __init__(self, max_size):
		self.max_size = max_size
		self.blocked = 0
		self.requests = []

	def push(self, request):
		if len(self.requests) == self.max_size:
			self.blocked += 1
		else:
			self.requests.append(request)

	def pop(self, request, time):
		queued_request_id = 0;
		for req in self.requests:
			if req.ID == request.ID:
				break;
			queued_request_id += 1

		queued_request = self.requests.pop(queued_request_id)
		queued_request.server_arrival_time = time
		return queued_request