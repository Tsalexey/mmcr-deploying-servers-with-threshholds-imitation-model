__author__ = 'tsarev alexey'

import random
import math
from request import Request
#--------------------------------------------------------------------------------------------------------------------#
#													   FLOW														  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Flow:
	'''
		This class reperesents Data Flow
	'''
	def __init__(self, lambd, mu, is_debug):
		self.lambd = lambd
		self.mu = mu
		self.next_arrival_time = 0
		self.request_id = 0
		self.generated_count = 0
		self.is_debug = is_debug

	def generate(self):
		'''
			Generate new request arrival
		'''
		if self.is_debug: print("		generated new request")
		alpha = random.expovariate(self.lambd)
		beta = random.expovariate(self.mu)
		self.next_arrival_time += alpha
		self.request_id += 1
		self.generated_count += 1
		return Request(self.request_id, self.next_arrival_time, alpha, beta)