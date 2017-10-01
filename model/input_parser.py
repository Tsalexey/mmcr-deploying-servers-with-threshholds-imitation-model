__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													   INPUT_PARSER												  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Input_parser:
	"""
	This class is designed to parse input validated by Validator
	"""
	def parse_input(self, args):
		"""
		Convert input args list into map
		"""
		input_map = {}
		x_axis = ""
		x_range = list()
		# fill map
		for i in range(2, len(args)):
			input_list = args[i].split("=")
			if len(input_list[1].split("-")) == 1:
				if input_list[1] == "True" or input_list[1] == "False":
					input_map[input_list[0]] = (True if input_list[1] == "True" else False)
				else:
					input_map[input_list[0]] = float(input_list[1])
			else:
				input_map[input_list[0]] = input_list[1]
		# find axis and range
		for i in range(2, len(args)):
			input_list = args[i].split("=")
			if len(input_list[1].split("-")) == 2:
				l = input_list[1].split("-")
				x_axis = input_list[0]
				for x in l:
					x_range.append(float(x))
		# return data
		return [x_axis, x_range, input_map]