import time
import sys

sys.path.append('../')
from core.simulation import Simulation


def main():
    if len(sys.argv) != 11:
        print("Input parameters must be: 'lambda mu theta C c0 Q L H simulation_time repeats'")
    else:
        start_time = time.time()

        lambd = float(sys.argv[1])
        mu = float(sys.argv[2])
        theta = float(sys.argv[3])
        C = int(sys.argv[4])
        c0 = int(sys.argv[5])
        Q = int(sys.argv[6])
        L = int(sys.argv[7])
        H = int(sys.argv[8])
        simulation_time = int(sys.argv[9])
        repeats = int(sys.argv[10])

        print("Test for M/M/C[c0]/R[L,H]: lambda =", lambd, ", mu =", mu, ", theta = ", theta,
              ", C =", C, ", c0=", c0, ", Q =", Q, ", sim time =",
              simulation_time, ", repeats =", repeats)

        B = 0
        W = 0
        N = 0

        is_debug = False
        simulation = Simulation("m/m/c[c0]/r[l,h]", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
        for i in range(0, repeats):
            simulation = Simulation("m/m/c[c0]/r[l,h]", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
            simulation.start_requests(simulation_time)
            B += simulation.queue.blocked / (simulation.queue.blocked + len(simulation.served_requests))

            w = 0
            for request in simulation.served_requests:
                w += request.w
            for request in simulation.queue.blocked_requests:
                w += request.w
            W += w / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))
            N += (w / (len(simulation.served_requests) + len(simulation.queue.blocked_requests))) * lambd

        B /= repeats
        W /= repeats
        N /= repeats

        end_time = time.time()

        print("B =", B, "\nW =", W, "\nN =", N)
        print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
    main()

