__author__ = 'tsarev alexey'

import csv
import sys
import os
import time

sys.path.append('../')
from graphics.graphics_generator import Graphics_generator
from core.validator import Validator
from core.input_parser import Input_parser
from stats.statistics import Statistics
from core.const import Const

'''
	This class is designed to collect simulation stats and write it to file
'''

def main():
	"""
        Main method
    """
	print("")
	if not Validator().validate_stat_generator(sys.argv):
		print("Fix problems and try again!\n")
	else:
		start_time = time.time()
		const = Const()

		[x_axis, x_range, input_map] = Input_parser().parse_input(sys.argv)

		print("\nInput parameters:")
		for key, value in input_map.items():
			print("		", key, "=", value)

		print("Gathering stats for ", x_axis, " from ", x_range[0], " to ", x_range[1], " with step ",
			  input_map[const.STEP])

		stat = Statistics(x_axis, x_range, input_map)
		generated_stat = stat.generate()

		print("Gathered ", len(generated_stat), " results to storage")

		filename = sys.argv[1]
		write_results(filename, generated_stat, x_axis, x_range, input_map)

		x = []
		B = []
		W = []
		N = []
		Wq = []
		Q = []
		for stat in generated_stat:
			x.append(stat.lambd)
			B.append(stat.B)
			N.append(stat.N)
			W.append(stat.W_system)
			Wq.append(stat.W_queue)
			Q.append(stat.Q)

		y_dict = {"B": B, "W": W, "N": N, "Wq": Wq, "Q": Q}
		path = generate_filename(filename, x_axis, x_range, input_map) + ".pdf"

		Graphics_generator.plot(x, r'$\lambda, мс^-1$', y_dict, path)

		end_time = time.time()
		print("Execution finished. Total execution time = %s seconds" % (end_time - start_time))


def write_results(filename, generated_stat, x_axis, x_range, input_map):
	"""
		Write simulation data to output file
	"""
	path = generate_filename(filename, x_axis, x_range, input_map) + ".csv"
	print("Result is written to " + path)

	outfile=open(path,'w')
	output = csv.writer(outfile, delimiter=';')
	output.writerow(['# Simulation', 'lambda', 'mu', 'theta', 'C', 'c0', 'L', 'H', 'blocked', 'served', 'generated', 'B', 'N', 'W system', 'Q', 'W_queue'])

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
		outrow.append(stat.W_system)
		outrow.append(stat.Q)
		outrow.append(stat.W_queue)
		output.writerow(outrow)
	outfile.close()

def generate_filename(filename, x_axis, x_range, input_map):
	abs_path = os.path.abspath(__file__)

	const = Const()
	lamb_parameter = (input_map[const.LAMBDA] if x_axis != const.LAMBDA else ('%s-%s' % (x_range[0], x_range[1])))
	mu_parameter = (input_map[const.MU] if x_axis != const.MU else ('%s-%s' % (x_range[0], x_range[1])))
	theta_parameter = (input_map[const.THETA] if x_axis != const.THETA else ('%s-%s' % (x_range[0], x_range[1])))
	C_parameter = (input_map[const.C] if x_axis != const.C else ('%s-%s' % (x_range[0], x_range[1])))
	c0_parameter = (input_map[const.C0] if x_axis != const.C0 else ('%s-%s' % (x_range[0], x_range[1])))
	L_parameter = (input_map[const.L] if x_axis != const.L else ('%s-%s' % (x_range[0], x_range[1])))
	H_parameter = (input_map[const.H] if x_axis != const.H else ('%s-%s' % (x_range[0], x_range[1])))

	path = os.path.relpath('stats',
						   abs_path) + "\\" + filename + '-(lambda=%s,mu=%s,theta=%s,C=%s,c0=%s,L=%s,H=%s,sim_time=%s)' % (
	lamb_parameter, mu_parameter, theta_parameter, C_parameter, c0_parameter, L_parameter, H_parameter,
	input_map["simulation_time"])
	return path

if __name__ == '__main__':
	main()

