__author__ = 'tsarev alexey'

import random
import csv
import sys
import os
import time

from validator import Validator
from input_parser import Input_parser

'''
	This class is designed to collect simulation statistics and out it to file
'''
def write_results(input_map, simulations):
	'''
		Write simulation data to output file
	'''
	# TODO 
	print()

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

		# stat = Statistics(x_axis, x_range, input_map, )
		# simulations = stat.generate()
		# write_results(input_map, simulations)

		end_time = time.time()
		print("Execution finished. Execution time = %s seconds" % (end_time - start_time))

if __name__ == '__main__':
	main()

