import math
import sys

def main():
	if len(sys.argv) != 5	:
		print("Input parameters must be: 'lambda mu C Q'")
	else:
		lambd = float(sys.argv[1])
		mu = float(sys.argv[2])
		C = int(sys.argv[3])
		Q = int(sys.argv[4])

		print("Theoretical M/M/C/R: lambda =", lambd, ", mu =", mu, ", C =", C, ", Q =", Q)
		ro = lambd/mu

		p0 = 0;

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
		print("B = ", B)

if __name__ == '__main__':
	main()

