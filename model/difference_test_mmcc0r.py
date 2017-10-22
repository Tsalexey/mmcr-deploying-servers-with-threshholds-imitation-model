import math
import sys
import time
from simulation import Simulation


def main():
    start_time = time.time()

    lambd = 2
    mu = 1
    theta = 0.1
    C = 5
    c0 = 3
    Q = 20
    #
    L = 1
    H = 1
    #
    simulation_time = 1000
    repeats = 5

    print("Test for M/M/C[c0]/R: lambda =", lambd, ", mu =", mu, ", C =", C, ", c0=", c0,", Q =", Q, ", theta = ", theta, ", sim time =",
              simulation_time, ", repeats =", repeats)

    ### theoretical
    ro = lambd / mu
    p0 = 0

    for i in range(0, C):
        p0 += math.pow(ro, i) / math.factorial(i)

    for i in range(C, C + Q + 1):
        p0 += math.pow(ro, i) / (math.pow(C, i - C) * math.factorial(C))

    p0 = math.pow(p0, -1)

    p = []
    p.append(p0)
    for i in range(1, C + Q + 1):
        if i <= C - 1:
            p.append(math.pow(ro, i) / math.factorial(i) * p0)
        else:
            p.append(p0 * math.pow(ro, i) / (math.pow(C, i - C) * math.factorial(C)))

    B = p[C + Q]
    W = 0
    N = 0
    for x in p:
        N += x * p.index(x)
    W = N / lambd

    ### sim
    B2 = 0
    W2 = 0
    N2 = 0

    is_debug = False
    if is_debug: print("Q=",Q)
    simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
    for i in range(0, repeats):
        simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
        simulation.start()
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
    # print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs(math.pow(B, 2) - math.pow(B2, 2)))
    print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2 - B) / B),
              "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2 - W) / W),
              "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N))

    # print("N=", N, ", N2=", N2)
    # print("W=", W, ", W2=", W2)

    print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
    main()