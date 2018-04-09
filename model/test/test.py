import random
from numpy import random as rng
from random import SystemRandom
import numpy as np
crypto = SystemRandom()

def generate(lambd):
    return -np.log(crypto.random())/lambd;

lambd = 5;
n = 1000000

for j in range(1,6):
    t = 0;

    for i in range(1, n):
        t += generate(lambd)
        # t +=  rng.exponential(scale=1 /lambd);
        # t += random.expovariate(lambd)
    m = t/n
    print("M = ", m)
    print("M exp = ", 1/lambd)

    t = 0;

    for i in range(1, n):
        a = generate(lambd)
        # a =  rng.exponential(scale=1 /lambd )
        # a = random.expovariate(lambd)
        t += (a-m)*(a-m)

    d = t/n
    print("D = ", d)
    print("D exp = ", 1/lambd/lambd)

    print("________")