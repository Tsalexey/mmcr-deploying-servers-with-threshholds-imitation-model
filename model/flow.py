import random
import math
from request import Request
#--------------------------------------------------------------------------------------------------------------------#
#													   FLOW														  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Flow:
	def __init__(self, lambd, mu):
		self.lambd = lambd
		self.mu = mu
		self.next_arrival_time = 0
		self.request_id = 0
		self.generated_count = 0

	def generate(self):
		alpha = random.expovariate(self.lambd)
		beta = random.expovariate(self.mu)
		self.next_arrival_time += alpha
		self.request_id += 1
		self.generated_count += 1
		return Request(self.request_id, self.next_arrival_time, alpha, beta)