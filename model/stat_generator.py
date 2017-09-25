__author__ = 'tsarev alexey'

import random
import csv
import sys
import os

def parse_input(args):
	input_map = {}
	x_axis = ""
	x_range = []
	# fill map
	for i in range(2, 10):
		input_list = args[i].split("=")
		input_map[input_list[0]] = input_list[1]
	# find axis and range
	for key, value in input_map.items():
		if len(value.split("-")) == 2:
			x_axis = key
			x_range =  ([int(x)]  for x in value.split("-"))
	# return data
	return [x_axis, x_range, input_map]

def write_results(input_map, simulations):
	# TODO rewrite 
	# # write statistics to file
	# abs_path = os.path.abspath(__file__)
	# path = os.path.relpath('statistics', abs_path) + "\\" + filename + '-(%s,%s,%s,%s,%s,%s,%s,%s).csv' % (lambd,mu,theta,C,c0,L,H,simulation_time)

	# outfile=open(path,'w')
	# output = csv.writer(outfile, delimiter=';')
	# output.writerow(['Request ID','Queue', 'Arrival_Time','Queue_Arrival_time','Server_Arrival_time','alpha','beta'])

	# i=0
	# for request in simulation.served_requests:
	# 	i=i+1
	# 	outrow=[]
	# 	outrow.append(request.ID)
	# 	outrow.append(request.queue_size_at_serving)
	# 	outrow.append(request.arrival_time)
	# 	outrow.append(request.queue_arrival_time)
	# 	outrow.append(request.server_arrival_time)
	# 	outrow.append(request.alpha)
	# 	outrow.append(request.beta)
	# 	output.writerow(outrow)

	# outfile.close()


def main():
	# TODO: uncomment after Validator implementation
	# if not Validator().validate(sys.argv):
	#	print("Fix the problem and try again!\n")

	start_time = time.time()

	[x_axis, x_range, input_map] = parse_input(sys.argv)

	print("\nInput parameters:")
	for key, value in input_map.items():
		print("		", key, "=", value)

	print("Gathering statistics for ", x_axis, " from ", x_range[0], " to ", x_range[1], " with step ", input_map["step"])

	stat = Statistics(x_axis, x_range, input_map)
	simulations = stat.generate()
	write_results(input_map, simulations)

	end_time = time.time()
	print("Execution finished. Execution time = %s seconds" % (end_time - start_time))

if __name__ == '__main__':
	main()

