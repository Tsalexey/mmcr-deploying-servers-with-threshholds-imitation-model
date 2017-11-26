__author__ = 'tsarev alexey'

from core.queue import Queue
from core.request import Request
from core.server import Server
from core.states import States
from core.flow import Flow
#--------------------------------------------------------------------------------------------------------------------#
#													  SIMULATION													 #
#--------------------------------------------------------------------------------------------------------------------#

class Simulation:
	"""
		This class represents simulation process
	"""
	def __init__(self, mode, lambd, mu, theta, servers_count, core_servers_count, L, H, simulation_time, max_queue_size, is_debug):
		self.lambd = lambd
		self.mu = mu
		self.theta = theta
		self.servers_count = int(servers_count)
		self.core_servers_count = int(core_servers_count)
		self.L = int(L)
		self.H = int(H)
		self.simulation_time = simulation_time
		self.is_debug = is_debug
		self.auto_continue = not self.is_debug
		self.mode = mode

		self.flow = Flow(lambd, mu, is_debug)
		self.queue = Queue(int(max_queue_size), is_debug)

		self.generated_request = Request(-1, 0, 0, 0)

		self.system_state = States.IDLE
		self.prev_system_state = States.IDLE

		self.servers = []
		self.served_requests = []
		self.generated_requests = []

		self.time = 0
		self.prev_time = 0
		self.up_down_time = 0
		self.prev_up_down_time = 0

		self.up_down_count = 0
		self.up_down_mean = 0

		self.state_time = dict.fromkeys(States.get_States_list(States), 0)
		self.state_count = dict.fromkeys(States.get_States_list(States), 0)

		for i in range(int(servers_count)):
			self.servers.append(Server(i, True if i < int(core_servers_count) else False, is_debug))

	def update_state_time(self):
		self.state_time[self.prev_system_state] += self.time - self.prev_time

	def update_state_count(self):
		self.state_count[self.prev_system_state] += 1

	def update_system_state(self):
		self.prev_system_state = self.system_state
		self.system_state = self.get_system_state()

	def get_system_state(self):
		"""
			Calculate server state
		"""
		if self.mode == "m/m/c/r":
			return States.IDLE
		if self.mode == "m/m/c[c0]/r":
			if self.system_state == States.IDLE:
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() == self.core_servers_count:
					return States.IDLE
				if len(self.queue.requests) > 0:
					return States.TURN_UP
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() > self.core_servers_count:
					return States.TURN_OFF
				return "Error[IDLE]"
			if self.system_state == States.TURN_UP:
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() == self.core_servers_count:
					return States.IDLE
				if len(self.queue.requests) > 0:
					return States.TURN_UP
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() > self.core_servers_count:
					return States.TURN_OFF
				return "Error[TURN_UP]"
			if self.system_state == States.TURN_OFF:
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() > self.core_servers_count:
					return States.TURN_OFF
				if len(self.queue.requests) == 0 and self.get_deployed_servers_count() == self.core_servers_count:
					return States.IDLE
				if len(self.queue.requests) > 0:
					return States.TURN_UP
				return "Error[TURN_OFF]"
			return "Error[m/m/c[c0]/r]"
		if self.mode == "m/m/c[c0]/r[l,h]":
			if self.system_state == States.IDLE:
				if len(self.queue.requests) >= self.H:
					return States.TURN_UP
				if len(self.queue.requests) < self.H:
					return States.IDLE
				return "Error[IDLE]"
			if self.system_state == States.TURN_UP or self.system_state == States.FULL:
				if len(self.queue.requests) <= self.L:
					return States.TURN_OFF
				if len(self.queue.requests) > self.L and self.servers_count == self.get_deployed_servers_count():
					return States.FULL
				if len(self.queue.requests) > self.L:
					return States.TURN_UP
				return "Error[TURN_UP]"
			if self.system_state == States.TURN_OFF:
				if len(self.queue.requests) >= self.H:
					return States.TURN_UP
				if len(self.queue.requests) < self.H and self.get_deployed_servers_count() == self.core_servers_count:
					return States.IDLE
				if len(self.queue.requests) < self.H and self.get_deployed_servers_count() > self.core_servers_count:
					return States.TURN_OFF
				return "Error[TURN_OFF]"
			return "Error[m/m/c[c0]/r[l,h]]"
		return "Error[mode not supported]"
	
	def update_time(self):
		if self.system_state == States.IDLE:
			self.prev_up_down_time = 0
		else:
			if self.prev_system_state == States.IDLE:
				self.prev_up_down_time = self.time
			else:
				if self.system_state != self.prev_system_state:
					if self.system_state == States.TURN_OFF or self.prev_system_state == States.TURN_OFF:
						self.up_down_count += 1
						self.up_down_time += self.time - self.prev_up_down_time
						self.up_down_mean = self.up_down_time / self.up_down_count

		self.prev_time = self.time
		self.time = self.get_system_time()

	def get_system_time(self):
		"""
			Calculate time after last event
		"""
		first_generated_request = self.get_first_arrived_generated_request()
		first_served_server = self.get_first_served_server()
		first_turned_server = self.get_first_turned_server()

		next_arrive_time = first_generated_request.arrival_time
		next_serve_time = float('inf') if first_served_server.ID == -1 else first_served_server.departure_time
		next_turn_time = float('inf') if (first_turned_server.ID == -1 and (self.system_state != States.TURN_UP or self.system_state != States.FULL)) else first_turned_server.turn_on_time

		t = min([next_arrive_time, next_serve_time, next_turn_time])
		if self.is_debug:
			t0 = "%.3f"%first_generated_request.arrival_time
			t1 = "never" if next_serve_time == float('inf') else "%.3f"%next_serve_time
			t2 = "never" if next_turn_time == float('inf') else "%.3f"%next_turn_time
			if t == next_arrive_time: event = "ARRIVE"
			if t == next_serve_time: event = "SERVE"
			if t == next_turn_time: event = "TURN"
			print("	Event=", event, ", arrive= ", t0, ", ",
				  "serve= ", t1, "(#", first_served_server.ID, "),"
				  "turn up= ", t2, "(#", first_turned_server.ID, ")")

		return t

	def get_free_deployed_server(self):
		"""
			Return free working server
		"""
		free_server = False
		for server in self.servers:
			if not server.is_busy and server.is_deployed and not server.to_be_turned_off:
				return server
		return free_server

	def get_free_deployed_servers_count(self):
		"""
			Return count of free working servers
		"""
		count = 0
		for server in self.servers:
			if not server.is_busy and server.is_deployed and not server.to_be_turned_off:
				count += 1
		return count

	def get_busy_deployed_servers_count(self):
		"""
			Return count of busy working servers
		"""
		count = 0
		for server in self.servers:
			if server.is_busy and server.is_deployed:
				count += 1
		return count

	def get_deployed_servers_count(self):
		"""
			Return working servers count
		"""
		count = 0
		for server in self.servers:
			if server.is_deployed:
				count += 1
		return count

	def get_first_arrived_generated_request(self):
		"""
			Return request to be served first
		"""
		generated_request = self.generated_requests[0]
		for request in self.generated_requests:
			if request.arrival_time < generated_request.arrival_time:
				generated_request = request
		return generated_request

	def get_first_served_server(self):
		"""
			Return server to be served first
		"""
		served_server = Server(-1, True, False)
		served_server.departure_time = float('inf')
		for server in self.servers:
			if server.is_busy and server.is_deployed and server.departure_time < served_server.departure_time:
				served_server = server
		return served_server

	def get_first_turned_server(self):
		"""
			Return server to be turned on first
		"""
		served_server = Server(-1, True, False)
		served_server.turn_on_time = float('inf')
		for server in self.servers:		
			if server.to_be_turned_on and server.turn_on_time < served_server.turn_on_time:
				served_server = server
		return served_server

	def get_servers_to_turn_off(self):
		"""
			Return servers list to be turned off
		"""
		result = []
		# sort servers by departure time
		self.servers.sort(key=lambda x: x.departure_time)
		for i in range(0, len(self.servers)):
			self.servers[i].ID = i
		# turn off c(t)-c0 served deployed servers
		turned_off_servers = 0
		for server in self.servers:
			if turned_off_servers < self.get_deployed_servers_count() - self.core_servers_count and server.is_deployed:
				turned_off_servers += 1
				result.append(server)
		return result

	def pop_generated_request(self, request):
		"""
			Delete request from list of generated request waiting to be served
		"""
		request_id = 0;
		for req in self.generated_requests:
			if req.ID == request.ID:
				self.generated_requests.pop(request_id)
				break;
			request_id += 1

	def has_turned_servers(self):
		turned_count = 0
		for server in self.servers:
			if server.is_deployed:
				turned_count += 1
		return True if turned_count != self.core_servers_count else False

	def turn_on_servers(self):
		# start turning up servers
		for server in self.servers:
			self.servers[server.ID].turn_on(self.time, self.theta)
		# time = turn up server, change server state to deployed
		for server in self.servers:
			if server.turn_on_time == self.time:
				self.servers[server.ID].deploy()

	def turn_off_servers(self):
		servers_to_turn_off = self.get_servers_to_turn_off()
		for server in self.servers:
			self.servers[server.ID].turn_off()
		for server in servers_to_turn_off:
			if server.departure_time == self.time and server.is_busy and server.is_deployed and server.to_be_turned_off:
				served_request = self.servers[server.ID].unload_and_undeploy()
				self.served_requests.append(served_request)
		for server in self.servers:
			if server.departure_time == self.time and server.is_busy and server.is_deployed and not server.to_be_turned_off:
				served_request = self.servers[server.ID].unload()
				self.served_requests.append(served_request)				

	def handle_idle(self):
		for server in self.servers:
			self.servers[server.ID].idle()

	def handle_idle_mode(self):
		self.handle_idle()
		self.serve_request()
		self.handle_request()
		self.handle_queue()

	def handle_turn_on_mode(self):
		self.turn_on_servers()
		self.serve_request()
		self.handle_request()
		self.handle_queue()				

	def handle_turn_off_mode(self):
		self.turn_off_servers()		
		self.handle_request()
		self.handle_queue()

	def serve_request(self):
		# time = departure time, serve request
		for server in self.servers:
			if server.departure_time == self.time and server.is_busy and server.is_deployed:
				served_request = self.servers[server.ID].unload()
				self.served_requests.append(served_request)

	def handle_request(self):
		# time = new request arrive, handle request
		first_generated_request = self.get_first_arrived_generated_request()
		if first_generated_request.arrival_time == self.time:
			if self.get_free_deployed_servers_count() > 0:
				self.servers[self.get_free_deployed_server().ID].load(self.generated_request)
			else:
				self.queue.push(self.generated_request)
			self.pop_generated_request(first_generated_request)
			self.generated_request = self.flow.generate()
			self.generated_requests.append(self.generated_request)
						
	def handle_queue(self):
		# handle queue at current time
		for request in self.queue.requests:
			if self.get_free_deployed_servers_count() > 0:
				request_from_queue = self.queue.pop(request, self.time)
				request_from_queue.queue_size_at_serving = len(self.queue.requests)
				request_from_queue.server_arrival_time = self.time
				self.servers[self.get_free_deployed_server().ID].load(request_from_queue)
			else: break		

	def start(self):
		"""
			Run simulation
		"""
		if self.is_debug: print("Simulation started")

		self.generated_request = self.flow.generate()
		self.generated_requests.append(self.generated_request)

		while self.time < self.simulation_time:
			self.run()
		if self.is_debug:
			print("Simulation ended")

	def start_requests(self, requestsToServe):
		"""
			Run simulation
		"""
		if self.is_debug: print("Simulation started")

		self.generated_request = self.flow.generate()
		self.generated_requests.append(self.generated_request)

		while len(self.served_requests) < requestsToServe:
			self.run()
		if self.is_debug:
			print("Simulation ended")

	def run(self):
		if self.is_debug: print("TIME = ", self.time)

		# IDLE
		if self.system_state == States.IDLE:
			self.handle_idle_mode()
		# TURN UP or FULL
		elif self.system_state == States.TURN_UP or self.system_state == States.FULL:
			self.handle_turn_on_mode()
		# TURN DOWN
		elif self.system_state == States.TURN_OFF:
			self.handle_turn_off_mode()

		self.update_system_state()
		self.update_time()
		self.update_state_time()
		self.update_state_count()

		self.debug_run()

	def debug_run(self):
		if self.is_debug:
			print("	", self.system_state)
			print("	Q = ", len(self.queue.requests), ", ",
				  "blocked = ", self.queue.blocked, ", ",
				  " busy = ", self.get_busy_deployed_servers_count(), "/", self.get_deployed_servers_count(), ",",
				  " free = ", self.get_free_deployed_servers_count(), "/", self.get_deployed_servers_count(), ",",
				  "C = ", self.servers_count, ",",
				  " generated = ", self.flow.generated_count, ",",
				  " served =", len(self.served_requests))

			# for server in self.servers:
			# 	server.get_info()

			print("	up-down: count = ", self.up_down_count, ", mean = ", self.up_down_mean, ", total = ", self.up_down_time)
			print(self.state_count)
			print(self.state_time)

		if self.is_debug and not self.auto_continue:
			user_input = input("	Press Enter to for next step, or input 'True' to turn on auto continue mode: ")
			if bool(user_input) == True:
				self.auto_continue = True