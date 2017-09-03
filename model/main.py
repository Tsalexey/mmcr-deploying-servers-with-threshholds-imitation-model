__author__ = 'tsarev alexey'

import random
import csv
import sys
import os

from enum import Enum
from simulation import Simulation
from server import Server
from queue import Queue
from request import Request
from flow import Flow

def main():
	if len(sys.argv) != 12:
		print("Input parameters must be: 'filename lambda mu theta C c0 Q L H simulation_time is_debug'")
	else:
		file_name = sys.argv[1]
		lambd = float(sys.argv[2])
		mu = float(sys.argv[3])
		theta = float(sys.argv[4])
		C = int(sys.argv[5])
		c0 = int(sys.argv[6])
		Q = int(sys.argv[7])
		L = int(sys.argv[8])
		H = int(sys.argv[9])
		simulation_time = float(sys.argv[10]);
		is_debug = True if sys.argv[11] == "True" else False;

		simulation = Simulation(lambd, mu, theta, C, c0, L, H, simulation_time, Q, is_debug)
		simulation.start()

		abs_path = os.path.abspath(__file__)
		path = os.path.relpath('statistics', abs_path) + "\\" + file_name + '-(%s,%s,%s,%s,%s,%s,%s,%s).csv' % (lambd,mu,theta,C,c0,L,H,simulation_time)

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

		if is_debug:
			print( "")
			print( "Summary results:")
			print( "... to be implemented")
		return simulation

if __name__ == '__main__':
	main()

