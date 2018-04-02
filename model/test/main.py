__author__ = 'tsarev alexey'

import csv
import os
import sys
import time

sys.path.append('../')
from core.simulation import Simulation

'''
	This class is designed for one simple Simulation execution
'''
def main():
	"""
	Main method to launch
	"""
	if len(sys.argv) < 12 or len(sys.argv) > 13:
		print("Input parameters must be: 'filename lambda mu C c0 Q theta L H simulation_time is_debug repeats(optionally)'")
	else:
		start_time = time.time()

		file_name = sys.argv[1]
		lambd = float(sys.argv[2])
		mu = float(sys.argv[3])
		C = int(sys.argv[4])
		c0 = int(sys.argv[5])
		Q = int(sys.argv[6])
		theta = float(sys.argv[7])
		L = int(sys.argv[8])
		H = int(sys.argv[9])
		simulation_time = float(sys.argv[10]);
		is_debug = True if sys.argv[11] == "True" else False;
		repeats = int(sys.argv[12]) if len(sys.argv) == 13 else 1;

		print("Simulation started for params: lambda =", lambd,
			                                  ", mu =", mu,
			                                  ", C =", C,
			                                  ", c0 =", c0,
			                                  ", Q =", Q,
			                                  ", theta =", theta,
			                                  ", L =", L,
			                                  ", H =", H,
			                                  ", repeats =", repeats)

		blocked = 0
		served = 0
		generated = 0
		B = 0
		N = 0

		simulation = Simulation("m/m/c[c0]/r[l,h]", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
		for i in range(0, repeats):
			simulation = Simulation("m/m/c[c0]/r[l,h]", lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
			simulation.start()
			blocked += simulation.queue.blocked
			served += simulation.served_count
			generated += simulation.flow.generated_count
			B += simulation.queue.blocked/(simulation.served_count+simulation.queue.blocked)
			N += simulation.served_count/simulation_time
		end_time = time.time()

		blocked = blocked/repeats
		served = served/repeats
		generated = generated/repeats
		B = B/repeats
		N = N/repeats

		print( "")
		print( "Summary results:")
		print( "blocked=", blocked, " served=", served, ", generated=", generated)
		print("B = ", B)
		print("N = ", N)
		print("Execution time = %s seconds" % (end_time - start_time))
		print( "... to be implemented more summary ...")

		# write stats to file
		abs_path = os.path.abspath(__file__)
		path = os.path.relpath('stats', abs_path)
		path = os.path.join(path, file_name + '-(%s,%s,%s,%s,%s,%s,%s,%s).csv' % (lambd,mu,theta,C,c0,L,H,simulation_time))

		outfile=open(path,'w')
		output = csv.writer(outfile, delimiter=';')
		output.writerow(['Request ID','Queue', 'Arrival_Time','Queue_Arrival_time','Server_Arrival_time','alpha','beta'])

		i=0
		for request in simulation.served_requests:
			i=i+1
			outrow=[]
			outrow.append(request.ID)
			outrow.append(request.queue_size_at_serving)
			outrow.append(request.arrival_time)
			outrow.append(request.queue_arrival_time)
			outrow.append(request.server_arrival_time)
			outrow.append(request.alpha)
			outrow.append(request.beta)
			output.writerow(outrow)
		outfile.close()

		return simulation

if __name__ == '__main__':
	main()

