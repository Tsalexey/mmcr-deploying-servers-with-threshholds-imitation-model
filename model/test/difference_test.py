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
		R = int(sys.argv[4])
		simulation_time = int(sys.argv[5])
		repeats = int(sys.argv[6])

		theoretical_mmcr = MMCR(lambd, mu, C, R)
		theoretical_result = theoretical_mmcr.run()

		B = theoretical_result[0]
		W = theoretical_result[1]
		N = theoretical_result[2]
		Wq = theoretical_result[3]
		Q = theoretical_result[4]

		### sim
		B2 = 0
		W2 = 0
		N2 = 0
		Wq2 = 0
		Q2 = 0

		theta = 1
		L = 1
		H = 1
		c0 = C
		is_debug = False
		simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, R, is_debug)
		for i in range(0, repeats):
			simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, R, is_debug)
			simulation.start()
			B2 += simulation.queue.blocked/(simulation.queue.blocked+simulation.served_count)

			w = 0
			for request in simulation.served_requests:
				w += request.w
			for request in simulation.queue.blocked_requests:
				w+= request.w
			W2 += w/(simulation.served_count + len(simulation.queue.blocked_requests))
			N2 += (w/(simulation.served_count + len(simulation.queue.blocked_requests)))*lambd

			wq = 0
			for request in simulation.served_requests:
				wq += request.wq
			for request in simulation.queue.blocked_requests:
				wq += request.wq
			Wq2 += wq / (simulation.served_count + len(simulation.queue.blocked_requests))
			Q2 += (wq / (simulation.served_count + len(simulation.queue.blocked_requests))) * lambd

		B2 /= repeats
		W2 /= repeats
		N2 /= repeats
		Wq2 /= repeats
		Q2 /= repeats

		end_time = time.time()

		print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2-B)/B),
			  "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2-W)/W),
			  "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N),
			  "\ntheoretical Wq =", Wq, ", simulation Wq=", Wq2, ", Difference = ", abs((Wq2 - Wq) / Wq),
			  "\ntheoretical Q =", Q, ", simulation Q=", Q2, ", Difference = ", abs((Q2 - Q) / Q)
			  )

		print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
	main()
