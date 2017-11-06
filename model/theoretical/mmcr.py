__author__ = "alexey tsarev"
import math


class MMCR:

	def __init__(self, lambd, mu, C, R):
		self.lambd = lambd
		self.mu = mu
		self.C = C
		self.R = R

	def run(self):
		print("Theoretical M/M/C/R: lambda =", self.lambd, ", mu =", self.mu, ", C =", self.C, ", R =", self.R)

		ro = self.lambd/self.mu

		p0 = 0

		for i in range(0, self.C):
			p0 += math.pow(ro, i)/math.factorial(i)

		for i in range(self.C, self.C+self.R+1):
			p0 += math.pow(ro, i)/(math.pow(self.C, i-self.C)*math.factorial(self.C))

		p0 = math.pow(p0, -1)

		p = []
		p.append(p0)
		for i in range(1, self.C+self.R+1):
			if i <= self.C-1:
				p.append(math.pow(ro, i)/math.factorial(i)*p0)
			else:
				p.append(p0*math.pow(ro, i)/(math.pow(self.C, i-self.C)*math.factorial(self.C)))

		B = p[self.C+self.R]

		W = 0
		N = 0
		for x in p:
			N += x * p.index(x)
		W = N / self.lambd

		Q = 0
		Wq = 0

		for x in p:
			if p.index(x) > self.C:
				Q += x * p.index(x)
		Wq = Q / self.lambd

		print("MMCR: B = ", B, ", N = ", N, ", W = ", W, ", Wq = ", Wq, ", Q = ", Q)
		return [B, W, N, Wq, Q]
