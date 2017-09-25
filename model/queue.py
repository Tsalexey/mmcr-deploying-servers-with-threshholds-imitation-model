__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													  QUEUE														  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Queue:
	def __init__(self, max_size, is_debug):
		self.max_size = max_size
		self.blocked = 0
		self.requests = []
		self.is_debug = is_debug

	def push(self, request):
		if len(self.requests) == self.max_size:
			if self.is_debug: print("		push: request blocked")
			self.blocked += 1
		else:
			if self.is_debug: print("		push: request entered to queue")
			self.requests.append(request)

	def pop(self, request, time):
		if self.is_debug: print("		push: request leaved queue")
		queued_request_id = 0;
		for req in self.requests:
			if req.ID == request.ID:
				break;
			queued_request_id += 1

		queued_request = self.requests.pop(queued_request_id)
		queued_request.server_arrival_time = time
		return queued_request