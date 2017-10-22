import time
import sys

sys.path.append('../')
from core.simulation import Simulation


def main():
    if len(sys.argv) != 9:
        print("Input parameters must be: 'lambda mu theta C c0 Q simulation_time repeats'")
    else:
        start_time = time.time()

        lambd = float(sys.argv[1])
        mu = float(sys.argv[2])
        theta = float(sys.argv[3])
        C = int(sys.argv[4])
        c0 = int(sys.argv[5])
        Q = int(sys.argv[6])
        simulation_time = int(sys.argv[7])
        repeats = int(sys.argv[8])

        print("Test for M/M/C[c0]/R: lambda =", lambd, ", mu =", mu, ", theta = ", theta,
              ", C =", C, ", c0=", c0, ", Q =", Q, ", sim time =",
              simulation_time, ", repeats =", repeats)

        # unused parameters
        L = 1
        H = 1
        #

        B = 0
        W = 0
        N = 0

        is_debug =  False
        simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
        for i in range(0, repeats):
            simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
            simulation.start()
            B += simulation.queue.blocked / (simulation.queue.blocked + len(simulation.served_requests))

            w = 0
            for request in simulation.served_requests:
                w += (request.server_arrival_time + request.beta) - request.arrival_time
            W += w / len(simulation.served_requests)
            N += (w / len(simulation.served_requests)) * lambd

        B /= repeats
        W /= repeats
        N /= repeats

        end_time = time.time()

        print("B =", B, "\nW =", W, "\nN =", N)
        print("Execution time = %s seconds" % (end_time - start_time))

if __name__ == '__main__':
    main()
