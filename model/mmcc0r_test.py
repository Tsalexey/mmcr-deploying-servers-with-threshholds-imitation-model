import math
import sys
import time
from simulation import Simulation


def main():
    start_time = time.time()

    lambd = 3
    mu = 1
    theta = 0.00000000000000000000000000000000000000000000001
    C = 5
    c0 = 1
    Q = 5
    #
    L = 1
    H = 1
    #
    simulation_time = 1000
    repeats = 10

    print("Test for M/M/C[c0]/R: lambda =", lambd, ", mu =", mu, ", C =", C, ", c0=", c0,", Q =", Q, ", theta = ", theta, ", sim time =",
              simulation_time, ", repeats =", repeats)

    ### sim
    B = 0
    W = 0
    W_q = 0
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

        w_q = 0
        for request in simulation.served_requests:
            w_q += request.server_arrival_time - request.queue_arrival_time
        W_q += w_q / len(simulation.served_requests)
        Q += (w_q / len(simulation.served_requests)) * lambd
    B /= repeats
    W /= repeats
    N /= repeats
    W_q /= repeats
    Q /= repeats

    end_time = time.time()
    # print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs(math.pow(B, 2) - math.pow(B2, 2)))
    print("B =", B, "\nW =", W, "\nN =", N, "\nQ =", Q, "\nW_q =", W_q)

    print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
    main()
