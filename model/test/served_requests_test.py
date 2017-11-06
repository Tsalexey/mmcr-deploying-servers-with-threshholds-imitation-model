import csv
import time
import sys

import os
sys.path.append('../')
from core.simulation import Simulation
from theoretical.mmcr import MMCR

def main():
    lambd = 2
    mu = 1
    theta = 0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    C = 5
    c0 = 1
    Q = 10
    L = 3
    H = 6
    simulation_time = 1000
    repeats = 1
    served_requests = [10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10]

    files = []

    for sr in served_requests:
        start_time = time.time()
        theoretical_mmcr = MMCR(lambd, mu, c0, Q)
        theoretical_result = theoretical_mmcr.run()

        B = theoretical_result[0]
        W = theoretical_result[1]
        N = theoretical_result[2]

        ### sim
        B2 = 0
        W2 = 0
        N2 = 0

        served = 0

        is_debug = False
        if is_debug: print("Q=",Q)

        simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
        for i in range(0, repeats):
            simulation = Simulation("m/m/c/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
            simulation.start(sr)
            B2 += simulation.queue.blocked / (simulation.queue.blocked + len(simulation.served_requests))

            w = 0
            for request in simulation.served_requests:
                w += (request.server_arrival_time + request.beta) - request.arrival_time
            W2 += w / len(simulation.served_requests)
            N2 += (w / len(simulation.served_requests)) * lambd

            w_q = 0
            for request in simulation.served_requests:
                w_q += request.server_arrival_time - request.queue_arrival_time

        B2 /= repeats
        W2 /= repeats
        N2 /= repeats

        end_time = time.time()


        abs_path = os.path.abspath(__file__)
        #os.path.relpath(abs_path) + "\\" +
        path =  'served_requests_test' + '-(lambda=%s,mu=%s,theta=%s,C=%s,c0=%s,L=%s,H=%s,sim_time=%s, served requests =%s)' % (
            lambd, mu, theta, C, c0, L, H, (end_time-start_time), sr)
        path = path + ".csv"

        outfile = open(path, 'w')
        output = csv.writer(outfile, delimiter=';')
        output.writerow(['Served', 'theor B', 'imit B', 'diff'])
        outrow = []
        outrow.append(B)
        outrow.append(B2)
        outrow.append(abs((B2 - B) / B))
        output.writerow(outrow)
        output.writerow(['Served', 'theor N', 'imit N', 'diff'])
        outrow = []
        outrow.append(N)
        outrow.append(N2)
        outrow.append(abs((N2 - N) / N))
        output.writerow(outrow)
        output.writerow(['Served', 'theor W', 'imit W', 'diff'])
        outrow = []
        outrow.append(W)
        outrow.append(W2)
        outrow.append(abs((W2 - W) / W))
        output.writerow(outrow)
        outfile.close()

        files.append(path)

        print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2 - B) / B),
                  "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2 - W) / W),
                  "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N))

if __name__ == '__main__':
	main()

