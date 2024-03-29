import time
import sys

sys.path.append('../')
from core.simulation import Simulation
from theoretical.mmcr import MMCR

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

        print("Difference test for M/M/C[c0]/R: lambda =", lambd, ", mu =", mu, ", C =", C, ", c0=", c0,", Q =", Q, ", theta = ", theta, ", sim time =",
                  simulation_time, ", repeats =", repeats)
        print("c0 will be used for theoretical m/m/c/r calculation")

        ### theoretical
        theoretical_mmcr = MMCR(lambd, mu, c0, Q)
        theoretical_result = theoretical_mmcr.run()

        B = theoretical_result[0]
        W = theoretical_result[1]
        N = theoretical_result[2]

        ### sim
        B2 = 0
        W2 = 0
        N2 = 0

        is_debug = False
        if is_debug: print("Q=",Q)
        simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
        for i in range(0, repeats):
            simulation = Simulation("m/m/c[c0]/r", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
            simulation.start_requests(10000)
            B2 += simulation.queue.blocked / (simulation.queue.blocked + simulation.served_count)

            w = 0
            for request in simulation.served_requests:
                w += request.w
            for request in simulation.queue.blocked_requests:
                w += request.w
            W2 += w / (simulation.served_count + len(simulation.queue.blocked_requests))
            N2 += (w / (simulation.served_count + len(simulation.queue.blocked_requests))) * lambd

        B2 /= repeats
        W2 /= repeats
        N2 /= repeats

        end_time = time.time()

        print("theoretical B =", B, ", simulation B=", B2, ", Difference = ", abs((B2 - B) / B),
                  "\ntheoretical W =", W, ", simulation W=", W2, ", Difference = ", abs((W2 - W) / W),
                  "\ntheoretical N =", N, ", simulation N=", N2, ", Difference = ", abs((N2 - N) / N))

        print("Execution time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
    main()