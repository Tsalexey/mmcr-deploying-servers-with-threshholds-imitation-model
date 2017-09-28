__author__ = 'tsarev alexey'

import random
import csv
import sys
import os
import time

from validator import Validator
from input_parser import Input_parser
from statistics import Statistics
'''
	This class is designed to collect simulation statistics and write it to file
'''

def main():
	'''
		Main method
	'''
	print("")
	if not Validator().validate_stat_generator(sys.argv):
		print("Fix problems and try again!\n")
	else:
		start_time = time.time()

		[x_axis, x_range, input_map] = Input_parser().parse_input(sys.argv)
		
		print("\nInput parameters:")
		for key, value in input_map.items():
			print("		", key, "=", value)

		print("Gathering statistics for ", x_axis, " from ", x_range[0], " to ", x_range[1], " with step ", input_map["step"])

		stat = Statistics(x_axis, x_range, input_map)
		generated_stat = stat.generate()

		print("Gathered ", len(generated_stat), " results to storage")

		filename = sys.argv[1]
		write_results(filename, generated_stat, x_axis, x_range, input_map)

		end_time = time.time()
		print("Execution finished. Total execution time = %s seconds" % (end_time - start_time))

def write_results(filename, generated_stat, x_axis, x_range, input_map):
	'''
		Write simulation data to output file
	'''
	abs_path = os.path.abspath(__file__)

	lamb_parameter = (input_map["lambda"] if x_axis != "lambda" else ('%s-%s'% (x_range[0], x_range[1])))
	mu_parameter = (input_map["mu"] if x_axis != "mu" else ('%s-%s'% (x_range[0], x_range[1])))
	theta_parameter = (input_map["theta"] if x_axis != "theta" else ('%s-%s'% (x_range[0], x_range[1])))
	C_parameter = (input_map["C"] if x_axis != "C" else ('%s-%s'% (x_range[0], x_range[1])))
	c0_parameter = (input_map["c0"] if x_axis != "c0" else ('%s-%s'% (x_range[0], x_range[1])))
	L_parameter = (input_map["L"] if x_axis != "L" else ('%s-%s'% (x_range[0], x_range[1])))
	H_parameter = (input_map["H"] if x_axis != "H" else ('%s-%s'% (x_range[0], x_range[1])))

	path = os.path.relpath('statistics', abs_path) + "\\" + filename + '-(lambda=%s,mu=%s,theta=%s,C=%s,c0=%s,L=%s,H=%s,sim_time=%s).csv' % (lamb_parameter, mu_parameter, theta_parameter, C_parameter, c0_parameter, L_parameter, H_parameter, input_map["simulation_time"])
	print("Result is written to " + path)

	outfile=open(path,'w')
	output = csv.writer(outfile, delimiter=';')
	output.writerow(['# Simulation', 'lambda', 'mu', 'theta', 'C', 'c0', 'L', 'H', 'blocked', 'served', 'generated', 'B', 'N'])

	i=0
	for stat in generated_stat:
		i=i+1
		outrow=[]
		outrow.append(i)
		outrow.append(stat.lambd)
		outrow.append(stat.mu)
		outrow.append(stat.theta)
		outrow.append(stat.servers_count)
		outrow.append(stat.core_servers_count)
		outrow.append(stat.L)
		outrow.append(stat.H)
		outrow.append(stat.blocked)
		outrow.append(stat.served)
		outrow.append(stat.generated)
		outrow.append(stat.B)
		outrow.append(stat.N)
		output.writerow(outrow)
	outfile.close()

if __name__ == '__main__':
	main()

