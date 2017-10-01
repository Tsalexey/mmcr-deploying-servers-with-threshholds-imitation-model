import math
import sys
import time
from simulation import Simulation

def main():
	if len(sys.argv) != 7:
		print("Input parameters must be: 'lambda mu C Q simulation_time repeats'")
	else:
		start_time = time.time()

		lambd = float(sys.argv[1])
		mu = float(sys.argv[2])
		C = int(sys.argv[3])
		Q = int(sys.argv[4])
		simulation_time = int(sys.argv[5])
		repeats = int(sys.argv[6])

		print("Difference test for M/M/C/R: lambda =", lambd, ", mu =", mu, ", C =", C, ", Q =", Q, ", sim time =", simulation_time, ", repeats =", repeats)

		### theoretical
		ro = lambd/mu
		p0 = 0

		for i in range(0, C):
			p0 += math.pow(ro, i)/math.factorial(i)

		for i in range(C, C+Q+1):
			p0 += math.pow(ro, i)/(math.pow(C, i-C)*math.factorial(C))

		p0 = math.pow(p0, -1)

		p = []
		p.append(p0)
		for i in range(1, C+Q+1):
			if i <= C-1:
				p.append(math.pow(ro, i)/math.factorial(i)*p0)
			else:
				p.append(p0*math.pow(ro, i)/(math.pow(C, i-C)*math.factorial(C)))

		B = p[C+Q]
		W = 0
		N = 0
		for x in p:
			N += x*p.index(x)
		W = N/lambd

		Q = 0
		W_q = 0

		i = 0
		for x in p:
			if i >= C+1:
				Q += x*p.index(x)

			i +=1
		W_q = Q/lambd

		### sim
		B2 = 0
		W2 = 0
		W2_q = 0
		Q2 = 0
		N2 = 0
		theta = 1
		L = 1
		H = 1
		c0 = C
		is_debug = False
		simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
		for i in range(0, repeats):
			simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
			simulation.start()
			B2 += simulation.queue.blocked/(simulation.queue.blocked+len(simulation.served_requests))
			
			w = 0
			for request in simulation.served_requests:
				w += (request.server_arrival_time + request.beta) - request.arrival_time
			W2 += w/len(simulation.served_requests)
			N2 += (w/len(simulation.served_requests))*lambd

			w_q = 0
			for request in simulation.served_requests:
				w_q += request.server_arrival_time - request.queue_arrival_time
			W2_q += w_q/len(simulation.served_requests)
			Q2 += (w_q/len(simulation.served_requests))*lambd
		B2 /= repeats
		W2 /= repeats
		N2 /= repeats
		W2_q /= repeats
		Q2 /= repeats

		end_time = time.time()
		# print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs(math.pow(B, 2) - math.pow(B2, 2)))
		print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2-B)/B),
			  "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2-W)/W),
			  "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N),
			  "\ntheoretical Q =", Q, ", simulation Q=", Q2, ", Difference = ", abs((Q2-Q)/Q),
			  "\ntheoretical W_q =", W_q, ", simulation W_q=", W2_q, ", Difference = ", abs((W2_q - W_q) / W_q))

		# print("N=", N, ", N2=", N2)
		# print("W=", W, ", W2=", W2)

		print("Execution time = %s seconds" % (end_time - start_time))
if __name__ == '__main__':
	main()