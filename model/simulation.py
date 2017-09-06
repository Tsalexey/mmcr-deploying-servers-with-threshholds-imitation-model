from enum import Enum
from server import Server
from queue import Queue
from request import Request
from flow import Flow
from states import States

#--------------------------------------------------------------------------------------------------------------------#
#													  SIMULATION													 #
#--------------------------------------------------------------------------------------------------------------------#

class Simulation:

	def __init__(self, lambd, mu, theta, servers_count, core_servers_count, L, H, simulation_time, max_queue_size, is_debug):
		self.lambd = lambd
		self.mu = mu
		self.theta = theta
		self.servers_count = servers_count
		self.core_servers_count = core_servers_count
		self.L = L
		self.H = H
		self.simulation_time = simulation_time
		self.is_debug = is_debug
		self.time = 0
		self.flow = Flow(lambd, mu, is_debug)
		self.generated_request = Request(-1, 0, 0, 0)
		self.queue = Queue(max_queue_size, is_debug)
		self.system_state = States.IDLE
		self.servers = []
		self.served_requests = []
		self.generated_requests = []
		for i in range(servers_count):
			self.servers.append(Server(i, True if i < core_servers_count else False, is_debug))

	def get_system_state(self):
		if self.system_state == States.IDLE:
			if len(self.queue.requests) >= self.H:
				return States.TURN_UP
			else:
				return States.IDLE
		elif self.system_state == States.TURN_UP:
			if len(self.queue.requests) <= self.L:
				return States.TURN_OFF
			else:
				return States.TURN_UP
		elif self.system_state == States.TURN_OFF:
			if  len(self.queue.requests) >= self.H:
				return States.TURN_UP
			elif not self.has_turned_servers():
				return States.IDLE
			else:
				return States.TURN_OFF
	
	def update_time(self):
		first_generated_request = self.get_first_arrived_generated_request()
		first_served_server = self.get_first_served_server()
		first_turned_server = self.get_first_turned_server()

		next_arrive_time = first_generated_request.arrival_time
		next_serve_time = self.simulation_time + 1 if first_served_server.ID == -1 else first_served_server.departure_time
		next_turn_time = self.simulation_time + 1 if first_turned_server.ID == -1 else first_turned_server.turn_on_time

		t = min([next_arrive_time, next_serve_time, next_turn_time])
		if self.is_debug:
			t0 = "%.3f"%first_generated_request.arrival_time
			t1 = "never" if next_serve_time == self.simulation_time + 1 else "%.3f"%next_serve_time
			t2 = "never" if next_turn_time == self.simulation_time + 1 else "%.3f"%next_turn_time
			if t == next_arrive_time: event = "ARRIVE"
			if t == next_serve_time: event = "SERVE"
			if t == next_turn_time: event = "TURN"
			print("	next event=", event, ", arrive= ", t0, ", ",
				  "serve= ", t1, "(#", first_served_server.ID, "),"
				  "turn up= ", t2, "(#", first_turned_server.ID, ")")

		self.time = t

		# if self.system_state == States.TURN_OFF:
		# 	for server in self.servers:
		# 		self.servers[server.ID].to_be_turned_on = False

	def get_free_deployed_server(self):
		free_server = False
		for server in self.servers:
			if not server.is_busy and server.is_deployed and not server.to_be_turned_off:
				return server
		return free_server

	def get_free_deployed_servers_count(self):
		count = 0
		for server in self.servers:
			if not server.is_busy and server.is_deployed and not server.to_be_turned_off:
				count += 1
		return count

	def get_busy_deployed_servers_count(self):
		count = 0
		for server in self.servers:
			if server.is_busy and server.is_deployed:
				count += 1
		return count

	def get_deployed_servers_count(self):
		count = 0
		for server in self.servers:
			if server.is_deployed:
				count += 1
		return count

	def get_first_arrived_generated_request(self):
		generated_request = self.generated_requests[0]
		for request in self.generated_requests:
			if request.arrival_time < generated_request.arrival_time:
				generated_request = request
		return generated_request

	def get_first_served_server(self):
		served_server = Server(-1, True, False)
		served_server.departure_time = self.simulation_time + 1
		for server in self.servers:
			if server.is_busy and server.is_deployed and server.departure_time < served_server.departure_time:
				served_server = server
		return served_server

	def get_first_turned_server(self):
		served_server = Server(-1, True, False)
		served_server.turn_on_time = self.simulation_time + 1
		for server in self.servers:		
			if server.to_be_turned_on and server.turn_on_time < served_server.turn_on_time:
				served_server = server
		return served_server

	def get_servers_to_turn_off(self):
		result = []
		# sort servers by departure time
		self.servers.sort(key=lambda x: x.departure_time)
		for i in range(0, len(self.servers)-1):
			self.servers[i].ID = i
		# turn off c(t)-c0 served deployed servers
		turned_off_servers = 0
		for server in self.servers:
			if turned_off_servers < self.get_deployed_servers_count() - self.core_servers_count and server.is_deployed:
				turned_off_servers += 1
				result.append(server)
		return result


	def pop_generated_request(self, request):
		request_id = 0;
		for req in self.generated_requests:
			if req.ID == request.ID:
				self.generated_requests.pop(request_id)
				break;
			request_id += 1

	def has_turned_servers(self):
		return True if len(self.servers) > self.core_servers_count else False

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

	def handle_idle_mode(self):
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
		auto_continue = not self.is_debug

		if self.is_debug:
			print("Simulation started")

		self.generated_request = self.flow.generate()
		self.generated_requests.append(self.generated_request)

		while self.time < self.simulation_time:
			if self.is_debug:
				print("TIME = " , self.time)

			self.system_state = self.get_system_state()
			
			# IDLE
			if self.system_state == States.IDLE:
				self.handle_idle_mode()
			# # TURN UP
			elif self.system_state == States.TURN_UP:
				self.handle_turn_on_mode()
			# # TURN DOWN
			elif self.system_state == States.TURN_OFF:
				self.handle_turn_off_mode()

			if self.is_debug:
				print("	System in ", self.system_state)
				print("	Queue size = ", len(self.queue.requests), ", ", 
					  "blocked = ", self.queue.blocked, ", ",
					  self.get_busy_deployed_servers_count(), "/", self.get_deployed_servers_count(), " busy, ",
					  self.get_free_deployed_servers_count(), "/", self.get_deployed_servers_count(), " free, ",
					  self.servers_count, " total servers, ",
					  self.flow.generated_count, " generated, ",
					  len(self.served_requests), " served")
	
			if self.is_debug:
				for server in self.servers:
					server.get_info()

			self.update_time()

			if self.is_debug and not auto_continue:
				user_input  = input("Press Enter to for next step, or input 'True' to turn on auto continue mode: ")
				if bool(user_input) == True:
					auto_continue = True
		if self.is_debug:
			print("Simulation ended")