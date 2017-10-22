import sys
import time

sys.path.append('../')
from core.simulation import Simulation
from theoretical.mmcr import MMCR


def main():
	if len(sys.argv) != 7:
		print("Input parameters must be: 'lambda mu C Q simulation_time repeats'")
	else:
		start_time = time.time()
		print("Difference test for theoretical M/M/C/R model and 'm/m/c/r' imitation mode.")

		lambd = float(sys.argv[1])
		mu = float(sys.argv[2])
		C = int(sys.argv[3])
		Q = int(sys.argv[4])
		simulation_time = int(sys.argv[5])
		repeats = int(sys.argv[6])

		theoretical_mmcr = MMCR(lambd, mu, C, Q)
		theoretical_result = theoretical_mmcr.run()

		B = theoretical_result[0]
		W = theoretical_result[1]
		N = theoretical_result[2]

		### sim
		B2 = 0
		W2 = 0
		N2 = 0
		theta = 1
		L = 1
		H = 1
		c0 = C
		is_debug =  False
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

		B2 /= repeats
		W2 /= repeats
		N2 /= repeats

		end_time = time.time()

		print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2-B)/B),
			  "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2-W)/W),
			  "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N))

		print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
	main()
