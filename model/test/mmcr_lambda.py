import math
import sys
import numpy as np
import os
import csv

def main():
	if len(sys.argv) != 7:
		print("Input parameters must be: 'step lambda1 lambda2 mu C Q'")
	else:
		step = float(sys.argv[1])
		lambd1 = float(sys.argv[2])
		lambd2 = float(sys.argv[3])
		mu = float(sys.argv[4])
		C = int(sys.argv[5])
		Q = int(sys.argv[6])

		print("M/M/C/R: step =", step, ", lambda1 =", lambd1,  "lambda2 =", lambd2, ", mu =", mu, ", C =", C, ", Q =", Q)

		lambd = []
		blocks = []

		for L in np.arange(lambd1, lambd2+1, step):
			ro = L/mu
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
			lambd.append(L)
			blocks.append(B)

		# write stats to file
		abs_path = os.path.abspath(__file__)
		path = os.path.relpath('stats', abs_path) + "\\" + "mmcr_lambda" + '-(%s,%s,%s,%s,%s).csv' % (lambd1, lambd2, mu, C, Q)

		outfile=open(path,'w')
		output = csv.writer(outfile, delimiter=';')
		output.writerow(['#Lambda','B'])

		i=0
		for ll in lambd:
			outrow=[]
			outrow.append(lambd[i])
			outrow.append(blocks[i])
			output.writerow(outrow)
			i += 1
		outfile.close()


if __name__ == '__main__':
	main()